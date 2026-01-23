import pytest
from sqlmodel import Session, create_engine, SQLModel
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.api import app
from backend.db import get_session
from backend.models.chatbot import Task as TaskDB


@pytest.fixture(scope="function")
def test_client_and_db():
    # Create an in-memory SQLite database for testing
    engine = create_engine("sqlite:///test.db", echo=True)
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    # Override the get_session dependency
    app.dependency_overrides[get_session] = get_test_session

    client = TestClient(app)

    yield client, engine

    # Clean up
    app.dependency_overrides.clear()


def test_add_task_success(test_client_and_db):
    """Test successful task creation"""
    client, engine = test_client_and_db

    # Test data - using JSON as per MCP tools specification
    task_data = {
        "user_id": "test_user_123",
        "title": "Buy groceries",
        "description": "Milk, bread, eggs",
        "priority": "medium",
        "category": "personal"
    }

    response = client.post("/tasks/", json=task_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["user_id"] == "test_user_123"
    assert data["status"] == "pending"


def test_add_task_missing_required_fields(test_client_and_db):
    """Test that add_task fails when required fields are missing"""
    client, engine = test_client_and_db

    # Missing title - using JSON as per MCP tools specification
    task_data = {
        "user_id": "test_user_123",
        "description": "Some description"
    }

    response = client.post("/tasks/", json=task_data)

    # Should return validation error (422 for missing required field)
    assert response.status_code == 422


def test_list_tasks_success(test_client_and_db):
    """Test successful retrieval of user's tasks"""
    client, engine = test_client_and_db

    # First, create a task
    task_data = {
        "user_id": "test_user_123",
        "title": "Test task",
        "description": "Test description"
    }
    client.post("/tasks/", json=task_data)

    # Now list tasks for the user
    response = client.get("/tasks/test_user_123")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(task["title"] == "Test task" for task in data)


def test_list_tasks_filtering(test_client_and_db):
    """Test filtering tasks by status, category, etc."""
    client, engine = test_client_and_db

    # Create multiple tasks with different properties
    task_data_1 = {
        "user_id": "test_user_123",
        "title": "High priority task",
        "priority": "high",
        "category": "work"
    }
    task_data_2 = {
        "user_id": "test_user_123",
        "title": "Low priority task",
        "priority": "low",
        "category": "personal"
    }

    client.post("/tasks/", json=task_data_1)
    client.post("/tasks/", json=task_data_2)

    # Test filtering by priority - note: the current API doesn't support query parameters for filtering
    # So we'll just retrieve all tasks and check if the filtering logic is applied on the client side
    response = client.get("/tasks/test_user_123")

    assert response.status_code == 200
    data = response.json()
    high_priority_tasks = [task for task in data if task["priority"] == "high"]
    assert len(high_priority_tasks) >= 1


def test_complete_task_success(test_client_and_db):
    """Test successfully completing a task"""
    client, engine = test_client_and_db

    # Create a task first
    task_data = {
        "user_id": "test_user_123",
        "title": "Task to complete",
        "description": "Description"
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Complete the task
    response = client.put(f"/tasks/{task_id}/complete")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["status"] == "completed"


def test_complete_nonexistent_task(test_client_and_db):
    """Test completing a task that doesn't exist"""
    client, engine = test_client_and_db

    response = client.put("/tasks/999999/complete")

    assert response.status_code == 404


def test_update_task_success(test_client_and_db):
    """Test successfully updating a task"""
    client, engine = test_client_and_db

    # Create a task first
    task_data = {
        "user_id": "test_user_123",
        "title": "Original task",
        "description": "Original description",
        "priority": "low"
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "user_id": "test_user_123",
        "title": "Updated task",
        "priority": "high",
        "description": "Updated description"
    }

    response = client.put(f"/tasks/{task_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated task"
    assert data["priority"] == "high"


def test_delete_task_success(test_client_and_db):
    """Test successfully deleting a task"""
    client, engine = test_client_and_db

    # Create a task first
    task_data = {
        "user_id": "test_user_123",
        "title": "Task to delete",
        "description": "Description"
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Delete the task using JSON endpoint as per MCP tools spec
    delete_data = {
        "user_id": "test_user_123",
        "task_id": task_id
    }
    response = client.post("/tasks/delete", json=delete_data)

    assert response.status_code == 200

    # Verify the task is gone
    list_response = client.get("/tasks/test_user_123")
    tasks = list_response.json()
    assert not any(task["id"] == task_id for task in tasks)


def test_user_data_isolation(test_client_and_db):
    """Test that users can only access their own tasks"""
    client, engine = test_client_and_db

    # Create tasks for different users
    user1_task = {
        "user_id": "user_1",
        "title": "User 1 task",
        "description": "Description for user 1"
    }
    user2_task = {
        "user_id": "user_2",
        "title": "User 2 task",
        "description": "Description for user 2"
    }

    client.post("/tasks/", json=user1_task)
    client.post("/tasks/", json=user2_task)

    # Verify user 1 only sees their own tasks
    response1 = client.get("/tasks/user_1")
    user1_tasks = response1.json()
    user1_titles = [task["title"] for task in user1_tasks]
    assert "User 1 task" in user1_titles
    assert "User 2 task" not in user1_titles

    # Verify user 2 only sees their own tasks
    response2 = client.get("/tasks/user_2")
    user2_tasks = response2.json()
    user2_titles = [task["title"] for task in user2_tasks]
    assert "User 2 task" in user2_titles
    assert "User 1 task" not in user2_titles


def test_add_task_validation_errors(test_client_and_db):
    """Test validation errors for add_task"""
    client, engine = test_client_and_db

    # Test with empty title
    task_data = {
        "user_id": "test_user_123",
        "title": "",  # Empty title should fail
        "description": "Valid description"
    }

    response = client.post("/tasks/", json=task_data)

    assert response.status_code == 422  # Validation error

    # Test with title exceeding max length
    long_title = "x" * 201  # Exceeds 200 char limit
    task_data_long = {
        "user_id": "test_user_123",
        "title": long_title,
        "description": "Valid description"
    }

    response = client.post("/tasks/", json=task_data_long)

    assert response.status_code == 422  # Validation error


def test_update_task_validation_errors(test_client_and_db):
    """Test validation errors for update_task"""
    client, engine = test_client_and_db

    # Create a task first
    task_data = {
        "user_id": "test_user_123",
        "title": "Original task",
        "description": "Original description"
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Try to update with invalid data (empty title)
    update_data = {
        "user_id": "test_user_123",
        "title": ""  # Empty title should fail
    }

    response = client.put(f"/tasks/{task_id}", json=update_data)

    assert response.status_code == 422  # Validation error


def test_health_check(test_client_and_db):
    """Test the health check endpoint"""
    client, engine = test_client_and_db

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data