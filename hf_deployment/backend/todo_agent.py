"""
REAL Todo Agent Implementation for Hackathon-2 Phase-3
(Evolution of Todo – Agent Implementation)

This agent implements:
1. Intent detection for core todo operations
2. Tool functions for task management
3. Dynamic responses based on stored tasks
4. In-memory storage for tasks
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Configure logger
logger = logging.getLogger(__name__)

class TodoAgent:
    """
    A REAL Todo Agent with intent detection and tool functions.
    Implements the core requirements for Hackathon-2 Phase-3.
    """

    def __init__(self):
        # In-memory storage for tasks (as requested)
        self.tasks = {}
        self.next_task_id = 1

        # Define intent patterns
        self.intent_patterns = {
            'add_task': [
                r'.*add.*task.*',
                r'.*create.*task.*',
                r'.*new.*task.*',
                r'.*make.*task.*',
                r'.*(?:need to|want to|should).*(?:do|complete|finish).*',
                r'.*schedule.*',
                r'.*remind me to.*',
            ],
            'show_tasks': [
                r'.*show.*all.*task.*',
                r'.*list.*task.*',
                r'.*see.*task.*',
                r'.*view.*task.*',
                r'.*what.*task.*',
                r'.*my.*task.*',
                r'.*display.*task.*',
            ],
            'update_task': [
                r'.*update.*task.*',
                r'.*change.*task.*',
                r'.*modify.*task.*',
                r'.*edit.*task.*',
                r'.*mark.*complete.*',
                r'.*done.*',
                r'.*finish.*',
                r'.*complete.*',
                r'.*completed.*',
            ],
            'review_progress': [
                r'.*review.*progress.*',
                r'.*how.*progress.*',
                r'.*check.*progress.*',
                r'.*my.*progress.*',
                r'.*progress.*today.*',
                r'.*accomplished.*today.*',
                r'.*done.*today.*',
            ],
            'make_plan': [
                r'.*plan.*today.*',
                r'.*make.*plan.*today.*',
                r'.*organize.*today.*',
                r'.*arrange.*today.*',
                r'.*schedule.*today.*',
                r'.*what.*do.*today.*',
            ]
        }

    def detect_intent(self, user_input: str) -> str:
        """
        Detect the user's intent from their input.

        Args:
            user_input: The raw user message

        Returns:
            Detected intent as a string
        """
        user_input_lower = user_input.lower().strip()

        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    return intent

        # Default fallback
        return 'unknown'

    def extract_task_details(self, user_input: str) -> Dict[str, str]:
        """
        Extract task details from user input using simple pattern matching.

        Args:
            user_input: The raw user message

        Returns:
            Dictionary with extracted task details
        """
        details = {
            'title': '',
            'description': '',
            'due_date': None,
            'priority': 'medium'
        }

        # Extract title (the main action/task)
        # Remove common prefixes like "I need to", "I want to", etc.
        cleaned_input = re.sub(r'^(i need to|i want to|i should|please|can you|to )', '', user_input.lower()).strip()

        # If it contains common verbs, take the rest as title
        if re.match(r'(add|create|make|schedule|remind me to)', user_input.lower()):
            parts = re.split(r'(add|create|make|schedule|remind me to)', user_input, 1)
            if len(parts) > 2:
                details['title'] = parts[2].strip()
            else:
                details['title'] = cleaned_input
        else:
            details['title'] = user_input.strip()

        # Extract priority indicators
        if any(word in user_input.lower() for word in ['urgent', 'important', 'asap', 'high priority', 'critical']):
            details['priority'] = 'high'
        elif any(word in user_input.lower() for word in ['low priority', 'not urgent', 'whenever']):
            details['priority'] = 'low'

        # Extract due date indicators
        if 'today' in user_input.lower():
            details['due_date'] = datetime.now().strftime('%Y-%m-%d')
        elif 'tomorrow' in user_input.lower():
            tomorrow = datetime.now() + timedelta(days=1)
            details['due_date'] = tomorrow.strftime('%Y-%m-%d')
        elif 'this week' in user_input.lower():
            # Set due date to end of week
            days_ahead = 7 - datetime.now().weekday()
            if days_ahead == 0:  # If today is Sunday
                days_ahead = 7
            weekend_date = datetime.now() + timedelta(days=days_ahead)
            details['due_date'] = weekend_date.strftime('%Y-%m-%d')

        # Set description same as title if not specified
        details['description'] = details['title']

        return details

    def create_task_tool(self, title: str, description: str = "", due_date: str = None, priority: str = "medium") -> Dict:
        """
        Tool function to create a new task.

        Args:
            title: Task title
            description: Task description
            due_date: Due date in YYYY-MM-DD format
            priority: Priority level (low, medium, high)

        Returns:
            Created task dictionary
        """
        task_id = self.next_task_id
        self.next_task_id += 1

        task = {
            'id': task_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'status': 'pending',  # Default status
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        self.tasks[task_id] = task
        logger.info(f"Created task {task_id}: {title}")

        return task

    def list_tasks_tool(self, status_filter: str = None) -> List[Dict]:
        """
        Tool function to list tasks.

        Args:
            status_filter: Optional filter by status (pending, in_progress, completed)

        Returns:
            List of tasks matching the filter
        """
        if status_filter:
            return [task for task in self.tasks.values() if task['status'] == status_filter]
        else:
            return list(self.tasks.values())

    def update_task_tool(self, task_id: int, status: str = None, title: str = None,
                        description: str = None, due_date: str = None, priority: str = None) -> Dict:
        """
        Tool function to update a task.

        Args:
            task_id: ID of the task to update
            status: New status
            title: New title
            description: New description
            due_date: New due date
            priority: New priority

        Returns:
            Updated task dictionary
        """
        if task_id not in self.tasks:
            return {'error': f'Task with ID {task_id} not found'}

        task = self.tasks[task_id]

        # Update fields if provided
        if status is not None:
            task['status'] = status
        if title is not None:
            task['title'] = title
        if description is not None:
            task['description'] = description
        if due_date is not None:
            task['due_date'] = due_date
        if priority is not None:
            task['priority'] = priority

        task['updated_at'] = datetime.now()

        logger.info(f"Updated task {task_id}: status={status}, title={title}")

        return task

    def process_add_task_intent(self, user_input: str) -> Dict:
        """
        Process add task intent.

        Args:
            user_input: Raw user input

        Returns:
            Response dictionary
        """
        task_details = self.extract_task_details(user_input)

        # Create the task
        new_task = self.create_task_tool(
            title=task_details['title'],
            description=task_details['description'],
            due_date=task_details['due_date'],
            priority=task_details['priority']
        )

        response = f"I've added the task '{new_task['title']}' to your list."
        if new_task['due_date']:
            response += f" Due date: {new_task['due_date']}."

        return {
            'response': response,
            'task': new_task,
            'tool_calls': [{'name': 'create_task', 'arguments': task_details}]
        }

    def process_show_tasks_intent(self, user_input: str) -> Dict:
        """
        Process show tasks intent.

        Args:
            user_input: Raw user input

        Returns:
            Response dictionary
        """
        # Determine if user wants all tasks or just active ones
        if 'completed' in user_input.lower():
            tasks = self.list_tasks_tool('completed')
            task_type = 'completed'
        elif 'pending' in user_input.lower() or 'active' in user_input.lower():
            tasks = self.list_tasks_tool('pending')
            task_type = 'pending'
        else:
            tasks = self.list_tasks_tool()
            task_type = 'all'

        if not tasks:
            if task_type == 'all':
                response = "You don't have any tasks in your list yet. Would you like to add one?"
            else:
                response = f"You don't have any {task_type} tasks. Would you like to add one?"
        else:
            response = f"Here are your {task_type} tasks:\n\n"
            for i, task in enumerate(tasks, 1):
                due_str = f" (Due: {task['due_date']})" if task['due_date'] else ""
                response += f"{i}. [{task['status']}] {task['title']}{due_str}\n"

        return {
            'response': response,
            'tasks': tasks,
            'tool_calls': [{'name': 'list_tasks', 'arguments': {'filter': task_type}}]
        }

    def process_update_task_intent(self, user_input: str) -> Dict:
        """
        Process update task intent.

        Args:
            user_input: Raw user input

        Returns:
            Response dictionary
        """
        # Try to extract task ID from user input
        task_id_match = re.search(r'\b(\d+)\b', user_input)
        if task_id_match:
            task_id = int(task_id_match.group(1))
        else:
            # If no specific ID, try to find a pending task that matches keywords
            keywords = re.findall(r'\w+', user_input.lower())
            matching_tasks = []
            for task_id, task in self.tasks.items():
                if task['status'] == 'pending':
                    task_keywords = re.findall(r'\w+', task['title'].lower())
                    if any(k in task_keywords for k in keywords if len(k) > 2):
                        matching_tasks.append(task_id)

            if not matching_tasks:
                return {
                    'response': "I couldn't find a matching task to update. Please specify which task number you want to update.",
                    'tool_calls': []
                }
            elif len(matching_tasks) == 1:
                task_id = matching_tasks[0]
            else:
                # Multiple matches, ask for clarification
                task_titles = [self.tasks[tid]['title'] for tid in matching_tasks]
                return {
                    'response': f"I found multiple tasks that match: {', '.join(task_titles[:3])}. Please specify which task number you want to update.",
                    'tool_calls': []
                }

        # Determine what to update based on user input
        new_status = None
        if any(word in user_input.lower() for word in ['done', 'complete', 'finished', 'completed']):
            new_status = 'completed'
        elif any(word in user_input.lower() for word in ['started', 'working', 'in progress', 'doing']):
            new_status = 'in_progress'
        elif any(word in user_input.lower() for word in ['pending', 'not started', 'later']):
            new_status = 'pending'

        if new_status:
            updated_task = self.update_task_tool(task_id, status=new_status)
            return {
                'response': f"I've updated task '{updated_task['title']}' to status: {updated_task['status']}",
                'task': updated_task,
                'tool_calls': [{'name': 'update_task', 'arguments': {'task_id': task_id, 'status': new_status}}]
            }
        else:
            return {
                'response': f"I'm not sure what update you want to make to task {task_id}. You can mark it as done, in progress, or pending.",
                'tool_calls': []
            }

    def process_review_progress_intent(self, user_input: str) -> Dict:
        """
        Process review progress intent.

        Args:
            user_input: Raw user input

        Returns:
            Response dictionary
        """
        completed_tasks = self.list_tasks_tool('completed')
        pending_tasks = self.list_tasks_tool('pending')
        in_progress_tasks = self.list_tasks_tool('in_progress')

        total_completed = len(completed_tasks)
        total_pending = len(pending_tasks)
        total_in_progress = len(in_progress_tasks)

        if total_completed == 0 and total_pending == 0 and total_in_progress == 0:
            response = "You haven't created any tasks yet. Would you like to add some tasks to track your progress?"
        else:
            response = f"Here's your progress:\n\n"
            response += f"- Completed tasks: {total_completed}\n"
            response += f"- Pending tasks: {total_pending}\n"
            response += f"- In-progress tasks: {total_in_progress}\n\n"

            if completed_tasks:
                response += "Completed tasks:\n"
                for task in completed_tasks[-5:]:  # Show last 5 completed tasks
                    response += f"  • {task['title']}\n"

            if pending_tasks or in_progress_tasks:
                response += "\nActive tasks:\n"
                for task in pending_tasks[:3] + in_progress_tasks[:3]:  # Show up to 3 of each
                    status = task['status']
                    response += f"  • [{status}] {task['title']}\n"

        return {
            'response': response,
            'summary': {
                'completed_count': total_completed,
                'pending_count': total_pending,
                'in_progress_count': total_in_progress
            },
            'tool_calls': [
                {'name': 'list_tasks', 'arguments': {'filter': 'completed'}},
                {'name': 'list_tasks', 'arguments': {'filter': 'pending'}},
                {'name': 'list_tasks', 'arguments': {'filter': 'in_progress'}}
            ]
        }

    def process_make_plan_intent(self, user_input: str) -> Dict:
        """
        Process make plan intent.

        Args:
            user_input: Raw user input

        Returns:
            Response dictionary
        """
        pending_tasks = self.list_tasks_tool('pending')
        in_progress_tasks = self.list_tasks_tool('in_progress')

        all_active_tasks = pending_tasks + in_progress_tasks

        if not all_active_tasks:
            response = "You don't have any active tasks. Here's a simple plan for today:\n\n"
            response += "1. Think about what you want to accomplish today\n"
            response += "2. Add your first task using the 'add task' command\n"
            response += "3. Prioritize your tasks by importance\n"
            response += "4. Work on one task at a time\n"
            response += "5. Mark tasks as complete when done"
        else:
            response = "Here's your plan for today based on your tasks:\n\n"
            response += "Priority tasks to focus on:\n"

            # Sort tasks by priority (high first), then by creation date
            sorted_tasks = sorted(all_active_tasks, key=lambda t: (
                {'high': 0, 'medium': 1, 'low': 2}[t['priority']], t['created_at']
            ))

            for i, task in enumerate(sorted_tasks[:5], 1):  # Limit to top 5 tasks
                priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[task['priority']]
                due_str = f" (Due: {task['due_date']})" if task['due_date'] else ""
                response += f"{i}. {priority_emoji} {task['title']}{due_str}\n"

            response += f"\nTotal active tasks: {len(all_active_tasks)}"

        return {
            'response': response,
            'tool_calls': [
                {'name': 'list_tasks', 'arguments': {'filter': 'pending'}},
                {'name': 'list_tasks', 'arguments': {'filter': 'in_progress'}}
            ]
        }

    def process_message(self, user_input: str) -> Dict:
        """
        Main method to process user input and return agent response.

        Args:
            user_input: Raw user message

        Returns:
            Response dictionary with 'response' and 'tool_calls' keys
        """
        intent = self.detect_intent(user_input)
        logger.info(f"Detected intent: {intent}")

        if intent == 'add_task':
            return self.process_add_task_intent(user_input)
        elif intent == 'show_tasks':
            return self.process_show_tasks_intent(user_input)
        elif intent == 'update_task':
            return self.process_update_task_intent(user_input)
        elif intent == 'review_progress':
            return self.process_review_progress_intent(user_input)
        elif intent == 'make_plan':
            return self.process_make_plan_intent(user_input)
        else:
            # Default response for unknown intents
            return {
                'response': (
                    "Hi! I'm your Todo Agent. I can help you:\n"
                    "• Add tasks (e.g., 'Add a task to buy groceries')\n"
                    "• Show your tasks (e.g., 'Show all my tasks')\n"
                    "• Update task status (e.g., 'Mark task 1 as complete')\n"
                    "• Review your progress (e.g., 'Review my progress today')\n"
                    "• Make a plan for today (e.g., 'Make my plan today')"
                ),
                'tool_calls': []
            }


# Global instance of the agent
todo_agent = TodoAgent()


def process_user_message_with_agent(user_input: str) -> Dict:
    """
    Wrapper function to process user messages with the real Todo Agent.

    Args:
        user_input: Raw user message

    Returns:
        Response dictionary compatible with existing API
    """
    return todo_agent.process_message(user_input)


# Example usage and testing
if __name__ == "__main__":
    # Test the agent with sample inputs
    test_inputs = [
        "Add a task to buy groceries",
        "Show all my tasks",
        "Make my plan today",
        "Review my progress today",
        "Mark task 1 as complete",
        "Update task 1 to in progress"
    ]

    print("Testing the REAL Todo Agent:")
    print("="*50)

    for input_text in test_inputs:
        print(f"\nInput: {input_text}")
        result = process_user_message_with_agent(input_text)
        print(f"Response: {result['response']}")
        print(f"Tool calls: {result['tool_calls']}")
        print("-" * 30)