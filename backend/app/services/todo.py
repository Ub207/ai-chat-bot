from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import Todo, User
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from fastapi import HTTPException, status
from typing import List, Optional


class TodoService:
    # Public methods (without authentication)
    @staticmethod
    async def get_all_todos(db: AsyncSession, skip: int = 0, limit: int = 100) -> tuple[List[Todo], int, int, int]:
        """Get all todos with stats."""
        # Get todos
        result = await db.execute(
            select(Todo)
            .offset(skip)
            .limit(limit)
        )
        todos = list(result.scalars().all())

        # Get total count
        count_result = await db.execute(
            select(func.count(Todo.id))
        )
        total = count_result.scalar() or 0

        # Get completed count
        completed_result = await db.execute(
            select(func.count(Todo.id)).where(Todo.is_completed == True)
        )
        completed = completed_result.scalar() or 0

        # Get pending count
        pending = total - completed

        return todos, total, completed, pending

    @staticmethod
    async def get_todo_by_id_public(db: AsyncSession, todo_id: int) -> Todo:
        """Get a single todo by ID."""
        result = await db.execute(
            select(Todo).where(Todo.id == todo_id)
        )
        todo = result.scalar_one_or_none()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        return todo

    @staticmethod
    async def create_todo_public(db: AsyncSession, todo_data: TodoCreate) -> Todo:
        """Create a new todo (for demo without auth - defaults to user_id=1)."""
        # Check if user 1 exists, if not create it first
        user_result = await db.execute(select(User).where(User.id == 1))
        user = user_result.scalar_one_or_none()

        if not user:
            user = User(
                email="demo@example.com",
                username="demo_user",
                hashed_password="demo_hash",  # Not used for auth in public mode
                is_active=True
            )
            db.add(user)
            await db.flush()

        new_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            user_id=user.id
        )
        db.add(new_todo)
        await db.commit()
        await db.refresh(new_todo)
        return new_todo

    @staticmethod
    async def update_todo_public(db: AsyncSession, todo_id: int, todo_data: TodoUpdate) -> Todo:
        """Update a todo (public version)."""
        todo = await TodoService.get_todo_by_id_public(db, todo_id)

        update_data = todo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        await db.commit()
        await db.refresh(todo)
        return todo

    @staticmethod
    async def delete_todo_public(db: AsyncSession, todo_id: int) -> None:
        """Delete a todo (public version)."""
        todo = await TodoService.get_todo_by_id_public(db, todo_id)
        await db.delete(todo)
        await db.commit()

    @staticmethod
    async def toggle_todo_completion_public(db: AsyncSession, todo_id: int) -> Todo:
        """Toggle todo completion status (public version)."""
        todo = await TodoService.get_todo_by_id_public(db, todo_id)
        todo.is_completed = not todo.is_completed
        await db.commit()
        await db.refresh(todo)
        return todo

    # Authenticated methods (kept for future use)
    @staticmethod
    async def get_user_todos(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> tuple[List[Todo], int]:
        """Get all todos for a user."""
        # Get todos
        result = await db.execute(
            select(Todo)
            .where(Todo.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        todos = list(result.scalars().all())

        # Get total count
        count_result = await db.execute(
            select(func.count(Todo.id)).where(Todo.user_id == user_id)
        )
        total = count_result.scalar() or 0

        return todos, total

    @staticmethod
    async def get_todo_by_id(db: AsyncSession, todo_id: int, user_id: int) -> Todo:
        """Get a single todo by ID, ensuring it belongs to the user."""
        result = await db.execute(
            select(Todo).where(Todo.id == todo_id)
        )
        todo = result.scalar_one_or_none()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        if todo.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this todo"
            )
        return todo

    @staticmethod
    async def create_todo(db: AsyncSession, todo_data: TodoCreate, user_id: int) -> Todo:
        """Create a new todo for a user."""
        new_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            user_id=user_id
        )
        db.add(new_todo)
        await db.commit()
        await db.refresh(new_todo)
        return new_todo

    @staticmethod
    async def update_todo(db: AsyncSession, todo_id: int, todo_data: TodoUpdate, user_id: int) -> Todo:
        """Update a todo."""
        todo = await TodoService.get_todo_by_id(db, todo_id, user_id)

        update_data = todo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        await db.commit()
        await db.refresh(todo)
        return todo

    @staticmethod
    async def delete_todo(db: AsyncSession, todo_id: int, user_id: int) -> None:
        """Delete a todo."""
        todo = await TodoService.get_todo_by_id(db, todo_id, user_id)
        await db.delete(todo)
        await db.commit()

    @staticmethod
    async def toggle_todo_completion(db: AsyncSession, todo_id: int, user_id: int) -> Todo:
        """Toggle todo completion status."""
        todo = await TodoService.get_todo_by_id(db, todo_id, user_id)
        todo.is_completed = not todo.is_completed
        await db.commit()
        await db.refresh(todo)
        return todo
