'use client';

import { useTodoStore } from '@/lib/store';

export function TodoStats() {
  const { stats } = useTodoStore();

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <p className="text-sm text-gray-500">Total</p>
        <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <p className="text-sm text-gray-500">Completed</p>
        <p className="text-2xl font-bold text-green-600">{stats.completed}</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <p className="text-sm text-gray-500">Pending</p>
        <p className="text-2xl font-bold text-amber-600">{stats.pending}</p>
      </div>
    </div>
  );
}
