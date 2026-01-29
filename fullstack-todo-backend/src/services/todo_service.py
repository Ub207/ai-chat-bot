"""Todo service layer containing business logic."""
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.todo import Todo
from src.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    """Service class for Todo business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize with database session."""
        self.db = db

    async def create(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo item."""
        todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            is_completed=todo_data.is_completed,
            due_at=todo_data.due_at,
        )
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get a todo item by ID."""
        result = await self.db.execute(
            select(Todo).where(Todo.id == todo_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        completed: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Todo]:
        """Get all todo items with optional filtering and pagination."""
        query = select(Todo)

        if completed is not None:
            query = query.where(Todo.is_completed == completed)

        query = query.offset(skip).limit(limit).order_by(Todo.created_at.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_stats(self) -> dict:
        """Get todo statistics."""
        total_result = await self.db.execute(select(func.count(Todo.id)))
        completed_result = await self.db.execute(
            select(func.count(Todo.id)).where(Todo.is_completed == True)
        )
        pending_result = await self.db.execute(
            select(func.count(Todo.id)).where(Todo.is_completed == False)
        )

        return {
            "total": total_result.scalar() or 0,
            "completed": completed_result.scalar() or 0,
            "pending": pending_result.scalar() or 0,
        }

    async def update(self, todo_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
        """Update an existing todo item."""
        todo = await self.get_by_id(todo_id)
        if not todo:
            return None

        update_data = todo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def delete(self, todo_id: int) -> bool:
        """Delete a todo item."""
        todo = await self.get_by_id(todo_id)
        if not todo:
            return False

        await self.db.delete(todo)
        await self.db.commit()
        return True

    async def toggle_complete(self, todo_id: int, is_completed: bool) -> Optional[Todo]:
        """Toggle the completion status of a todo item."""
        todo = await self.get_by_id(todo_id)
        if not todo:
            return None

        todo.is_completed = is_completed
        await self.db.commit()
        await self.db.refresh(todo)
        return todo
