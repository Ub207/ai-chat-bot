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
    user_msg = message.content.lower().strip()

    # GREETINGS
    if any(x in user_msg for x in ["hi", "hello", "hey"]):
        return {
            "response": "Hello! I'm your Todo Assistant. I help you plan tasks and manage your day.",
            "tool_calls": []
        }

    # PLAN TODAY
    if "plan" in user_msg and "today" in user_msg:
        return {
            "response": (
                "Here's a clear plan for today:\n"
                "1. Review pending tasks\n"
                "2. Complete one high-priority task\n"
                "3. Take short breaks\n"
                "4. Review progress in the evening"
            ),
            "tool_calls": []
        }

    # PLAN TOMORROW
    if "plan" in user_msg and "tomorrow" in user_msg:
        return {
            "response": (
                "Here's a simple plan for tomorrow:\n"
                "1. Decide top 3 goals\n"
                "2. Prepare tasks in advance\n"
                "3. Start with the hardest task first"
            ),
            "tool_calls": []
        }

    # WHO ARE YOU
    if "who are you" in user_msg:
        return {
            "response": (
                "I'm a Todo Assistant built for Hackathon-2 Phase-3. "
                "I help users plan tasks without using external AI APIs."
            ),
            "tool_calls": []
        }

    # NON-TODO QUESTIONS
    if any(x in user_msg for x in ["ai jobs", "problem solving", "interview"]):
        return {
            "response": (
                "Right now I focus on task planning only. "
                "You can ask me to plan your day or manage tasks."
            ),
            "tool_calls": []
        }

    # DEFAULT FALLBACK
    return {
        "response": (
            "I can help you plan your day, create tasks, or review progress. "
            "Try asking: 'make my plan today'"
        ),
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