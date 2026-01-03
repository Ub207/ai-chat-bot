import { create } from 'zustand';
import type { Todo, TodoStats } from '@/types';
import { todoApi } from './api';

interface TodoState {
  todos: Todo[];
  stats: TodoStats;
  loading: boolean;
  error: string | null;

  // Actions
  fetchTodos: (completed?: boolean) => Promise<void>;
  createTodo: (title: string, description?: string) => Promise<void>;
  updateTodo: (id: number, data: Partial<Todo>) => Promise<void>;
  toggleTodo: (id: number, is_completed: boolean) => Promise<void>;
  deleteTodo: (id: number) => Promise<void>;
  clearError: () => void;
}

export const useTodoStore = create<TodoState>((set, get) => ({
  todos: [],
  stats: { total: 0, completed: 0, pending: 0 },
  loading: false,
  error: null,

  fetchTodos: async (completed?: boolean) => {
    set({ loading: true, error: null });
    try {
      const response = await todoApi.getTodos(completed);
      set({
        todos: response.todos,
        stats: {
          total: response.total,
          completed: response.completed,
          pending: response.pending,
        },
        loading: false,
      });
    } catch (error) {
      set({
        error: 'Failed to fetch todos',
        loading: false,
      });
      throw error;
    }
  },

  createTodo: async (title: string, description?: string) => {
    set({ loading: true, error: null });
    try {
      const todo = await todoApi.createTodo({ title, description });
      set((state) => ({
        todos: [todo, ...state.todos],
        stats: {
          ...state.stats,
          total: state.stats.total + 1,
          pending: state.stats.pending + 1,
        },
        loading: false,
      }));
    } catch (error) {
      set({ error: 'Failed to create todo', loading: false });
      throw error;
    }
  },

  updateTodo: async (id: number, data: Partial<Todo>) => {
    set({ error: null });
    try {
      const updatedTodo = await todoApi.updateTodo(id, data);
      set((state) => ({
        todos: state.todos.map((t) => (t.id === id ? updatedTodo : t)),
      }));
    } catch (error) {
      set({ error: 'Failed to update todo' });
      throw error;
    }
  },

  toggleTodo: async (id: number, is_completed: boolean) => {
    set({ error: null });
    try {
      const updatedTodo = await todoApi.toggleTodoStatus(id, is_completed);
      set((state) => ({
        todos: state.todos.map((t) => (t.id === id ? updatedTodo : t)),
        stats: {
          ...state.stats,
          completed: state.stats.completed + (is_completed ? 1 : -1),
          pending: state.stats.pending + (is_completed ? -1 : 1),
        },
      }));
    } catch (error) {
      set({ error: 'Failed to toggle todo' });
      throw error;
    }
  },

  deleteTodo: async (id: number) => {
    set({ error: null });
    try {
      await todoApi.deleteTodo(id);
      set((state) => {
        const todo = state.todos.find((t) => t.id === id);
        return {
          todos: state.todos.filter((t) => t.id !== id),
          stats: {
            total: state.stats.total - 1,
            completed: state.stats.completed - (todo?.is_completed ? 1 : 0),
            pending: state.stats.pending - (todo?.is_completed ? 0 : 1),
          },
        };
      });
    } catch (error) {
      set({ error: 'Failed to delete todo' });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));
