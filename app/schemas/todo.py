from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: Optional[str] = None
    priority: int = 0  # 0: Low, 1: Medium, 2: High


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[int] = None


class TodoResponse(TodoBase):
    id: int
    is_completed: bool
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TodoListResponse(BaseModel):
    todos: list[TodoResponse]
    total: int
    completed: int = 0
    pending: int = 0
