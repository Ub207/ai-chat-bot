"""Integration tests for Todo API endpoints."""
from datetime import datetime

import pytest
from httpx import AsyncClient

from app.schemas.todo import TodoResponse


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint returns healthy status."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint returns API info."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data


class TestTodoCreateEndpoint:
    """Tests for POST /todos endpoint."""

    @pytest.mark.asyncio
    async def test_create_todo_success(self, client: AsyncClient):
        """Test successful todo creation."""
        response = await client.post(
            "/api/todos",
            json={"title": "Test todo", "description": "Test description"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test todo"
        assert data["description"] == "Test description"
        assert data["is_completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    @pytest.mark.asyncio
    async def test_create_todo_minimal(self, client: AsyncClient):
        """Test creating todo with minimal data."""
        response = await client.post(
            "/api/todos",
            json={"title": "Minimal todo"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal todo"
        assert data["description"] is None

    @pytest.mark.asyncio
    async def test_create_todo_empty_title_fails(self, client: AsyncClient):
        """Test that empty title returns 422."""
        response = await client.post(
            "/api/todos",
            json={"title": ""},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_todo_with_due_date(self, client: AsyncClient):
        """Test creating todo with due date."""
        due = "2024-12-31T23:59:00"
        response = await client.post(
            "/api/todos",
            json={"title": "Due todo", "due_at": due},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["due_at"] is not None


class TestTodoListEndpoint:
    """Tests for GET /todos endpoint."""

    @pytest.mark.asyncio
    async def test_list_todos_empty(self, client: AsyncClient):
        """Test listing todos when empty."""
        response = await client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert data["todos"] == []
        assert data["total"] == 0
        assert data["completed"] == 0
        assert data["pending"] == 0

    @pytest.mark.asyncio
    async def test_list_todos_with_data(self, client: AsyncClient):
        """Test listing todos after creating some."""
        # Create todos
        await client.post("/api/todos", json={"title": "Todo 1"})
        await client.post("/api/todos", json={"title": "Todo 2"})
        await client.post("/api/todos", json={"title": "Todo 3"})

        response = await client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 3
        assert data["total"] == 3
        assert data["completed"] == 0
        assert data["pending"] == 3

    @pytest.mark.asyncio
    async def test_list_todos_filter_completed(self, client: AsyncClient):
        """Test filtering todos by completion status."""
        await client.post("/api/todos", json={"title": "Todo 1"})
        await client.post("/api/todos", json={"title": "Todo 2"})
        await client.patch("/api/todos/1/status", json={"is_completed": True})

        # Get pending
        response = await client.get("/api/todos?completed=false")
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 1
        assert data["todos"][0]["title"] == "Todo 2"


class TestTodoGetEndpoint:
    """Tests for GET /todos/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_get_todo_success(self, client: AsyncClient):
        """Test getting a specific todo."""
        create_resp = await client.post(
            "/api/todos",
            json={"title": "Test todo"},
        )
        todo_id = create_resp.json()["id"]

        response = await client.get(f"/api/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Test todo"

    @pytest.mark.asyncio
    async def test_get_todo_not_found(self, client: AsyncClient):
        """Test getting non-existent todo returns 404."""
        response = await client.get("/api/todos/999")
        assert response.status_code == 404


class TestTodoUpdateEndpoint:
    """Tests for PUT /todos/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_update_todo_success(self, client: AsyncClient):
        """Test updating a todo."""
        create_resp = await client.post(
            "/api/todos",
            json={"title": "Original title"},
        )
        todo_id = create_resp.json()["id"]

        response = await client.put(
            f"/api/todos/{todo_id}",
            json={"title": "Updated title", "description": "New description"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["description"] == "New description"

    @pytest.mark.asyncio
    async def test_update_todo_not_found(self, client: AsyncClient):
        """Test updating non-existent todo returns 404."""
        response = await client.put(
            "/api/todos/999",
            json={"title": "Updated"},
        )
        assert response.status_code == 404


class TestTodoToggleEndpoint:
    """Tests for PATCH /todos/{id}/status endpoint."""

    @pytest.mark.asyncio
    async def test_toggle_complete_success(self, client: AsyncClient):
        """Test toggling todo completion status."""
        create_resp = await client.post(
            "/api/todos",
            json={"title": "Test todo"},
        )
        todo_id = create_resp.json()["id"]

        # Mark as complete
        response = await client.patch(
            f"/api/todos/{todo_id}/status",
            json={"is_completed": True},
        )
        assert response.status_code == 200
        assert response.json()["is_completed"] is True

        # Mark as incomplete
        response = await client.patch(
            f"/api/todos/{todo_id}/status",
            json={"is_completed": False},
        )
        assert response.status_code == 200
        assert response.json()["is_completed"] is False

    @pytest.mark.asyncio
    async def test_toggle_not_found(self, client: AsyncClient):
        """Test toggling non-existent todo returns 404."""
        response = await client.patch(
            "/api/todos/999/status",
            json={"is_completed": True},
        )
        assert response.status_code == 404


class TestTodoDeleteEndpoint:
    """Tests for DELETE /todos/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_delete_todo_success(self, client: AsyncClient):
        """Test deleting a todo."""
        create_resp = await client.post(
            "/api/todos",
            json={"title": "To delete"},
        )
        todo_id = create_resp.json()["id"]

        response = await client.delete(f"/api/todos/{todo_id}")
        assert response.status_code == 204

        # Verify deletion
        get_resp = await client.get(f"/api/todos/{todo_id}")
        assert get_resp.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_todo_not_found(self, client: AsyncClient):
        """Test deleting non-existent todo returns 404."""
        response = await client.delete("/api/todos/999")
        assert response.status_code == 404
