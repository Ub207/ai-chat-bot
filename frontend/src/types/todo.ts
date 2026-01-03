export interface Todo {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  priority: number;
  user_id: number;
  created_at: string | null;
  updated_at: string | null;
}

export interface TodoCreate {
  title: string;
  description?: string;
  priority?: number;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
  priority?: number;
}

export interface TodoListResponse {
  todos: Todo[];
  total: number;
  completed: number;
  pending: number;
}

export interface TodoStats {
  total: number;
  completed: number;
  pending: number;
}
