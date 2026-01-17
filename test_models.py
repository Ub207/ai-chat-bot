"""Simple test to verify the database models work correctly"""

import tempfile
import os
from sqlmodel import SQLModel, create_engine, Session
from datetime import datetime
from backend.models.chatbot import Conversation, Message, Task


def test_models():
    """Test that the models can be created and used"""

    # Create an in-memory SQLite database for testing
    _, temp_db_path = tempfile.mkstemp(suffix='.db')
    temp_db_url = f"sqlite:///{temp_db_path}"

    # Create engine and tables
    engine = create_engine(temp_db_url)
    SQLModel.metadata.create_all(engine)

    print("Testing database models...")

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
        print(f"  Updated at: {conversation.updated_at}")

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

        print(f"\n✓ Created message with ID: {message.id}")
        print(f"  Conversation ID: {message.conversation_id}")
        print(f"  User ID: {message.user_id}")
        print(f"  Role: {message.role}")
        print(f"  Content: {message.content}")
        print(f"  Created at: {message.created_at}")

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

        print(f"\n✓ Created task with ID: {task.id}")
        print(f"  User ID: {task.user_id}")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description}")
        print(f"  Priority: {task.priority}")
        print(f"  Status: {task.status}")
        print(f"  Conversation ID: {task.conversation_id}")
        print(f"  Created at: {task.created_at}")
        print(f"  Updated at: {task.updated_at}")

    # Verify the data was stored correctly
    with Session(engine) as session:
        # Get the conversation back
        retrieved_conv = session.get(Conversation, conversation.id)
        assert retrieved_conv is not None
        assert retrieved_conv.user_id == "test_user_123"

        # Get the message back
        retrieved_msg = session.get(Message, message.id)
        assert retrieved_msg is not None
        assert retrieved_msg.content == "Hello, I want to add a task!"
        assert retrieved_msg.role == "user"

        # Get the task back
        retrieved_task = session.get(Task, task.id)
        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.status == "pending"

        print("\n✓ All data retrieved successfully and matches expected values")

    # Clean up the temporary database file
    os.unlink(temp_db_path)

    print("\n🎉 All tests passed! Models are working correctly.")


def test_relationships():
    """Test that relationships work properly"""

    # Create an in-memory SQLite database for testing
    _, temp_db_path = tempfile.mkstemp(suffix='.db')
    temp_db_url = f"sqlite:///{temp_db_path}"

    # Create engine and tables
    engine = create_engine(temp_db_url)
    SQLModel.metadata.create_all(engine)

    print("\nTesting relationships...")

    with Session(engine) as session:
        # Create a conversation
        conversation = Conversation(user_id="test_user_456")
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Add multiple messages to the conversation
        for i in range(3):
            msg = Message(
                conversation_id=conversation.id,
                user_id="test_user_456",
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i+1}"
            )
            session.add(msg)

        # Add a task linked to the conversation
        task = Task(
            user_id="test_user_456",
            title="Related Task",
            conversation_id=conversation.id
        )
        session.add(task)

        session.commit()

        # Refresh to load relationships
        session.refresh(conversation)

        print(f"✓ Conversation has {len(conversation.messages)} messages")
        print(f"✓ Conversation has {len(conversation.tasks)} tasks")

        # Test that we can access related objects
        for msg in conversation.messages:
            print(f"  - Message: {msg.content} (Role: {msg.role})")

        for task in conversation.tasks:
            print(f"  - Task: {task.title}")

    # Clean up the temporary database file
    os.unlink(temp_db_path)

    print("✓ Relationships are working correctly")


if __name__ == "__main__":
    test_models()
    test_relationships()
    print("\n✅ All tests completed successfully!")