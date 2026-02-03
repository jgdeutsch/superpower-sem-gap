'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Lock } from 'lucide-react';

export default function LoginPage() {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const res = await fetch('/api/auth', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password }),
    });

    if (res.ok) {
      router.push('/');
      router.refresh();
    } else {
      setError('Invalid password');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <div className="flex justify-center mb-6">
            <div className="p-3 rounded-full bg-indigo-100">
              <Lock className="w-8 h-8 text-indigo-600" />
            </div>
          </div>

          <h1 className="text-2xl font-bold text-center text-gray-900 mb-2">
            SEM Gap Analysis
          </h1>
          <p className="text-center text-gray-600 mb-6">
            Enter password to continue
          </p>

          <form onSubmit={handleSubmit}>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 mb-4"
              autoFocus
            />

            {error && (
              <p className="text-red-600 text-sm mb-4 text-center">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition disabled:opacity-50"
            >
              {loading ? 'Checking...' : 'Enter'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
