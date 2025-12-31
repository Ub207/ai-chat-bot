'use client'

import Link from 'next/link'
import { useAuthStore } from '@/lib/auth'

export default function Header() {
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <Link href="/dashboard" className="text-xl font-bold text-gray-900">
          Todo App
        </Link>

        <div className="flex items-center gap-4">
          <span className="text-gray-600">
            {user?.username}
          </span>
          <button
            onClick={handleLogout}
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  )
}
