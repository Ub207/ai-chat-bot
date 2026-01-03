from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
from app.services import TodoService


router = APIRouter(tags=["Todos"])


@router.get("", response_model=TodoListResponse)
async def get_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Get all todos."""
    todos, total, completed, pending = await TodoService.get_all_todos(db, skip, limit)
    return TodoListResponse(todos=todos, total=total, completed=completed, pending=pending)


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a single todo by ID."""
    todo = await TodoService.get_todo_by_id_public(db, todo_id)
    return todo


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new todo."""
    todo = await TodoService.create_todo_public(db, todo_data)
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a todo."""
    todo = await TodoService.update_todo_public(db, todo_id, todo_data)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a todo."""
    await TodoService.delete_todo_public(db, todo_id)


@router.patch("/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Toggle todo completion status."""
    todo = await TodoService.toggle_todo_completion_public(db, todo_id)
    return todo
