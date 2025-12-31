'use client'

import { useState } from 'react'
import { Todo } from '@/lib/types'
import { cn } from '@/lib/utils'

interface TodoItemProps {
  todo: Todo
  onToggle: (id: number) => Promise<void>
  onDelete: (id: number) => Promise<void>
  onEdit: (todo: Todo) => void
}

export default function TodoItem({ todo, onToggle, onDelete, onEdit }: TodoItemProps) {
  const [loading, setLoading] = useState(false)

  const handleToggle = async () => {
    if (loading) return
    setLoading(true)
    try {
      await onToggle(todo.id)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (loading) return
    if (!confirm('Are you sure you want to delete this todo?')) return
    setLoading(true)
    try {
      await onDelete(todo.id)
    } finally {
      setLoading(false)
    }
  }

  const priorityColors = {
    0: 'bg-gray-100 text-gray-600',
    1: 'bg-yellow-100 text-yellow-700',
    2: 'bg-red-100 text-red-700',
  }

  const priorityLabels = {
    0: 'Low',
    1: 'Medium',
    2: 'High',
  }

  return (
    <div className={cn(
      'flex items-start gap-3 p-4 bg-white rounded-lg border shadow-sm transition-all',
      todo.is_completed && 'bg-gray-50'
    )}>
      <button
        onClick={handleToggle}
        disabled={loading}
        className={cn(
          'mt-1 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors',
          todo.is_completed
            ? 'bg-primary-600 border-primary-600 text-white'
            : 'border-gray-300 hover:border-primary-500'
        )}
      >
        {todo.is_completed && (
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
          </svg>
        )}
      </button>

      <div className="flex-1 min-w-0">
        <h3 className={cn(
          'font-medium text-gray-900',
          todo.is_completed && 'line-through text-gray-500'
        )}>
          {todo.title}
        </h3>
        {todo.description && (
          <p className={cn(
            'text-sm text-gray-500 mt-1',
            todo.is_completed && 'line-through'
          )}>
            {todo.description}
          </p>
        )}
        <div className="flex items-center gap-2 mt-2">
          <span className={cn(
            'text-xs px-2 py-0.5 rounded-full font-medium',
            priorityColors[todo.priority as keyof typeof priorityColors]
          )}>
            {priorityLabels[todo.priority as keyof typeof priorityLabels]}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => onEdit(todo)}
          className="p-2 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
          title="Edit"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
        <button
          onClick={handleDelete}
          disabled={loading}
          className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          title="Delete"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  )
}
