"""Utility functions for working with the Todo App Chatbot models"""

import logging
from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from backend.models.chatbot import Conversation, Message, Task
import json

# Configure logger
logger = logging.getLogger(__name__)


def get_user_conversations(session: Session, user_id: str) -> List[Conversation]:
    """Get all conversations for a specific user"""
    statement = select(Conversation).where(Conversation.user_id == user_id)
    return session.exec(statement).all()


def get_conversation_messages(session: Session, conversation_id: int) -> List[Message]:
    """Get all messages for a specific conversation"""
    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    return session.exec(statement).all()


def get_user_tasks(session: Session, user_id: str) -> List[Task]:
    """Get all tasks for a specific user"""
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    return session.exec(statement).all()


def get_active_tasks(session: Session, user_id: str) -> List[Task]:
    """Get active tasks (not completed) for a specific user"""
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.status.in_(["pending", "in_progress"])
    ).order_by(Task.due_date.asc())
    return session.exec(statement).all()


def create_conversation(session: Session, user_id: str) -> Conversation:
    """Create a new conversation for a user"""
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def add_message_to_conversation(
    session: Session,
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    tool_calls: Optional[str] = None
) -> Message:
    """Add a message to a conversation"""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )
    session.add(message)

    # Update conversation timestamp
    conversation = session.get(Conversation, conversation_id)
    conversation.updated_at = datetime.now()

    session.commit()
    session.refresh(message)
    return message


def create_task(
    session: Session,
    user_id: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    priority: str = "medium",
    category: Optional[str] = None,
    conversation_id: Optional[int] = None
) -> Task:
    """Create a new task"""
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        category=category,
        conversation_id=conversation_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task_status(session: Session, task_id: int, status: str) -> Task:
    """Update the status of a task"""
    task = session.get(Task, task_id)
    if task:
        task.status = status
        task.updated_at = datetime.now()
        session.add(task)
        session.commit()
        session.refresh(task)
    return task


def complete_task(session: Session, task_id: int) -> Task:
    """Mark a task as completed"""
    return update_task_status(session, task_id, "completed")


def delete_task(session: Session, task_id: int) -> bool:
    """Delete a task"""
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False


