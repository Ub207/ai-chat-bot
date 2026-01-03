# API Contracts: Todo Endpoints

**Phase**: 1 - Design
**Date**: 2025-12-31
**Status**: Approved

## Base URL

```
Development: http://localhost:8000/api
Production:  https://api.yourdomain.com/api
```

## Endpoints

### GET /api/todos

Retrieve all todos.

**Request:**
```http
GET /api/todos HTTP/1.1
Host: localhost:8000
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, bread, eggs",
      "is_completed": false,
      "created_at": "2025-12-31T10:00:00Z",
      "updated_at": "2025-12-31T10:00:00Z"
    }
  ],
  "total": 1
}
```

---

### POST /api/todos

Create a new todo.

**Request:**
```http
POST /api/todos HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs"
}
```

**Validation Rules:**
- `title`: Required, 1-255 characters
- `description`: Optional, max 2000 characters

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "is_completed": false,
    "created_at": "2025-12-31T10:00:00Z",
    "updated_at": "2025-12-31T10:00:00Z"
  },
  "message": "Todo created successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Validation error",
  "details": {
    "title": ["Field required"]
  }
}
```

---

### GET /api/todos/{id}

Retrieve a single todo by ID.

**Request:**
```http
GET /api/todos/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "is_completed": false,
    "created_at": "2025-12-31T10:00:00Z",
    "updated_at": "2025-12-31T10:00:00Z"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Todo not found"
}
```

---

### PUT /api/todos/{id}

Update an existing todo.

**Request:**
```http
PUT /api/todos/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "title": "Buy groceries and snacks",
  "is_completed": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries and snacks",
    "description": "Milk, bread, eggs",
    "is_completed": true,
    "created_at": "2025-12-31T10:00:00Z",
    "updated_at": "2025-12-31T10:30:00Z"
  },
  "message": "Todo updated successfully"
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Todo not found"
}
```

---

### DELETE /api/todos/{id}

Delete a todo (hard delete).

**Request:**
```http
DELETE /api/todos/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Todo deleted successfully"
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Todo not found"
}
```

---

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid input data |
| 404 | Not Found | Resource does not exist |
| 500 | Internal Server Error | Server error |

## Health Check

### GET /health

Check API health status.

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-31T10:00:00Z"
}
```
