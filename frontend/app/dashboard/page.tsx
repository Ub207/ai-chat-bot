'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import Header from '@/components/Header'
import TodoList from '@/components/TodoList'
import TodoForm from '@/components/TodoForm'
import { todosApi } from '@/lib/api'
import { useAuthStore, isAuthenticated } from '@/lib/auth'
import { Todo } from '@/lib/types'

export default function DashboardPage() {
  const router = useRouter()
  const { user, setUser } = useAuthStore()
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null)
  const [error, setError] = useState('')

  // Auth check
  useEffect(() => {
    if (typeof window !== 'undefined' && !isAuthenticated()) {
      router.push('/login')
    }
  }, [router])

  // Fetch todos
  const fetchTodos = useCallback(async () => {
    try {
      const response = await todosApi.getAll()
      setTodos(response.data.todos)
    } catch (err: unknown) {
      const errorMessage = err instanceof Error
        ? err.message
        : 'Failed to fetch todos'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (user) {
      fetchTodos()
    }
  }, [user, fetchTodos])

  // Create todo
  const handleCreate = async (data: { title: string; description: string; priority: number }) => {
    await todosApi.create(data)
    setShowForm(false)
    await fetchTodos()
  }

  // Update todo
  const handleUpdate = async (data: { title: string; description: string; priority: number }) => {
    if (!editingTodo) return
    await todosApi.update(editingTodo.id, data)
    setEditingTodo(null)
    await fetchTodos()
  }

  // Toggle todo
  const handleToggle = async (id: number) => {
    await todosApi.toggle(id)
    await fetchTodos()
  }

  // Delete todo
  const handleDelete = async (id: number) => {
    await todosApi.delete(id)
    await fetchTodos()
  }

  // Edit handler
  const handleEdit = (todo: Todo) => {
    setEditingTodo(todo)
  }

  // Form handlers
  const handleOpenCreate = () => {
    setShowForm(true)
    setEditingTodo(null)
  }

  const handleCloseForm = () => {
    setShowForm(false)
    setEditingTodo(null)
  }

  const handleFormSubmit = async (data: { title: string; description: string; priority: number }) => {
    if (editingTodo) {
      await handleUpdate(data)
    } else {
      await handleCreate(data)
    }
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">My Todos</h1>
            <p className="text-gray-600 mt-1">
              {todos.filter(t => t.is_completed).length} of {todos.length} completed
            </p>
          </div>
          <button
            onClick={handleOpenCreate}
            className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-primary-700 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Todo
          </button>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <TodoList
            todos={todos}
            onToggle={handleToggle}
            onDelete={handleDelete}
            onEdit={handleEdit}
          />
        )}
      </main>

      {(showForm || editingTodo) && (
        <TodoForm
          todo={editingTodo}
          onSubmit={handleFormSubmit}
          onCancel={handleCloseForm}
        />
      )}
    </div>
  )
}
