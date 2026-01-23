# API Documentation

## Overview

The Todo App Chatbot API provides endpoints for managing conversations, tasks, and messages. The API follows REST principles with JSON responses and uses standard HTTP methods. Authentication is handled via JWT tokens passed in the Authorization header.

## Base URL

```
https://api.todo-chatbot.com/v1  # Production
http://localhost:8000            # Development
```

## Authentication

All endpoints require authentication via JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <JWT_TOKEN>
```

## Common Response Format

### Success Responses
```json
{
  "success": true,
  "data": { /* response data */ },
  "timestamp": "2026-01-13T12:00:00Z"
}
```

### Error Responses
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { /* additional error details */ }
  },
  "timestamp": "2026-01-13T12:00:00Z"
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| AUTH_001 | 401 | Invalid or missing authentication token |
| AUTH_002 | 403 | Access denied: user_id does not match authentication |
| CHAT_001 | 404 | Conversation not found or access denied |
| VALIDATION_001 | 422 | Invalid request format |
| SERVER_001 | 500 | Internal server error |

## Endpoints

### Chat Endpoint

#### POST `/api/{user_id}/chat`

Initiate or continue a conversation with the chatbot.

##### Parameters
- `user_id` (path, required): Unique identifier of the requesting user

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

##### Request Body
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

##### Request Schema
```json
{
  "type": "object",
  "properties": {
    "conversation_id": {
      "type": ["integer", "null"],
      "description": "Optional existing conversation ID, if null a new conversation will be created"
    },
    "message": {
      "type": "string",
      "minLength": 1,
      "maxLength": 10000,
      "description": "The user's message to the chatbot"
    }
  },
  "required": ["message"],
  "additionalProperties": false
}
```

##### Response Schema
```json
{
  "type": "object",
  "properties": {
    "conversation_id": {
      "type": "integer",
      "description": "The ID of the conversation (newly created or existing)"
    },
    "response": {
      "type": "string",
      "description": "The assistant's response message"
    },
    "tool_calls": {
      "type": ["array", "null"],
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "The name of the MCP tool called"
          },
          "arguments": {
            "type": "object",
            "description": "Arguments passed to the tool"
          }
        },
        "required": ["name", "arguments"]
      },
      "description": "Optional array of MCP tool calls executed"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp of the response"
    }
  },
  "required": ["conversation_id", "response", "timestamp"],
  "additionalProperties": false
}
```

##### Example Request
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 123,
    "message": "Add a task to buy groceries"
  }'
```

##### Example Response
```json
{
  "conversation_id": 123,
  "response": "I've created a task: 'buy groceries'. Is there anything else you'd like to add?",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "user123",
        "title": "buy groceries",
        "priority": "medium"
      }
    }
  ],
  "timestamp": "2026-01-13T12:00:00Z"
}
```

### Task Management Endpoints

#### POST `/tasks/`

Create a new task.

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

##### Request Body
```json
{
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "priority": "medium",
  "category": "personal",
  "due_date": "2026-01-15T10:00:00Z",
  "conversation_id": 123
}
```

##### Request Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "Unique identifier of the user creating the task"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "description": "Title of the task (1-200 characters)"
    },
    "description": {
      "type": "string",
      "maxLength": 1000,
      "description": "Optional detailed description of the task"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "default": "medium",
      "description": "Priority level of the task"
    },
    "due_date": {
      "type": "string",
      "format": "date-time",
      "description": "Due date in ISO 8601 format"
    },
    "category": {
      "type": "string",
      "maxLength": 50,
      "description": "Category for organizing tasks"
    },
    "conversation_id": {
      "type": "integer",
      "description": "ID of the conversation that created this task"
    }
  },
  "required": ["user_id", "title"],
  "additionalProperties": false
}
```

##### Response Schema
Same as the Task model response.

##### Example Request
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "priority": "medium"
  }'
```

#### GET `/tasks/{user_id}`

Retrieve all tasks for a specific user.

##### Parameters
- `user_id` (path, required): Unique identifier of the user whose tasks to retrieve

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
```

##### Query Parameters
- `status` (optional): Filter by task status ("all", "pending", "in_progress", "completed", "cancelled")
- `limit` (optional): Maximum number of tasks to return (default: 50, max: 100)
- `offset` (optional): Number of tasks to skip for pagination (default: 0)
- `category` (optional): Filter by specific category
- `priority` (optional): Filter by priority level

##### Response Schema
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {"type": "integer"},
      "title": {"type": "string"},
      "description": {"type": "string"},
      "status": {"type": "string"},
      "priority": {"type": "string"},
      "due_date": {"type": "string"},
      "category": {"type": "string"},
      "created_at": {"type": "string"},
      "updated_at": {"type": "string"}
    },
    "required": ["id", "title", "status", "priority", "created_at", "updated_at"]
  }
}
```

