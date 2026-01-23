#!/usr/bin/env python3
"""
Test script for the TodoAgent implementation
"""

from todo_agent import TodoAgent

def test_todo_agent():
    """Test the TodoAgent functionality"""
    print("Testing TodoAgent implementation...")
    print("="*50)

    # Create a new agent instance with a specific user ID
    agent = TodoAgent(user_id="test_user_123")

    # Test 1: Add tasks
    print("\n1. Testing 'add task' command:")
    response = agent.process_request("add task Buy groceries")
    print(f"Response: {response}")

    response = agent.process_request("add task Complete project proposal")
    print(f"Response: {response}")

    response = agent.process_request("add task Schedule meeting with team")
    print(f"Response: {response}")

    # Test 2: Show all tasks
    print("\n2. Testing 'show all tasks' command:")
    response = agent.process_request("show all tasks")
    print(f"Response:\n{response}")

    # Test 3: Update task status
    print("\n3. Testing 'update task' command:")
    response = agent.process_request("update task #1 completed")
    print(f"Response: {response}")

    # Test 4: Show all tasks again to see the update
    print("\n4. Testing 'show all tasks' command after update:")
    response = agent.process_request("show all tasks")
    print(f"Response:\n{response}")

    # Test 5: Review progress
    print("\n5. Testing 'review my progress today' command:")
    response = agent.process_request("review my progress today")
    print(f"Response:\n{response}")

    # Test 6: Delete a task
    print("\n6. Testing 'delete task' command:")
    response = agent.process_request("delete task #2")
    print(f"Response: {response}")

    # Test 7: Show all tasks after deletion
    print("\n7. Testing 'show all tasks' command after deletion:")
    response = agent.process_request("show all tasks")
    print(f"Response:\n{response}")

    # Test 8: Invalid command
    print("\n8. Testing unknown command:")
    response = agent.process_request("invalid command")
    print(f"Response: {response}")

    print("\n" + "="*50)
    print("Test completed!")

if __name__ == "__main__":
    test_todo_agent()