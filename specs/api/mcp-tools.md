# MCP Tools Specification for Todo App Chatbot

## Overview

This specification defines 5 MCP (Model Context Protocol) tools for the Todo App Chatbot Phase III. These tools enable the AI agent to perform CRUD operations on tasks through standardized interfaces with proper validation, error handling, and user data isolation.

## Tool 1: add_task

### Purpose
Create a new task in the system with validation and user data isolation.

### Parameters
- **user_id** (required, string): Unique identifier of the user creating the task
- **title** (required, string): Title of the task (1-200 characters)
- **description** (optional, string): Optional detailed description of the task
- **priority** (optional, string): Task priority level (default: "medium", values: "low", "medium", "high")
- **due_date** (optional, string): Due date in ISO 8601 format
- **category** (optional, string): Category for organizing tasks

### Input JSON Schema
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
    }
  },
  "required": ["user_id", "title"],
  "additionalProperties": false
}
```

### Return Format
```json
{
  "task_id": "integer",
  "status": "string",
  "title": "string"
}
```

### Error Cases
- **Invalid title**: Title is empty, exceeds 200 characters, or contains invalid characters
- **Database error**: Unable to connect to database or save record
- **Unauthorized access**: user_id does not match authenticated user
- **Validation error**: Invalid input parameters

### User Data Isolation
- Only the user identified by user_id can create tasks in their own account
- System validates that user_id matches the authenticated user context

---

## Tool 2: list_tasks

### Purpose
Retrieve tasks with optional filtering and user data isolation.

### Parameters
- **user_id** (required, string): Unique identifier of the user whose tasks to retrieve
- **status** (optional, string): Filter by task status (values: "all", "pending", "in_progress", "completed", "cancelled"; default: "all")
- **limit** (optional, integer): Maximum number of tasks to return (default: 50, max: 100)
- **offset** (optional, integer): Number of tasks to skip for pagination (default: 0)
- **category** (optional, string): Filter by specific category
- **priority** (optional, string): Filter by priority level

### Input JSON Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "Unique identifier of the user whose tasks to retrieve"
    },
    "status": {
      "type": "string",
      "enum": ["all", "pending", "in_progress", "completed", "cancelled"],
      "default": "all",
      "description": "Filter by task status"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "default": 50,
      "description": "Maximum number of tasks to return"
    },
    "offset": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "description": "Number of tasks to skip for pagination"
    },
    "category": {
      "type": "string",
      "maxLength": 50,
      "description": "Filter by specific category"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "Filter by priority level"
    }
  },
  "required": ["user_id"],
  "additionalProperties": false
}
```

### Return Format
```json
{
  "tasks": [
    {
      "id": "integer",
      "title": "string",
      "description": "string",
      "status": "string",
      "priority": "string",
      "due_date": "string",
      "category": "string",
      "created_at": "string",
      "updated_at": "string"
    }
  ],
  "total_count": "integer",
  "has_more": "boolean"
}
```

### Error Cases
- **Database error**: Unable to connect to database or retrieve records
- **Unauthorized access**: user_id does not match authenticated user
- **Invalid parameters**: Invalid status value or invalid limit/offset values

### User Data Isolation
- Only returns tasks belonging to the specified user_id
- Cannot access tasks from other users
- System validates that user_id matches the authenticated user context

---

## Tool 3: complete_task

### Purpose
Mark a task as completed with validation and user data isolation.

### Parameters
- **user_id** (required, string): Unique identifier of the user owning the task
- **task_id** (required, integer): ID of the task to mark as completed

### Input JSON Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "Unique identifier of the user owning the task"
    },
    "task_id": {
      "type": "integer",
      "minimum": 1,
      "description": "ID of the task to mark as completed"
    }
  },
  "required": ["user_id", "task_id"],
  "additionalProperties": false
}
```

### Return Format
```json
{
  "task_id": "integer",
  "status": "string",
  "title": "string"
}
```

### Error Cases
- **Task not found**: task_id does not exist or does not belong to user
- **Database error**: Unable to connect to database or update record
- **Unauthorized access**: user_id does not match authenticated user
- **Invalid state**: Task is already completed or in a state that cannot be completed

### User Data Isolation
- Only allows completing tasks owned by the specified user_id
- Cannot modify tasks from other users
- System validates that user_id matches the authenticated user context

---

## Tool 4: update_task

### Purpose
Modify an existing task with validation and user data isolation.

### Parameters
- **user_id** (required, string): Unique identifier of the user owning the task
- **task_id** (required, integer): ID of the task to update
- **title** (optional, string): New title for the task (1-200 characters)
- **description** (optional, string): New description for the task
- **status** (optional, string): New status for the task
- **priority** (optional, string): New priority level
- **due_date** (optional, string): New due date in ISO 8601 format
- **category** (optional, string): New category for the task

### Input JSON Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "Unique identifier of the user owning the task"
    },
    "task_id": {
      "type": "integer",
      "minimum": 1,
      "description": "ID of the task to update"
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
  "required": ["user_id", "task_id"],
  "additionalProperties": false
}
```

### Return Format
```json
{
  "task_id": "integer",
  "status": "string",
  "title": "string"
}
```

### Error Cases
- **Task not found**: task_id does not exist or does not belong to user
- **Invalid parameters**: Invalid field values (e.g., title too long)
- **Database error**: Unable to connect to database or update record
- **Unauthorized access**: user_id does not match authenticated user

### User Data Isolation
- Only allows updating tasks owned by the specified user_id
- Cannot modify tasks from other users
- System validates that user_id matches the authenticated user context

---

## Tool 5: delete_task

### Purpose
Delete an existing task with validation and user data isolation.

### Parameters
- **user_id** (required, string): Unique identifier of the user owning the task
- **task_id** (required, integer): ID of the task to delete

### Input JSON Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
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

### Return Format
```json
{
  "task_id": "integer",
  "status": "string",
  "title": "string"
}
```

### Error Cases
- **Task not found**: task_id does not exist or does not belong to user
- **Database error**: Unable to connect to database or delete record
- **Unauthorized access**: user_id does not match authenticated user
- **Deletion protection**: Task cannot be deleted due to dependencies

### User Data Isolation
- Only allows deleting tasks owned by the specified user_id
- Cannot delete tasks from other users
- System validates that user_id matches the authenticated user context

## Common Error Response Format

All tools return errors in the following format:
```json
{
  "error": {
    "type": "string",
    "message": "string",
    "code": "string"
  }
}
```

## Common Security Requirements

- All tools must validate that the user_id parameter matches the authenticated user context
- All tools must implement proper rate limiting to prevent abuse
- All tools must sanitize input to prevent injection attacks
- All tools must log operations for audit purposes