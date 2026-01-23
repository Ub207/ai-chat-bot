"""Database setup and initialization for the Todo App Chatbot Phase III"""

import logging
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import text
from typing import Generator
from contextlib import contextmanager
import os
from backend.models.chatbot import Conversation, Message, Task
from backend.config import settings

# Configure logger
logger = logging.getLogger(__name__)

# Database configuration
# Use the database URL from settings instead of directly from environment
DATABASE_URL = settings.database_url

# Validate that DATABASE_URL is set
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set. Please configure your database connection.")
    raise ValueError("DATABASE_URL environment variable is required for the application to run.")

# Create engine
engine = create_engine(DATABASE_URL, echo=(settings.app_env.lower() == "development"))


def create_db_and_tables():
    """Create database tables if they don't exist"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session


@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """Initialize the database with required tables"""
    logger.info("Initializing database...")

    # Create all tables
    SQLModel.metadata.create_all(engine)

    logger.info("Database initialized successfully!")


def run_migrations():
    """Run database migrations (placeholder for alembic integration)"""
    logger.info("Running database migrations...")

    # In a real application, you'd use Alembic here
    # For now, we'll just ensure tables exist
    SQLModel.metadata.create_all(engine)

    logger.info("Migrations completed!")


# Example usage functions
def create_sample_conversation(user_id: str) -> Conversation:
    """Create a sample conversation for testing"""
    from .models.chatbot import Conversation

    conversation = Conversation(
        user_id=user_id
    )

    with get_db_session() as session:
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    return conversation


def create_sample_message(conversation_id: int, user_id: str, role: str, content: str) -> Message:
    """Create a sample message for testing"""
    from .models.chatbot import Message

    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )

    with get_db_session() as session:
        session.add(message)
        session.commit()
        session.refresh(message)

    return message


def create_sample_task(user_id: str, title: str, description: str = None) -> Task:
    """Create a sample task for testing"""
    from .models.chatbot import Task

    task = Task(
        user_id=user_id,
        title=title,
        description=description
    )

    with get_db_session() as session:
        session.add(task)
        session.commit()
        session.refresh(task)

    return task


# Test the models
if __name__ == "__main__":
    # Initialize database
    init_db()

    # Create sample data
    conv = create_sample_conversation("test_user_123")
    logger.info(f"Created conversation: {conv.id}")

    msg = create_sample_message(conv.id, "test_user_123", "user", "Hello, I want to add a task!")
    logger.info(f"Created message: {msg.id}")

    task = create_sample_task("test_user_123", "Buy groceries", "Need to buy milk and bread")
    logger.info(f"Created task: {task.id}")

    logger.info("Sample data created successfully!")