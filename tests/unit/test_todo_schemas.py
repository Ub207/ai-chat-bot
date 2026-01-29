"""Unit tests for Todo schemas."""
from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse


class TestTodoCreateSchema:
    """Tests for TodoCreate schema."""

    def test_valid_todo_create(self):
        """Test creating a valid todo."""
        todo = TodoCreate(title="Test todo", description="Test description")
        assert todo.title == "Test todo"
        assert todo.description == "Test description"
        assert todo.is_completed is False
        assert todo.due_at is None

    def test_todo_create_minimal(self):
        """Test creating a todo with minimal data."""
        todo = TodoCreate(title="Minimal todo")
        assert todo.title == "Minimal todo"
        assert todo.description is None
        assert todo.is_completed is False

    def test_todo_create_empty_title_fails(self):
        """Test that empty title raises validation error."""
        with pytest.raises(ValidationError):
            TodoCreate(title="")

    def test_todo_create_title_too_long(self):
        """Test that title over 255 chars raises validation error."""
        with pytest.raises(ValidationError):
            TodoCreate(title="x" * 256)

    def test_todo_create_with_due_at(self):
        """Test creating a todo with due date."""
        due = datetime(2024, 12, 31, 23, 59)
        todo = TodoCreate(title="Due todo", due_at=due)
        assert todo.due_at == due


class TestTodoUpdateSchema:
    """Tests for TodoUpdate schema."""

    def test_valid_todo_update(self):
        """Test creating a valid todo update."""
        update = TodoUpdate(title="Updated title")
        assert update.title == "Updated title"

    def test_todo_update_partial(self):
        """Test partial update with only description."""
        update = TodoUpdate(description="New description")
        assert update.description == "New description"
        assert update.title is None

    def test_todo_update_all_fields(self):
        """Test updating all fields."""
        due = datetime(2024, 12, 31)
        update = TodoUpdate(
            title="Updated",
            description="New desc",
            is_completed=True,
            due_at=due,
        )
        assert update.title == "Updated"
        assert update.description == "New desc"
        assert update.is_completed is True
        assert update.due_at == due


class TestTodoResponseSchema:
    """Tests for TodoResponse schema."""

    def test_todo_response_from_attributes(self):
        """Test creating response from model attributes."""
        now = datetime.utcnow()
        response = TodoResponse(
            id=1,
            title="Test",
            description=None,
            is_completed=False,
            due_at=None,
            created_at=now,
            updated_at=now,
        )
        assert response.id == 1
        assert response.title == "Test"
