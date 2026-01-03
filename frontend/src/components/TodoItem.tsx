'use client';

import { useState } from 'react';
import { format } from 'date-fns';
import { useTodoStore } from '@/lib/store';
import type { Todo } from '@/types';

interface TodoItemProps {
  todo: Todo;
}

export function TodoItem({ todo }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const { toggleTodo, updateTodo, deleteTodo } = useTodoStore();

  const handleToggle = () => {
    toggleTodo(todo.id, !todo.is_completed);
  };

  const handleSave = () => {
    if (editTitle.trim()) {
      updateTodo(todo.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      });
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setIsEditing(false);
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return null;
    try {
      return format(new Date(dateStr), 'MMM d, yyyy h:mm a');
    } catch {
      return null;
    }
  };

  return (
    <div
      className={`group flex items-start gap-3 p-4 bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all ${
        todo.is_completed ? 'bg-gray-50' : ''
      }`}
    >
      <input
        type="checkbox"
        checked={todo.is_completed}
        onChange={handleToggle}
        className="mt-1 w-5 h-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
      />

      <div className="flex-1 min-w-0">
        {isEditing ? (
          <div className="space-y-2">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Todo title"
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm resize-none"
              placeholder="Description (optional)"
              rows={2}
            />
            <div className="flex gap-2">
              <button
                onClick={handleSave}
                className="px-3 py-1 bg-primary-600 text-white rounded-md text-sm hover:bg-primary-700"
              >
                Save
              </button>
              <button
                onClick={handleCancel}
                className="px-3 py-1 bg-gray-200 text-gray-700 rounded-md text-sm hover:bg-gray-300"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <>
            <h3
              className={`font-medium text-gray-900 ${
                todo.is_completed ? 'line-through text-gray-500' : ''
              }`}
            >
              {todo.title}
            </h3>
            {todo.description && (
              <p
                className={`text-sm mt-1 ${
                  todo.is_completed ? 'text-gray-400' : 'text-gray-600'
                }`}
              >
                {todo.description}
              </p>
            )}
            {todo.due_at && (
              <p className="text-xs mt-2 text-gray-500">
                Due: {formatDate(todo.due_at)}
              </p>
            )}
            <p className="text-xs mt-1 text-gray-400">
              Created: {formatDate(todo.created_at)}
            </p>
          </>
        )}
      </div>

      <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
        {!isEditing && (
          <>
            <button
              onClick={() => setIsEditing(true)}
              className="p-2 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded-md transition-colors"
              title="Edit"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </button>
            <button
              onClick={() => deleteTodo(todo.id)}
              className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
              title="Delete"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </>
        )}
      </div>
    </div>
  );
}
