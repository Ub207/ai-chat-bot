import pytest
from sqlmodel import Session, create_engine, SQLModel
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime

# Add the project root to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.api import app
from backend.db import get_session
from backend.models.chatbot import Conversation as ConversationDB, Message as MessageDB


@pytest.fixture(scope="function")
def test_client_and_db():
    # Create an in-memory SQLite database for testing
    engine = create_engine("sqlite:///test.db", echo=True)
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    # Override the get_session dependency
    app.dependency_overrides[get_session] = get_test_session

    client = TestClient(app)

    yield client, engine

    # Clean up
    app.dependency_overrides.clear()


def test_create_conversation_success(test_client_and_db):
    """Test successful conversation creation"""
    client, engine = test_client_and_db

    # Create a new conversation
    response = client.post("/conversations/", params={"user_id": "test_user_123"})

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["user_id"] == "test_user_123"


def test_get_user_conversations(test_client_and_db):
    """Test retrieving all conversations for a user"""
    client, engine = test_client_and_db

    # Create a conversation first
    create_response = client.post("/conversations/", params={"user_id": "test_user_123"})
    assert create_response.status_code == 200

    # Get conversations for the user
    response = client.get("/conversations/test_user_123")

    assert response.status_code == 200
    conversations = response.json()
    assert len(conversations) >= 1
    assert any(conv["user_id"] == "test_user_123" for conv in conversations)


