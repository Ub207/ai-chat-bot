"""Pydantic schemas for Todo validation and serialization."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    """Base schema with common Todo fields."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the todo item",
    )
    description: Optional[str] = Field(
        None,
        description="Detailed description of the todo item",
    )
    is_completed: bool = Field(
        default=False,
        description="Whether the todo item is completed",
    )
    due_at: Optional[datetime] = Field(
        None,
        description="Due date and time for the todo item",
    )


class TodoCreate(TodoBase):
    """Schema for creating a new Todo."""

    pass


class TodoUpdate(BaseModel):
    """Schema for updating an existing Todo."""

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated title of the todo item",
    )
    description: Optional[str] = Field(
        None,
        description="Updated description of the todo item",
    )
    is_completed: Optional[bool] = Field(
        None,
        description="Updated completion status",
    )
    due_at: Optional[datetime] = Field(
        None,
        description="Updated due date and time",
    )


class TodoResponse(TodoBase):
    """Schema for Todo response data."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TodoListResponse(BaseModel):
    """Schema for list of todos response."""

    todos: list[TodoResponse]
    total: int
    completed: int
    pending: int


class TodoStatusUpdate(BaseModel):
    """Schema for toggling todo completion status."""

    is_completed: bool = Field(
        ...,
        description="New completion status",
    )
