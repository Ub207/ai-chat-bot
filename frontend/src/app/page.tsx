'use client';

import { useState, useEffect } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

interface Todo {
  id: number;
  title: string;
  status: string;
}

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTodos();
  }, []);

  async function fetchTodos() {
    try {
      const res = await fetch(`${API_BASE}/todos`);
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      setTodos(data.todos || []);
    } catch (e) {
      console.error('Error fetching todos:', e);
    }
  }

  async function addTodo(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      if (res.ok) {
        setTitle('');
        fetchTodos();
      }
    } catch (e) {
      console.error('Error adding todo:', e);
    }
    setLoading(false);
  }

  async function toggleTodo(id: number, currentStatus: string) {
    try {
      const newStatus = currentStatus === 'completed' ? 'pending' : 'completed';
      const isCompleted = newStatus === 'completed';
      const res = await fetch(`${API_BASE}/todos/${id}/toggle`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      fetchTodos();
    } catch (e) {
      console.error('Error toggling todo:', e);
    }
  }

  async function deleteTodo(id: number) {
    try {
      const res = await fetch(`${API_BASE}/todos/${id}`, { method: 'DELETE' });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      fetchTodos();
    } catch (e) {
      console.error('Error deleting todo:', e);
    }
  }

  const completed = todos.filter(t => t.status === 'completed').length;
  const pending = todos.length - completed;

  return (
    <div style={{
      minHeight: '100vh',
      padding: '20px',
      backgroundColor: '#f9fafb',
      fontFamily: 'system-ui, sans-serif'
    }}>
      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 'bold', textAlign: 'center', marginBottom: '8px' }}>
          Todo App
        </h1>
        <p style={{ textAlign: 'center', color: '#666', marginBottom: '24px' }}>
          Stay organized, get things done
        </p>

        {/* Add Todo */}
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', marginBottom: '16px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
          <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>Add New Todo</h2>
          <form onSubmit={addTodo}>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What needs to be done?"
              style={{
                width: '100%',
                padding: '12px',
                border: '1px solid #ddd',
                borderRadius: '8px',
                fontSize: '16px',
                marginBottom: '8px',
                boxSizing: 'border-box'
              }}
            />
            <button
              type="submit"
              disabled={!title.trim() || loading}
              style={{
                width: '100%',
                padding: '12px',
                backgroundColor: title.trim() && !loading ? '#0284c7' : '#ccc',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                cursor: title.trim() && !loading ? 'pointer' : 'not-allowed'
              }}
            >
              {loading ? 'Adding...' : 'Add Todo'}
            </button>
          </form>
        </div>

        {/* Stats */}
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', marginBottom: '16px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
          <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>Statistics</h2>
          <div style={{ display: 'flex', gap: '20px' }}>
            <div><strong>Total:</strong> {todos.length}</div>
            <div><strong>Completed:</strong> {completed}</div>
            <div><strong>Pending:</strong> {pending}</div>
          </div>
        </div>

        {/* Todos List */}
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
          <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>Your Todos</h2>

          {todos.length === 0 ? (
            <p style={{ color: '#999', textAlign: 'center', padding: '20px' }}>
              No todos yet. Add one above!
            </p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {todos.map(todo => (
                <div
                  key={todo.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '12px',
                    backgroundColor: '#f9fafb',
                    borderRadius: '8px'
                  }}
                >
                  <input
                    type="checkbox"
                    checked={todo.status === 'completed'}
                    onChange={() => toggleTodo(todo.id, todo.status)}
                    style={{ width: '20px', height: '20px' }}
                  />
                  <span style={{
                    flex: 1,
                    textDecoration: todo.status === 'completed' ? 'line-through' : 'none',
                    color: todo.status === 'completed' ? '#999' : '#000'
                  }}>
                    {todo.title}
                  </span>
                  <button
                    onClick={() => deleteTodo(todo.id)}
                    style={{
                      padding: '6px 12px',
                      backgroundColor: '#ef4444',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}