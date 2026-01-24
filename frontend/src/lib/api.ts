import axios from 'axios';
import type { Todo, TodoCreate, TodoUpdate, TodoListResponse } from '@/types';

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const todoApi = {
  // Get all todos with optional filtering
  async getTodos(completed?: boolean): Promise<TodoListResponse> {
    const params = completed !== undefined ? { completed: String(completed) } : {};
    const response = await api.get('/todos', { params });
    return response.data;
  },

  // Get a single todo by ID
  async getTodo(id: number): Promise<Todo> {
    const response = await api.get(`/todos/${id}`);
    return response.data;
  },

  // Create a new todo
  async createTodo(data: TodoCreate): Promise<Todo> {
    const response = await api.post('/todos', data);
    return response.data;
  },

  // Update a todo
  async updateTodo(id: number, data: TodoUpdate): Promise<Todo> {
    const response = await api.put(`/todos/${id}`, data);
    return response.data;
  },

  // Toggle todo completion status
  async toggleTodoStatus(id: number, is_completed: boolean): Promise<Todo> {
    const response = await api.patch(`/todos/${id}/status`, { is_completed });
    return response.data;
  },

  // Delete a todo
  async deleteTodo(id: number): Promise<void> {
    await api.delete(`/todos/${id}`);
  },
};

export default api;