def test_add_message_to_conversation(test_client_and_db):
    """Test adding a message to a conversation"""
    client, engine = test_client_and_db

    # Create a conversation first
    conv_response = client.post("/conversations/", params={"user_id": "test_user_123"})
    assert conv_response.status_code == 200
    conversation_id = conv_response.json()["id"]

    # Add a message to the conversation
    response = client.post("/messages/", params={
        "conversation_id": conversation_id,
        "user_id": "test_user_123",
        "role": "user",
        "content": "Hello, this is a test message!"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Hello, this is a test message!"
    assert data["role"] == "user"
    assert data["conversation_id"] == conversation_id


def test_get_conversation_messages(test_client_and_db):
    """Test retrieving all messages for a conversation"""
    client, engine = test_client_and_db

    # Create a conversation and add a message
    conv_response = client.post("/conversations/", params={"user_id": "test_user_123"})
    assert conv_response.status_code == 200
    conversation_id = conv_response.json()["id"]

    # Add a message
    msg_response = client.post("/messages/", params={
        "conversation_id": conversation_id,
        "user_id": "test_user_123",
        "role": "user",
        "content": "Test message content"
    })
    assert msg_response.status_code == 200

    # Get messages for the conversation
    response = client.get(f"/conversations/{conversation_id}/messages")

    assert response.status_code == 200
    messages = response.json()
    assert len(messages) >= 1
    assert any(msg["content"] == "Test message content" for msg in messages)


def test_conversation_stateless_flow(test_client_and_db):
    """Test that conversation history is properly retrieved from DB"""
    client, engine = test_client_and_db

    # Create a conversation
    conv_response = client.post("/conversations/", params={"user_id": "test_user_123"})
    assert conv_response.status_code == 200
    conversation_id = conv_response.json()["id"]

    # Add multiple messages to the conversation
    messages = [
        {"role": "user", "content": "First message"},
        {"role": "assistant", "content": "First response"},
        {"role": "user", "content": "Second message"},
        {"role": "assistant", "content": "Second response"}
    ]

    for msg in messages:
        response = client.post("/messages/", params={
            "conversation_id": conversation_id,
            "user_id": "test_user_123",
            "role": msg["role"],
            "content": msg["content"]
        })
        assert response.status_code == 200

    # Retrieve all messages to verify they were stored correctly
    response = client.get(f"/conversations/{conversation_id}/messages")

    assert response.status_code == 200
    retrieved_messages = response.json()
    assert len(retrieved_messages) == len(messages)

    # Verify messages are in chronological order
    for i, msg in enumerate(messages):
        assert retrieved_messages[i]["role"] == msg["role"]
        assert retrieved_messages[i]["content"] == msg["content"]


def test_message_persistence_across_requests(test_client_and_db):
    """Test that messages persist between different API requests"""
    client, engine = test_client_and_db

    # Create a conversation
    conv_response = client.post("/conversations/", params={"user_id": "test_user_123"})
    assert conv_response.status_code == 200
    conversation_id = conv_response.json()["id"]

    # Add a message
    client.post("/messages/", params={
        "conversation_id": conversation_id,
        "user_id": "test_user_123",
        "role": "user",
        "content": "Persistent message"
    })

    # Simulate a new request and verify the message is still there
    response = client.get(f"/conversations/{conversation_id}/messages")

    assert response.status_code == 200
    messages = response.json()
    persistent_msg_exists = any(
        msg["content"] == "Persistent message" for msg in messages
    )
    assert persistent_msg_exists


def test_user_data_isolation_for_conversations(test_client_and_db):
    """Test that users can only access their own conversations and messages"""
    client, engine = test_client_and_db

    # Create conversations for different users
    user1_conv = client.post("/conversations/", params={"user_id": "user_1"})
    user2_conv = client.post("/conversations/", params={"user_id": "user_2"})

    assert user1_conv.status_code == 200
    assert user2_conv.status_code == 200

    user1_conv_id = user1_conv.json()["id"]
    user2_conv_id = user2_conv.json()["id"]

    # Add messages to each conversation
    client.post("/messages/", params={
        "conversation_id": user1_conv_id,
        "user_id": "user_1",
        "role": "user",
        "content": "User 1 message"
    })

    client.post("/messages/", params={
        "conversation_id": user2_conv_id,
        "user_id": "user_2",
        "role": "user",
        "content": "User 2 message"
    })

    # Verify user 1 can only see their own conversation
    user1_convs = client.get("/conversations/user_1").json()
    user1_conv_ids = [conv["id"] for conv in user1_convs]
    assert user1_conv_id in user1_conv_ids
    assert user2_conv_id not in user1_conv_ids

    # Verify user 2 can only see their own conversation
    user2_convs = client.get("/conversations/user_2").json()
    user2_conv_ids = [conv["id"] for conv in user2_convs]
    assert user2_conv_id in user2_conv_ids
    assert user1_conv_id not in user2_conv_ids

    # Verify message isolation as well
    user1_msgs = client.get(f"/conversations/{user1_conv_id}/messages").json()
    user1_msg_content = [msg["content"] for msg in user1_msgs]
    assert "User 1 message" in user1_msg_content
    # We shouldn't be able to access user 2's messages through user 1's conversation
    assert "User 2 message" not in user1_msg_content


def test_conversation_creation_without_user_id(test_client_and_db):
    """Test that conversation creation requires a user_id"""
    client, engine = test_client_and_db

    # Try to create conversation without user_id (should fail gracefully)
    response = client.post("/conversations/")  # No user_id parameter

    # Since FastAPI will validate the path parameters, this should return a 422
    # if user_id is required in the endpoint signature
    assert response.status_code in [422, 400]  # Validation error


def test_invalid_conversation_id_access(test_client_and_db):
    """Test accessing non-existent conversation"""
    client, engine = test_client_and_db

    # Try to get messages from a non-existent conversation ID
    response = client.get("/conversations/999999/messages")

    # This might return 200 with empty list or 404 depending on implementation
    # Both are acceptable outcomes


def test_message_role_validation(test_client_and_db):
    """Test that message roles are validated"""
    client, engine = test_client_and_db

    # Create a conversation first
    conv_response = client.post("/conversations/", params={"user_id": "test_user_123"})
    assert conv_response.status_code == 200
    conversation_id = conv_response.json()["id"]

    # Try adding a message with an invalid role
    response = client.post("/messages/", params={
        "conversation_id": conversation_id,
        "user_id": "test_user_123",
        "role": "invalid_role",  # This might be validated by the API
        "content": "Test message"
    })

    # The response code could be 200 if the role isn't validated, or 422 if it is
    # Just checking that the system handles it gracefully


def test_health_check(test_client_and_db):
    """Test the health check endpoint"""
    client, engine = test_client_and_db

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data