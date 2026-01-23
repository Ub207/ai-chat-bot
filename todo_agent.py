import uuid
import re
from datetime import datetime
from typing import Dict, List, Optional, Any

# In-memory storage for tasks
tasks_storage: Dict[str, Dict] = {}

def create_task(session, user_id: str, title: str, description: str = "", priority: str = "medium"):
    """Create a new task for the user"""
    task_id = str(uuid.uuid4())
    new_task = {
        "id": task_id,
        "user_id": user_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    tasks_storage[task_id] = new_task
    return new_task

def get_user_tasks(session, user_id: str):
    """Retrieve all tasks for the user"""
    user_tasks = [task for task in tasks_storage.values() if task["user_id"] == user_id]
    return user_tasks

def update_task_status(session, task_id: str, status: str):
    """Update the status of a task"""
    if task_id in tasks_storage:
        task = tasks_storage[task_id]
        task["status"] = status
        task["updated_at"] = datetime.now().isoformat()
        return task
    return None

def delete_task(session, task_id: str):
    """Delete a task by ID"""
    if task_id in tasks_storage:
        del tasks_storage[task_id]
        return True
    return False

class TodoAgent:
    """
    A Phase-3 Todo Agent that executes real actions using task API functions.
    Implements explicit intent routing for:
    - add task
    - show all tasks
    - update task status
    - delete task
    - review my progress today
    """

    def __init__(self, user_id: str = "demo_user"):
        self.user_id = user_id
        self.session = None  # Placeholder for session

    def parse_command(self, user_input: str) -> Dict[str, Any]:
        """Parse user input to identify command and extract parameters"""
        user_input = user_input.strip()

        # Define command patterns
        patterns = {
            "add_task": r"add task (.+)",
            "show_tasks": r"show all tasks",
            "update_task": r"update task #?(\d+) (completed|pending|in progress|todo)",
            "delete_task": r"delete task #?(\d+)",
            "review_progress": r"review my progress today"
        }

        for cmd, pattern in patterns.items():
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                groups = match.groups()
                if cmd == "add_task":
                    return {"command": cmd, "title": groups[0].strip()}
                elif cmd == "show_tasks":
                    return {"command": cmd}
                elif cmd == "update_task":
                    return {"command": cmd, "task_id": int(groups[0]), "status": groups[1]}
                elif cmd == "delete_task":
                    return {"command": cmd, "task_id": int(groups[0])}
                elif cmd == "review_progress":
                    return {"command": cmd}

        return {"command": "unknown"}

    def execute_command(self, parsed_cmd: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the parsed command and return response"""
        command = parsed_cmd["command"]
        user_id = self.user_id

        if command == "add_task":
            title = parsed_cmd.get("title", "").strip()
            if not title:
                return {
                    "response": "Error: Task title cannot be empty. Please provide a title after 'add task'.",
                    "tool_calls": []
                }

            # Call the create_task function
            try:
                result = create_task(self.session, user_id, title)
                return {
                    "response": f"Task '{title}' added successfully with ID #{result['id'][:8]}!",
                    "tool_calls": [{"function": "create_task", "arguments": {"session": self.session, "user_id": user_id, "title": title, "description": "", "priority": "medium"}}]
                }
            except Exception as e:
                return {
                    "response": f"Error adding task: {str(e)}",
                    "tool_calls": []
                }

        elif command == "show_tasks":
            try:
                tasks = get_user_tasks(self.session, user_id)
                if not tasks:
                    response = "No tasks found for you."
                else:
                    task_list = "\n".join([f"- #{task['id'][:8]}: {task['title']} [{task['status']}]" for task in tasks])
                    response = f"Your tasks:\n{task_list}"

                return {
                    "response": response,
                    "tool_calls": [{"function": "get_user_tasks", "arguments": {"session": self.session, "user_id": user_id}}]
                }
            except Exception as e:
                return {
                    "response": f"Error retrieving tasks: {str(e)}",
                    "tool_calls": []
                }

        elif command == "update_task":
            task_id = parsed_cmd.get("task_id")
            status = parsed_cmd.get("status", "").lower()

            if status == "todo":
                status = "pending"  # Map 'todo' to 'pending'

            try:
                # Find task by index (since user provides #1, #2, etc.)
                user_tasks = get_user_tasks(self.session, user_id)
                if task_id <= 0 or task_id > len(user_tasks):
                    return {
                        "response": f"Error: Task #{task_id} not found.",
                        "tool_calls": []
                    }

                # Get the actual task ID from the list position
                task_to_update = user_tasks[task_id - 1]
                actual_task_id = task_to_update["id"]

                # Update the task status
                update_task_status(self.session, actual_task_id, status)
                return {
                    "response": f"Task #{task_id} ({task_to_update['title']}) updated to '{status}'.",
                    "tool_calls": [{"function": "update_task_status", "arguments": {"session": self.session, "task_id": actual_task_id, "status": status}}]
                }
            except Exception as e:
                return {
                    "response": f"Error updating task: {str(e)}",
                    "tool_calls": []
                }

        elif command == "delete_task":
            task_id = parsed_cmd.get("task_id")
            try:
                # Find task by index
                user_tasks = get_user_tasks(self.session, user_id)
                if task_id <= 0 or task_id > len(user_tasks):
                    return {
                        "response": f"Error: Task #{task_id} not found.",
                        "tool_calls": []
                    }

                # Get the actual task ID from the list position
                task_to_delete = user_tasks[task_id - 1]
                actual_task_id = task_to_delete["id"]

                # Delete the task
                delete_task(self.session, actual_task_id)
                return {
                    "response": f"Task #{task_id} ({task_to_delete['title']}) deleted successfully.",
                    "tool_calls": [{"function": "delete_task", "arguments": {"session": self.session, "task_id": actual_task_id}}]
                }
            except Exception as e:
                return {
                    "response": f"Error deleting task: {str(e)}",
                    "tool_calls": []
                }

        elif command == "review_progress":
            try:
                tasks = get_user_tasks(self.session, user_id)
                if not tasks:
                    response = "You have no tasks yet."
                else:
                    completed_tasks = [task for task in tasks if task['status'].lower() in ['completed', 'done']]
                    pending_tasks = [task for task in tasks if task['status'].lower() in ['pending', 'todo', 'in progress']]

                    response = f"You have {len(completed_tasks)} completed tasks and {len(pending_tasks)} pending tasks.\n\n"

                    if completed_tasks:
                        response += f"Completed: {', '.join([task['title'] for task in completed_tasks])}\n"

                    if pending_tasks:
                        response += f"Pending: {', '.join([task['title'] for task in pending_tasks])}\n"

                return {
                    "response": response,
                    "tool_calls": [{"function": "get_user_tasks", "arguments": {"session": self.session, "user_id": user_id}}]
                }
            except Exception as e:
                return {
                    "response": f"Error reviewing progress: {str(e)}",
                    "tool_calls": []
                }

        else:
            return {
                "response": "Unknown command. Available commands: 'add task <title>', 'show all tasks', 'update task #<id> <status>', 'delete task #<id>', 'review my progress today'",
                "tool_calls": []
            }

    def process_request(self, user_input: str) -> str:
        """Process a todo list request from the user"""
        parsed_cmd = self.parse_command(user_input)
        result = self.execute_command(parsed_cmd)

        return result["response"]

    def add_task(self, task_description: str) -> str:
        """Add a new task to the storage"""
        task_id = str(uuid.uuid4())
        new_task = {
            "id": task_id,
            "description": task_description,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        tasks_storage[task_id] = new_task
        return f"Task added successfully with ID: {task_id[:8]}"

    def show_all_tasks(self) -> str:
        """Show all tasks in the storage"""
        if not self.tasks:
            return "No tasks found."

        task_list = []
        for task_id, task in self.tasks.items():
            status = "✓ Completed" if task["completed"] else "○ Pending"
            task_list.append(f"[{task_id[:8]}] {status}: {task['description']}")

        return "\n".join(task_list)

    def update_task(self, task_id: str, new_description: Optional[str] = None, completed: Optional[bool] = None) -> str:
        """Update an existing task"""
        # Find task by partial ID match
        matched_task_id = None
        for stored_task_id in self.tasks.keys():
            if stored_task_id.startswith(task_id) or task_id.startswith(stored_task_id):
                matched_task_id = stored_task_id
                break

        if not matched_task_id:
            return f"Task with ID '{task_id}' not found."

        task = self.tasks[matched_task_id]
        updates_made = []

        if new_description is not None:
            task["description"] = new_description
            updates_made.append("description")

        if completed is not None:
            task["completed"] = completed
            updates_made.append("status")

        task["updated_at"] = datetime.now().isoformat()

        if updates_made:
            return f"Task [{matched_task_id[:8]}] updated: {', '.join(updates_made)}"
        else:
            return f"No updates made to task [{matched_task_id[:8]}]"

    def review_progress_today(self) -> str:
        """Review progress on tasks created or updated today"""
        today = datetime.now().date().isoformat()
        today_tasks = []

        for task_id, task in self.tasks.items():
            # Check if task was created today
            created_date = datetime.fromisoformat(task["created_at"]).date().isoformat()
            updated_date = datetime.fromisoformat(task["updated_at"]).date().isoformat()

            if created_date == today or updated_date == today:
                status = "✓ Completed" if task["completed"] else "○ Pending"
                today_tasks.append(f"[{task_id[:8]}] {status}: {task['description']}")

        if not today_tasks:
            return "No tasks were created or updated today."

        completed_count = sum(1 for task in today_tasks if "✓ Completed" in task)
        total_count = len(today_tasks)

        result = f"You have {total_count} task(s) from today.\n"
        result += f"Completed: {completed_count}/{total_count}\n\n"
        result += "\n".join(today_tasks)

        return result

    def make_plan_today(self) -> str:
        """Make a plan for today by showing pending tasks"""
        today_pending = []

        for task_id, task in self.tasks.items():
            if not task["completed"]:
                created_date = datetime.fromisoformat(task["created_at"]).date().isoformat()
                if created_date == datetime.now().date().isoformat():
                    today_pending.append(f"[{task_id[:8]}] {task['description']}")

        if not today_pending:
            return "No pending tasks for today. Consider adding some tasks!"

        result = f"Your plan for today ({datetime.now().date()}):\n"
        result += f"You have {len(today_pending)} pending task(s) for today:\n\n"
        result += "\n".join(today_pending)

        return result