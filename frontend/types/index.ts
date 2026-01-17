// Type definitions for the Todo Chatbot application

export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface Conversation {
  id: number;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id?: number;
  conversation_id: number;
  user_id: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  tool_calls?: ToolCall[] | null;
  created_at: string;
}

export interface ToolCall {
  name: string;
  arguments: Record<string, any>;
}

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  due_date?: string;
  priority: 'low' | 'medium' | 'high';
  category?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  conversation_id?: number;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
  timestamp: string;
}

export interface ChatRequest {
  conversation_id: number | null;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls?: ToolCall[] | null;
  timestamp: string;
}