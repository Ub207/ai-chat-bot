import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { TodoList } from '@/components/TodoList';
import { AddTodoForm } from '@/components/AddTodoForm';
import { TodoStats } from '@/components/TodoStats';
import { useTodoStore } from '@/lib/store';

// Mock the store
jest.mock('@/lib/store', () => ({
  useTodoStore: jest.fn(),
}));

// Mock the API
jest.mock('@/lib/api', () => ({
  todoApi: {
    getTodos: jest.fn(),
    createTodo: jest.fn(),
    updateTodo: jest.fn(),
    toggleTodoStatus: jest.fn(),
    deleteTodo: jest.fn(),
  },
}));

const mockTodos = [
  {
    id: 1,
    title: 'Test Todo 1',
    description: 'Test description 1',
    is_completed: false,
    due_at: null,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    title: 'Test Todo 2',
    description: null,
    is_completed: true,
    due_at: null,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
];

describe('Todo Components', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('AddTodoForm', () => {
    it('renders form inputs', () => {
      (useTodoStore as jest.Mock).mockReturnValue({
        createTodo: jest.fn(),
        loading: false,
        error: null,
        clearError: jest.fn(),
      });

      render(<AddTodoForm />);

      expect(screen.getByPlaceholderText('What needs to be done?')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Add a description (optional)')).toBeInTheDocument();
      expect(screen.getByText('Add Todo')).toBeInTheDocument();
    });

    it('disables button when title is empty', () => {
      (useTodoStore as jest.Mock).mockReturnValue({
        createTodo: jest.fn(),
        loading: false,
        error: null,
        clearError: jest.fn(),
      });

      render(<AddTodoForm />);

      const button = screen.getByText('Add Todo');
      expect(button).toBeDisabled();
    });

    it('enables button when title is filled', () => {
      (useTodoStore as jest.Mock).mockReturnValue({
        createTodo: jest.fn(),
        loading: false,
        error: null,
        clearError: jest.fn(),
      });

      render(<AddTodoForm />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      fireEvent.change(input, { target: { value: 'New todo' } });

      const button = screen.getByText('Add Todo');
      expect(button).not.toBeDisabled();
    });
  });

  describe('TodoStats', () => {
    it('displays correct statistics', () => {
      (useTodoStore as jest.Mock).mockReturnValue({
        stats: { total: 5, completed: 2, pending: 3 },
      });

      render(<TodoStats />);

      expect(screen.getByText('5')).toBeInTheDocument();
      expect(screen.getByText('2')).toBeInTheDocument();
      expect(screen.getByText('3')).toBeInTheDocument();
    });
  });

  describe('TodoList', () => {
    it('shows loading state', () => {
      (useTodoStore as jest.Mock).mockReturnValue({
        todos: [],
        loading: true,
        fetchTodos: jest.fn(),
      });

      render(<TodoList />);

      expect(screen.getByRole('status')).toBeInTheDocument();
    });

    it('shows empty state when no todos', () => {
      (useTodoStore as jest.Mock).mockReturnValue({
        todos: [],
        loading: false,
        fetchTodos: jest.fn(),
      });

      render(<TodoList />);

      expect(screen.getByText('No todos yet. Add one above!')).toBeInTheDocument();
    });

    it('renders todo items', () => {
      (useTodoStore as jest.Mock).mockReturnValue({
        todos: mockTodos,
        loading: false,
        fetchTodos: jest.fn(),
      });

      render(<TodoList />);

      expect(screen.getByText('Test Todo 1')).toBeInTheDocument();
      expect(screen.getByText('Test Todo 2')).toBeInTheDocument();
    });
  });
});
