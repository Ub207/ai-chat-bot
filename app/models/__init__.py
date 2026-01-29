from sqlalchemy.orm import relationship
from app.models.user import User
from app.models.todo import Todo

# Add relationship to User model
User.todos = relationship("Todo", back_populates="owner")

__all__ = ["User", "Todo"]
