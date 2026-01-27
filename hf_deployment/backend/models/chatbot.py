"""Database models for the Todo App Chatbot Phase III"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, Text
from sqlalchemy import text
import json

if TYPE_CHECKING:
    from .chatbot import Conversation, Task  # Self-referencing imports for relationships


class Conversation(SQLModel, table=True):
    """Model representing a conversation between user and chatbot"""

    __tablename__ = "conversations"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Using string for flexibility with different auth systems

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('NOW()'))
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('NOW()'), onupdate=text('NOW()'))
    )

    # Relationship with messages
    messages: list["Message"] = Relationship(back_populates="conversation")
    # Relationship with tasks
    tasks: list["Task"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """Model representing a message in a conversation"""

    __tablename__ = "messages"

    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(index=True)  # Who sent the message
    role: str = Field(sa_column=Column(Text, nullable=False))  # "user", "assistant", "system", etc.
    content: str = Field(sa_column=Column(Text, nullable=False))
    tool_calls: Optional[str] = Field(default=None, sa_column=Column(Text))  # JSON string of tool calls (optional)

    # Timestamp
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('NOW()'))
    )

    # Relationship with conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")


def validate_role(v: str) -> str:
    """Validate that the role is one of the allowed values"""
    allowed_roles = {"user", "assistant", "system", "tool"}
    if v not in allowed_roles:
        raise ValueError(f"Role must be one of {allowed_roles}")
    return v


# Add validation to the Message model
Message.model_config = {"validate_assignment": True}


class Task(SQLModel, table=True):
    """Extended Task model for the Todo App Chatbot"""

    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Link task to user
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    due_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
    priority: str = Field(default="medium", max_length=20)  # low, medium, high
    category: Optional[str] = Field(default=None, max_length=50)
    status: str = Field(default="pending", max_length=20)  # pending, in_progress, completed, cancelled
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversations.id", index=True)  # Link to conversation that created it

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('NOW()'))
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('NOW()'), onupdate=text('NOW()'))
    )

    # Relationship with conversation
    conversation: Optional[Conversation] = Relationship(back_populates="tasks")