##### Example Request
```bash
curl -X GET "http://localhost:8000/tasks/user123?status=pending&priority=high" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### PUT `/tasks/{task_id}`

Update an existing task.

##### Parameters
- `task_id` (path, required): ID of the task to update

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

##### Request Body
```json
{
  "user_id": "user123",
  "title": "Updated task title",
  "priority": "high",
  "status": "in_progress"
}
```

##### Request Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "Unique identifier of the user owning the task"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "description": "New title for the task"
    },
    "description": {
      "type": "string",
      "maxLength": 1000,
      "description": "New description for the task"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "in_progress", "completed", "cancelled"],
      "description": "New status for the task"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "New priority level"
    },
    "due_date": {
      "type": "string",
      "format": "date-time",
      "description": "New due date in ISO 8601 format"
    },
    "category": {
      "type": "string",
      "maxLength": 50,
      "description": "New category for the task"
    }
  },
  "required": ["user_id"],
  "additionalProperties": false
}
```

##### Example Request
```bash
curl -X PUT "http://localhost:8000/tasks/456" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "priority": "high",
    "status": "in_progress"
  }'
```

#### PUT `/tasks/{task_id}/complete`

Mark a task as completed.

##### Parameters
- `task_id` (path, required): ID of the task to mark as completed

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
```

##### Example Request
```bash
curl -X PUT "http://localhost:8000/tasks/456/complete" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### DELETE `/tasks/{task_id}`

Delete a task by ID.

##### Parameters
- `task_id` (path, required): ID of the task to delete

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
```

##### Example Request
```bash
curl -X DELETE "http://localhost:8000/tasks/456" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### POST `/tasks/delete`

Alternative endpoint to delete a task using JSON data.

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

##### Request Body
```json
{
  "user_id": "user123",
  "task_id": 456
}
```

##### Request Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "minLength": 1,
      "description": "Unique identifier of the user owning the task"
    },
    "task_id": {
      "type": "integer",
      "minimum": 1,
      "description": "ID of the task to delete"
    }
  },
  "required": ["user_id", "task_id"],
  "additionalProperties": false
}
```

##### Example Request
```bash
curl -X POST "http://localhost:8000/tasks/delete" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "task_id": 456
  }'
```

### Conversation Management Endpoints

#### POST `/conversations/`

Create a new conversation.

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
```

##### Query Parameters
- `user_id` (required): Unique identifier of the user creating the conversation

##### Example Request
```bash
curl -X POST "http://localhost:8000/conversations/?user_id=user123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### GET `/conversations/{user_id}`

Retrieve all conversations for a specific user.

##### Parameters
- `user_id` (path, required): Unique identifier of the user whose conversations to retrieve

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
```

##### Example Request
```bash
curl -X GET "http://localhost:8000/conversations/user123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Message Management Endpoints

#### POST `/messages/`

Add a message to a conversation.

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
```

##### Query Parameters
- `conversation_id` (required): ID of the conversation
- `user_id` (required): ID of the user sending the message
- `role` (required): Role of the message sender ("user", "assistant", "system", "tool")
- `content` (required): Content of the message
- `tool_calls` (optional): JSON string of tool calls (if any)

##### Example Request
```bash
curl -X POST "http://localhost:8000/messages/?conversation_id=123&user_id=user123&role=user&content=Hello%20there!" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### GET `/conversations/{conversation_id}/messages`

Retrieve all messages for a specific conversation.

##### Parameters
- `conversation_id` (path, required): ID of the conversation

##### Headers
```
Authorization: Bearer <JWT_TOKEN>
```

##### Example Request
```bash
curl -X GET "http://localhost:8000/conversations/123/messages" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Health Check Endpoint

#### GET `/health`

Check the health status of the API.

##### Example Request
```bash
curl -X GET "http://localhost:8000/health"
```

##### Example Response
```json
{
  "status": "healthy",
  "timestamp": "2026-01-13T12:00:00Z"
}
```

## Rate Limiting

All API endpoints are subject to rate limiting:

- **Authenticated users**: 1000 requests per hour per user
- **Unauthenticated requests**: 100 requests per hour per IP
- **Burst allowance**: 10 requests per minute

Exceeding rate limits will result in a `429 Too Many Requests` response.

## Response Time Expectations

- **Simple operations** (GET, simple POST): < 200ms (p95)
- **Complex operations** (with database queries): < 500ms (p95)
- **MCP tool calls**: < 2000ms (p95)

## CORS Policy

The API implements strict CORS policies allowing requests only from:
- `https://yourdomain.com`
- `http://localhost:3000` (development)

## Security Headers

All responses include security headers:
- `Strict-Transport-Security`: Enforces HTTPS
- `X-Content-Type-Options`: Prevents MIME type sniffing
- `X-Frame-Options`: Prevents clickjacking
- `X-XSS-Protection`: Enables browser XSS protection