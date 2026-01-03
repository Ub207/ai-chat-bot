# Data Model: Full Stack Todo Application

**Phase**: 1 - Design
**Date**: 2025-12-31
**Status**: Approved

## Database Schema

### Primary Table: todos

```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    due_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_todos_created_at ON todos(created_at DESC);
CREATE INDEX idx_todos_is_completed ON todos(is_completed);
CREATE INDEX idx_todos_due_at ON todos(due_at) WHERE due_at IS NOT NULL;
```

## Entity Definition

### Todo Entity

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier |
| title | VARCHAR(255) | NOT NULL | Short task description |
| description | TEXT | NULLABLE | Detailed task information |
| is_completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| due_at | TIMESTAMP | NULLABLE | Optional due date/time |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last modification timestamp |

## API Schemas

### Request Schemas

**CreateTodoRequest:**
```typescript
interface CreateTodoRequest {
  title: string;      // Required, max 255 chars
  description?: string;  // Optional
}
```

**UpdateTodoRequest:**
```typescript
interface UpdateTodoRequest {
  title?: string;     // Optional, max 255 chars
  description?: string;  // Optional
  is_completed?: boolean;  // Optional
}
```

### Response Schemas

**TodoResponse:**
```typescript
interface TodoResponse {
  id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;  // ISO 8601 format
  updated_at: string;  // ISO 8601 format
}
```

**TodoListResponse:**
```typescript
interface TodoListResponse {
  success: boolean;
  data: TodoResponse[];
  total: number;
}
```

## Frontend Types

```typescript
// frontend/src/types/todo.ts

export interface Todo {
  id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTodoInput {
  title: string;
  description?: string;
}

export interface UpdateTodoInput {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}
```

## Relationships

**Single Entity Only:**

This application uses a single `todos` table with no foreign key relationships. Each todo is an independent record.

**Future Extensibility:**

The schema is designed to support future enhancements:
- User authentication: Add `user_id` foreign key
- Categories: Add `category_id` foreign key or JSONB tags column
- Due dates: Add `due_at` timestamp column
