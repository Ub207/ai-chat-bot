"""API endpoints for the Todo App Chatbot Phase III"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
from datetime import datetime
import os
import json

from backend.models.chatbot import (
    Conversation,
    Message,
    Task,
    Conversation as ConversationDB,
    Message as MessageDB,
    Task as TaskDB
)
from backend.db import get_session, init_db
from backend.utils import (
    get_user_conversations,
    get_conversation_messages,
    get_user_tasks,
    get_active_tasks,
    create_conversation,
    add_message_to_conversation,
    create_task,
    complete_task,
    delete_task
)
from backend.config import settings

# Create FastAPI app with configurable title and version
app = FastAPI(
    title="Todo App Chatbot API",
    version="0.1.0",
    debug=False  # Disable debug mode for production
)

# Configure CORS middleware
# In production, replace "*" with your actual frontend domain(s)
# Example: ["https://yourdomain.com", "https://www.yourdomain.com"]
origins = [
    "http://localhost:3000",  # Default Next.js dev server
    "http://localhost:3001",  # Alternative dev port
    "http://localhost:3002",  # Another alternative dev port
    "http://127.0.0.1:3000",  # Alternative localhost format
    "http://127.0.0.1:3001",  # Alternative localhost format
    "http://127.0.0.1:3002",  # Alternative localhost format
]

# Add production origins from environment or settings
production_origin = getattr(settings, 'FRONTEND_ORIGIN', None)
if production_origin:
    origins.append(production_origin)

# For Vercel deployments, add common Vercel patterns
vercel_origin = getattr(settings, 'VERCEL_URL', None)
if vercel_origin:
    origins.append(f"https://{vercel_origin}")

# Allow all origins in development mode, restrict in production
origins = ["*"]  # Allow all in development

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    # Expose headers that clients might need to access
    expose_headers=["Content-Disposition", "X-Total-Count"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    init_db()


# Conversation endpoints
from pydantic import BaseModel

class CreateConversationRequest(BaseModel):
    user_id: str

@app.post("/conversations/", response_model=Conversation)
def create_new_conversation(session: Session = Depends(get_session)):
    """Create a new conversation for the demo user"""
    # Use a fixed demo user_id for Hackathon-2 Phase-3
    demo_user_id = "demo_user"
    conversation = create_conversation(session, demo_user_id)
    return conversation


@app.get("/conversations", response_model=List[Conversation])
def get_user_conversations_endpoint(session: Session = Depends(get_session)):
    """Get all conversations for the demo user"""
    demo_user_id = "demo_user"
    conversations = get_user_conversations(session, demo_user_id)
    return conversations


@app.get("/conversations/{conversation_id}/messages", response_model=List[Message])
def get_conversation_messages_endpoint(conversation_id: int, session: Session = Depends(get_session)):
    """Get all messages for a conversation"""
    messages = get_conversation_messages(session, conversation_id)
    return messages


# Message endpoints
@app.post("/messages/", response_model=Message)
def add_message(
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    tool_calls: str = None,
    session: Session = Depends(get_session)
):
    """Add a message to a conversation"""
    message = add_message_to_conversation(
        session,
        conversation_id,
        user_id,
        role,
        content,
        tool_calls
    )
    return message


# Chat endpoint that processes user messages and returns AI responses
from pydantic import BaseModel

class ChatMessageRequest(BaseModel):
    message: str  # Only expect message in the request body since conversation_id is in the path

@app.post("/conversations/{conversation_id}/messages")
def chat_endpoint(
    conversation_id: int,
    request: ChatMessageRequest,
    session: Session = Depends(get_session)
):
    """Process a chat message and return an AI response"""
    from backend.utils import process_user_message
    from datetime import datetime

    # Use the demo user for Hackathon-2 Phase-3
    demo_user_id = "demo_user"

    # Validate that the message is not empty
    if not request.message or request.message.strip() == "":
        raise HTTPException(status_code=422, detail="Message content cannot be empty")

    # Add user message to conversation
    user_message = add_message_to_conversation(
        session,
        conversation_id,
        demo_user_id,
        "user",
        request.message.strip()  # Strip whitespace to avoid storage issues
    )

    # Process the message and get AI response
    ai_response = process_user_message(user_message, session)

    # Add AI response to conversation
    ai_message = add_message_to_conversation(
        session,
        conversation_id,
        demo_user_id,
        "assistant",
        ai_response.get("response", "I'm sorry, I couldn't process that."),
        json.dumps(ai_response.get("tool_calls", [])) if ai_response.get("tool_calls") else None
    )

    # Add timestamp to the response to match frontend expectations
    result = ai_response.copy()
    result["conversation_id"] = conversation_id
    result["timestamp"] = datetime.now().isoformat()

    return result


# Task endpoints
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from typing import Optional

# Define Pydantic models for request bodies with validation
class CreateTaskRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=200)  # As per MCP tools spec
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    priority: Optional[str] = "medium"
    category: Optional[str] = Field(None, max_length=50)  # As per MCP tools spec
    conversation_id: Optional[int] = None

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v and v not in ['low', 'medium', 'high']:
            raise ValueError('priority must be low, medium, or high')
        return v

class UpdateTaskRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    title: Optional[str] = Field(None, min_length=1, max_length=200)  # As per MCP tools spec
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    category: Optional[str] = Field(None, max_length=50)  # As per MCP tools spec

    @field_validator('priority', mode='before')
    @classmethod
    def validate_priority(cls, v):
        if v is not None and v not in ['low', 'medium', 'high']:
            raise ValueError('priority must be low, medium, or high')
        return v

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in ['pending', 'in_progress', 'completed', 'cancelled']:
            raise ValueError('status must be pending, in_progress, completed, or cancelled')
        return v

class DeleteTaskRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    task_id: int = Field(..., ge=1)

@app.post("/tasks/", response_model=Task)
def create_new_task_from_json(
    task_request: CreateTaskRequest,
    session: Session = Depends(get_session)
):
    """Create a new task from JSON data"""
    task = create_task(
        session,
        task_request.user_id,
        task_request.title,
        task_request.description,
        task_request.due_date,
        task_request.priority,
        task_request.category,
        task_request.conversation_id
    )
    return task

# Backward compatibility with query parameters
@app.post("/tasks/from_params", response_model=Task)
def create_new_task_from_params(
    user_id: str,
    title: str,
    description: str = None,
    due_date: datetime = None,
    priority: str = "medium",
    category: str = None,
    conversation_id: int = None,
    session: Session = Depends(get_session)
):
    """Create a new task from query parameters (for backward compatibility)"""
    task = create_task(
        session,
        user_id,
        title,
        description,
        due_date,
        priority,
        category,
        conversation_id
    )
    return task


@app.get("/tasks/{user_id}", response_model=List[Task])
def get_user_tasks_endpoint(user_id: str, session: Session = Depends(get_session)):
    """Get all tasks for a user"""
    tasks = get_user_tasks(session, user_id)
    return tasks


@app.get("/tasks/{user_id}/active", response_model=List[Task])
def get_active_tasks_endpoint(user_id: str, session: Session = Depends(get_session)):
    """Get active tasks for a user"""
    tasks = get_active_tasks(session, user_id)
    return tasks


@app.put("/tasks/{task_id}/complete", response_model=Task)
def complete_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    """Mark a task as completed"""
    task = complete_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task_endpoint(
    task_id: int,
    task_request: UpdateTaskRequest,
    session: Session = Depends(get_session)
):
    """Update an existing task from JSON data"""
    # Get the task from the database
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the user
    if task.user_id != task_request.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    # Update the fields that were provided
    if task_request.title is not None:
        task.title = task_request.title
    if task_request.description is not None:
        task.description = task_request.description
    if task_request.status is not None:
        task.status = task_request.status
    if task_request.priority is not None:
        task.priority = task_request.priority
    if task_request.due_date is not None:
        task.due_date = task_request.due_date
    if task_request.category is not None:
        task.category = task_request.category

    # Update the timestamp
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


class DeleteTaskRequest(BaseModel):
    user_id: str
    task_id: int

@app.delete("/tasks/{task_id}")
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    """Delete a task by ID (using path parameter)"""
    success = delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}

@app.post("/tasks/delete")  # Alternative endpoint that accepts JSON
def delete_task_from_json(
    delete_request: DeleteTaskRequest,
    session: Session = Depends(get_session)
):
    """Delete a task using JSON data"""
    # Get the task from the database to verify ownership
    task = session.get(Task, delete_request.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the user
    if task.user_id != delete_request.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    success = delete_task(session, delete_request.task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}


# Include health check routes
from backend.health import router as health_router
app.include_router(health_router)


if __name__ == "__main__":
    import uvicorn
    # Hugging Face Spaces uses port 7860 by default
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))