def process_user_message(message: Message, session: Session):
    """
    Process user message and determine intent, then call appropriate backend tools
    """
    user_msg = message.content.strip()
    user_msg_lower = user_msg.lower()

    # Check if message contains multiple commands (more than one command keyword)
    command_keywords = ["add task", "show all tasks", "complete task", "delete task", "what tasks did i add today?"]
    found_commands = []

    for keyword in command_keywords:
        if keyword in user_msg_lower:
            found_commands.append(keyword)

    # If more than one command is detected, reject with error
    if len(found_commands) > 1:
        return {
            "response": "Please send one command at a time.",
            "tool_calls": []
        }

    # PARSE INTENT AND CALL APPROPRIATE TOOLS

    # ADD TASK: "add task <task title>"
    if user_msg_lower.startswith("add task "):
        task_title = user_msg[9:].strip()  # Extract title after "add task "
        if task_title:
            task = create_task(session, message.user_id, task_title)
            return {
                "response": f"Task ID: {task.id}\nTitle: {task.title}\nStatus: {task.status}",
                "tool_calls": [{"name": "add_task", "arguments": {"title": task_title}}]
            }
        else:
            return {
                "response": "Please provide a task title. Example: 'add task Buy groceries'",
                "tool_calls": []
            }

    # SHOW ALL TASKS: "show all tasks" (also accept minor variations)
    elif user_msg_lower in ["show all tasks", "show all task"]:
        tasks = get_user_tasks(session, message.user_id)
        if tasks:
            task_list = "\n".join([f"ID: {task.id}, Title: {task.title}, Status: {task.status}" for task in tasks])
            return {
                "response": f"Your tasks:\n{task_list}",
                "tool_calls": [{"name": "list_tasks", "arguments": {}}]
            }
        else:
            return {
                "response": "You have no tasks yet.",
                "tool_calls": [{"name": "list_tasks", "arguments": {}}]
            }

    # COMPLETE TASK: "complete task <id>"
    elif user_msg_lower.startswith("complete task "):
        task_id_str = user_msg_lower[14:].strip()  # Extract ID after "complete task "

        # Validate that the ID is numeric
        if not task_id_str.isdigit():
            return {
                "response": "Please provide a valid task ID. Example: 'complete task 5'",
                "tool_calls": []
            }

        try:
            task_id = int(task_id_str)
            task = complete_task(session, task_id)

            if task:
                return {
                    "response": f"Task ID: {task.id}\nTitle: {task.title}\nStatus: {task.status}",
                    "tool_calls": [{"name": "complete_task", "arguments": {"task_id": task_id}}]
                }
            else:
                return {
                    "response": f"Task with ID {task_id} not found.",
                    "tool_calls": []
                }
        except ValueError:
            return {
                "response": "Please provide a valid task ID. Example: 'complete task 5'",
                "tool_calls": []
            }

    # DELETE TASK: "delete task <id>"
    elif user_msg_lower.startswith("delete task "):
        task_id_str = user_msg_lower[12:].strip()  # Extract ID after "delete task "

        # Validate that the ID is numeric
        if not task_id_str.isdigit():
            return {
                "response": "Please provide a valid task ID. Example: 'delete task 5'",
                "tool_calls": []
            }

        try:
            task_id = int(task_id_str)
            success = delete_task(session, task_id)

            if success:
                return {
                    "response": f"Task with ID {task_id} has been deleted.",
                    "tool_calls": [{"name": "delete_task", "arguments": {"task_id": task_id}}]
                }
            else:
                return {
                    "response": f"Task with ID {task_id} not found.",
                    "tool_calls": []
                }
        except ValueError:
            return {
                "response": "Please provide a valid task ID. Example: 'delete task 5'",
                "tool_calls": []
            }

    # WHAT TASKS TODAY: "what tasks did I add today?"
    elif user_msg_lower == "what tasks did i add today?":
        from datetime import datetime, date
        today = date.today()

        # Get all tasks for the user
        all_tasks = get_user_tasks(session, message.user_id)

        # Filter tasks created today
        today_tasks = [task for task in all_tasks if task.created_at.date() == today]

        if today_tasks:
            task_list = "\n".join([f"ID: {task.id}, Title: {task.title}" for task in today_tasks])
            return {
                "response": f"You added these tasks today:\n{task_list}",
                "tool_calls": [{"name": "list_tasks", "arguments": {}}]
            }
        else:
            return {
                "response": "You didn't add any tasks today.",
                "tool_calls": [{"name": "list_tasks", "arguments": {}}]
            }

    # GREETINGS
    elif any(x in user_msg_lower for x in ["hi", "hello", "hey"]):
        return {
            "response": "Hello! I'm your Todo Assistant. I can help you with tasks. Try commands like: 'add task Buy groceries', 'show all tasks', 'complete task 1', 'delete task 1', or 'what tasks did I add today?'",
            "tool_calls": []
        }

    # DEFAULT FALLBACK
    else:
        return {
            "response": "I'm a Todo Assistant. Supported commands:\n- 'add task <task title>'\n- 'show all tasks'\n- 'complete task <id>'\n- 'delete task <id>'\n- 'what tasks did I add today?'",
            "tool_calls": []
        }


# Example usage
if __name__ == "__main__":
    from .db import get_db_session

    # Example: Create a conversation and add messages
    with get_db_session() as session:
        # Create a conversation
        conv = create_conversation(session, "test_user_456")
        logger.info(f"Created conversation: {conv.id}")

        # Add messages to the conversation
        msg1 = add_message_to_conversation(
            session,
            conv.id,
            "test_user_456",
            "user",
            "I need to schedule a meeting with the team"
        )
        logger.info(f"Added message: {msg1.id}")

        msg2 = add_message_to_conversation(
            session,
            conv.id,
            "assistant",
            "assistant",
            "Sure, what is the topic and when would you like to schedule it?"
        )
        logger.info(f"Added message: {msg2.id}")

        # Create a task from the conversation
        task = create_task(
            session,
            "test_user_456",
            "Schedule team meeting",
            "Schedule a meeting with the development team to discuss project status",
            priority="high",
            conversation_id=conv.id
        )
        logger.info(f"Created task: {task.id}")

        # Get user's active tasks
        active_tasks = get_active_tasks(session, "test_user_456")
        logger.info(f"Active tasks for user: {len(active_tasks)}")

        # Complete the task
        completed_task = complete_task(session, task.id)
        logger.info(f"Completed task: {completed_task.title}")