"""Simple test to verify the database models work correctly"""

import tempfile
import os
from sqlmodel import SQLModel, create_engine, Session
from datetime import datetime
from backend.models.chatbot import Conversation, Message, Task


def test_basic_creation():
    """Test that the models can be created and used"""

    # Create an in-memory SQLite database for testing
    _, temp_db_path = tempfile.mkstemp(suffix='.db')
    temp_db_url = f"sqlite:///{temp_db_path}"

    # Create engine and tables
    engine = create_engine(temp_db_url)
    SQLModel.metadata.create_all(engine)

    print("Testing basic model creation...")

    # Test Conversation model
    with Session(engine) as session:
        # Create a conversation
        conversation = Conversation(
            user_id="test_user_123"
        )

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        print(f"✓ Created conversation with ID: {conversation.id}")
        print(f"  User ID: {conversation.user_id}")
        print(f"  Created at: {conversation.created_at}")

        # Create a message
        message = Message(
            conversation_id=conversation.id,
            user_id="test_user_123",
            role="user",
            content="Hello, I want to add a task!"
        )

        session.add(message)
        session.commit()
        session.refresh(message)

        print(f"✓ Created message with ID: {message.id}")
        print(f"  Conversation ID: {message.conversation_id}")
        print(f"  Content: {message.content}")

        # Create a task
        task = Task(
            user_id="test_user_123",
            title="Test Task",
            description="This is a test task",
            priority="high",
            status="pending",
            conversation_id=conversation.id
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        print(f"✓ Created task with ID: {task.id}")
        print(f"  Title: {task.title}")
        print(f"  Status: {task.status}")

        # Verify data was stored correctly
        retrieved_conv = session.get(Conversation, conversation.id)
        assert retrieved_conv is not None
        assert retrieved_conv.user_id == "test_user_123"

        retrieved_msg = session.get(Message, message.id)
        assert retrieved_msg is not None
        assert retrieved_msg.content == "Hello, I want to add a task!"

        retrieved_task = session.get(Task, task.id)
        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"

        print("✓ All data retrieved successfully and matches expected values")

    # Clean up the temporary database file
    os.unlink(temp_db_path)

    print("\n🎉 All basic tests passed! Models are working correctly.")


if __name__ == "__main__":
    test_basic_creation()
    print("\n✅ All tests completed successfully!")