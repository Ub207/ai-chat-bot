'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function Home() {
  const router = useRouter()

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Todo App
        </h1>
        <p className="text-gray-600 mb-8">
          A production-ready full-stack todo application built with FastAPI and Next.js
        </p>

        <div className="space-y-4">
          <Link
            href="/login"
            className="block w-full bg-primary-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-primary-700 transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/register"
            className="block w-full bg-white text-primary-600 border border-primary-600 py-3 px-4 rounded-lg font-medium hover:bg-primary-50 transition-colors"
          >
            Create Account
          </Link>
        </div>
      </div>
    </div>
  )
}
