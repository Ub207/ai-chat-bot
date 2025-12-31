from sqlalchemy.orm import Session
from app.models import Todo, User
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from fastapi import HTTPException, status
from typing import List, Optional


class TodoService:
    @staticmethod
    def get_user_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> tuple[List[Todo], int]:
        """Get all todos for a user."""
        todos = db.query(Todo).filter(Todo.user_id == user_id).offset(skip).limit(limit).all()
        total = db.query(Todo).filter(Todo.user_id == user_id).count()
        return todos, total

    @staticmethod
    def get_todo_by_id(db: Session, todo_id: int, user_id: int) -> Todo:
        """Get a single todo by ID, ensuring it belongs to the user."""
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
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
    def create_todo(db: Session, todo_data: TodoCreate, user_id: int) -> Todo:
        """Create a new todo for a user."""
        new_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            user_id=user_id
        )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo

    @staticmethod
    def update_todo(db: Session, todo_id: int, todo_data: TodoUpdate, user_id: int) -> Todo:
        """Update a todo."""
        todo = TodoService.get_todo_by_id(db, todo_id, user_id)

        update_data = todo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        db.commit()
        db.refresh(todo)
        return todo

    @staticmethod
    def delete_todo(db: Session, todo_id: int, user_id: int) -> None:
        """Delete a todo."""
        todo = TodoService.get_todo_by_id(db, todo_id, user_id)
        db.delete(todo)
        db.commit()

    @staticmethod
    def toggle_todo_completion(db: Session, todo_id: int, user_id: int) -> Todo:
        """Toggle todo completion status."""
        todo = TodoService.get_todo_by_id(db, todo_id, user_id)
        todo.is_completed = not todo.is_completed
        db.commit()
        db.refresh(todo)
        return todo
