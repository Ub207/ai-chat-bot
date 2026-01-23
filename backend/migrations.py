"""Database migration script for Todo App Chatbot Phase III"""

import logging
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text
import os
from backend.models.chatbot import Conversation, Message, Task

# Configure logger
logger = logging.getLogger(__name__)


def get_engine():
    """Get database engine"""
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://username:password@localhost:5432/todo_chatbot"
    )
    return create_engine(DATABASE_URL)


def migrate_database():
    """Run database migrations"""
    engine = get_engine()

    logger.info("Starting database migration...")

    # Create all tables defined in the models
    SQLModel.metadata.create_all(engine)

    logger.info("Tables created/updated successfully!")

    # Add any custom migration logic here
    with engine.connect() as conn:
        # Example of custom migration - add indexes if needed
        # Check if indexes exist and create if not

        # Index for user_id in conversations table
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_conversations_user_id
                ON conversations (user_id);
            """))
        except Exception as e:
            logger.error(f"Error creating conversation user_id index: {e}")

        # Index for conversation_id in messages table
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_messages_conversation_id
                ON messages (conversation_id);
            """))
        except Exception as e:
            logger.error(f"Error creating message conversation_id index: {e}")

        # Index for user_id in messages table
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_messages_user_id
                ON messages (user_id);
            """))
        except Exception as e:
            logger.error(f"Error creating message user_id index: {e}")

        # Index for conversation_id in tasks table
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_tasks_conversation_id
                ON tasks (conversation_id);
            """))
        except Exception as e:
            logger.error(f"Error creating task conversation_id index: {e}")

        # Index for user_id in tasks table
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_tasks_user_id
                ON tasks (user_id);
            """))
        except Exception as e:
            logger.error(f"Error creating task user_id index: {e}")

        # Index for status in tasks table
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_tasks_status
                ON tasks (status);
            """))
        except Exception as e:
            logger.error(f"Error creating task status index: {e}")

        # Index for due_date in tasks table
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_tasks_due_date
                ON tasks (due_date);
            """))
        except Exception as e:
            logger.error(f"Error creating task due_date index: {e}")

        conn.commit()

    logger.info("All migrations completed successfully!")


def rollback_migration():
    """Rollback database migrations (use with caution!)"""
    logger.warning("Rolling back database migrations...")

    # WARNING: This will drop all tables - use with extreme caution!
    # In production, you should implement proper rollback mechanisms

    engine = get_engine()

    # Reflect existing tables
    from sqlalchemy import MetaData
    meta = MetaData()
    meta.reflect(bind=engine)

    # Drop all tables (be very careful!)
    for table in reversed(meta.sorted_tables):
        logger.warning(f"Dropping table: {table.name}")
        table.drop(engine)

    logger.info("Rollback completed!")


def check_db_connection():
    """Test database connection"""
    engine = get_engine()

    try:
        with engine.connect() as conn:
            # Test connection
            result = conn.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def seed_sample_data():
    """Seed the database with sample data"""
    from .db import create_sample_conversation, create_sample_message, create_sample_task

    logger.info("Seeding sample data...")

    # Create sample conversation
    conv = create_sample_conversation("sample_user_123")
    logger.info(f"Created sample conversation: {conv.id}")

    # Create sample messages
    msg1 = create_sample_message(conv.id, "sample_user_123", "user", "Hi, I want to add a task.")
    logger.info(f"Created sample message: {msg1.id}")

    msg2 = create_sample_message(conv.id, "assistant", "assistant", "Sure, what task would you like to add?")
    logger.info(f"Created sample message: {msg2.id}")

    # Create sample task
    task = create_sample_task("sample_user_123", "Complete project proposal", "Finish the project proposal document and send it to the team")
    logger.info(f"Created sample task: {task.id}")

    # Link task to conversation
    from .models.chatbot import Task
    from sqlmodel import Session

    engine = get_engine()
    with Session(engine) as session:
        db_task = session.get(Task, task.id)
        db_task.conversation_id = conv.id
        session.add(db_task)
        session.commit()

    logger.info("Sample data seeding completed!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "migrate":
            migrate_database()
        elif command == "rollback":
            confirm = input("Are you sure you want to rollback all migrations? This will delete all data! (yes/no): ")
            if confirm.lower() == "yes":
                rollback_migration()
            else:
                logger.info("Rollback cancelled.")
        elif command == "seed":
            if check_db_connection():
                seed_sample_data()
            else:
                logger.error("Cannot seed data - database connection failed.")
        elif command == "check":
            check_db_connection()
        else:
            logger.info("Usage: python migrations.py [migrate|rollback|seed|check]")
            logger.info("  migrate - Create/update database tables")
            logger.info("  rollback - Drop all tables (DANGEROUS)")
            logger.info("  seed - Add sample data to the database")
            logger.info("  check - Test database connection")
    else:
        logger.info("Usage: python migrations.py [migrate|rollback|seed|check]")
        logger.info("Run 'python migrations.py migrate' to create/update tables")