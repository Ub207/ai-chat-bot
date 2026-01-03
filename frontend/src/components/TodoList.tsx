'use client';

import { useEffect, useState } from 'react';
import { useTodoStore } from '@/lib/store';
import { TodoItem } from './TodoItem';
import type { Todo } from '@/types';

type Filter = 'all' | 'active' | 'completed';

export function TodoList() {
  const { todos, loading, fetchTodos } = useTodoStore();
  const [filter, setFilter] = useState<Filter>('all');

  useEffect(() => {
    let completed: boolean | undefined;
    if (filter === 'active') completed = false;
    else if (filter === 'completed') completed = true;
    fetchTodos(completed);
  }, [filter, fetchTodos]);

  const filteredTodos = todos;

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        {(['all', 'active', 'completed'] as Filter[]).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === f
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {f === 'all' ? 'All' : f === 'active' ? 'Active' : 'Completed'}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <svg className="animate-spin h-8 w-8 text-primary-600" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        </div>
      ) : filteredTodos.length === 0 ? (
        <div className="text-center py-12">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p className="mt-4 text-gray-500">
            {filter === 'all'
              ? 'No todos yet. Add one above!'
              : filter === 'active'
              ? 'No active todos'
              : 'No completed todos'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredTodos.map((todo: Todo) => (
            <TodoItem key={todo.id} todo={todo} />
          ))}
        </div>
      )}
    </div>
  );
}
