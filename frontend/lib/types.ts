export interface Todo {
  id: number
  title: string
  description?: string
  is_completed: boolean
  priority: number
  user_id: number
  created_at?: string
  updated_at?: string
}

export interface TodoFormData {
  title: string
  description: string
  priority: number
}

export interface User {
  id: number
  email: string
  username: string
  is_active?: boolean
  created_at?: string
}
