"""API routes for Todo CRUD operations."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_db
from src.models.todo import Todo
from src.schemas.error import ErrorResponse, NotFoundResponse
from src.schemas.todo import (
    TodoCreate,
    TodoListResponse,
    TodoResponse,
    TodoStatusUpdate,
    TodoUpdate,
)
from src.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request data"},
    },
    summary="Create a new todo",
    description="Creates a new todo item with the provided title and optional description.",
)
async def create_todo(
    todo_data: TodoCreate,
    db: AsyncSession = Depends(get_db),
) -> Todo:
    """Create a new todo item."""
    service = TodoService(db)
    return await service.create(todo_data)


@router.get(
    "",
    response_model=TodoListResponse,
    summary="List all todos",
    description="Retrieves all todo items with optional filtering by completion status.",
)
async def list_todos(
    completed: Optional[bool] = Query(
        None,
        description="Filter by completion status (true=completed, false=pending)",
    ),
    skip: int = Query(0, ge=0, description="Number of items to skip for pagination"),
    limit: int = Query(100, ge=1, le=500, description="Maximum items to return"),
    db: AsyncSession = Depends(get_db),
) -> TodoListResponse:
    """List all todos with optional filtering and pagination."""
    service = TodoService(db)
    todos = await service.get_all(completed=completed, skip=skip, limit=limit)
    stats = await service.get_stats()

    return TodoListResponse(
        todos=todos,
        total=stats["total"],
        completed=stats["completed"],
        pending=stats["pending"],
    )


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    responses={
        404: {"model": NotFoundResponse, "description": "Todo not found"},
    },
    summary="Get a todo by ID",
    description="Retrieves a specific todo item by its unique identifier.",
)
async def get_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db),
) -> Todo:
    """Get a specific todo by ID."""
    service = TodoService(db)
    todo = await service.get_by_id(todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    return todo


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    responses={
        404: {"model": NotFoundResponse, "description": "Todo not found"},
    },
    summary="Update a todo",
    description="Updates an existing todo item with the provided data.",
)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: AsyncSession = Depends(get_db),
) -> Todo:
    """Update an existing todo."""
    service = TodoService(db)
    todo = await service.update(todo_id, todo_data)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    return todo


@router.patch(
    "/{todo_id}/status",
    response_model=TodoResponse,
    responses={
        404: {"model": NotFoundResponse, "description": "Todo not found"},
    },
    summary="Toggle todo completion",
    description="Toggles the completion status of a specific todo item.",
)
async def toggle_todo_status(
    todo_id: int,
    status_update: TodoStatusUpdate,
    db: AsyncSession = Depends(get_db),
) -> Todo:
    """Toggle the completion status of a todo."""
    service = TodoService(db)
    todo = await service.toggle_complete(todo_id, status_update.is_completed)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    return todo


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": NotFoundResponse, "description": "Todo not found"},
    },
    summary="Delete a todo",
    description="Deletes a specific todo item by its unique identifier.",
)
async def delete_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a todo item."""
    service = TodoService(db)
    deleted = await service.delete(todo_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )
