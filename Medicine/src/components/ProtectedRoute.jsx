import { useLocation } from 'react-router-dom'
import { Lock } from 'lucide-react'

import useAuth from '../context/useAuth.js'
import Card from './Card.jsx'
import Button from './Button.jsx'

function ProtectedRoute({ children }) {
  const { user } = useAuth()
  const location = useLocation()

  if (user) {
    return children
  }

  return (
    <div className="flex min-h-[70vh] items-center justify-center px-4 py-16">
      <Card className="max-w-md p-8 text-center sm:p-10">
        <span className="mx-auto grid size-16 place-items-center rounded-2xl bg-amber-50 text-amber-600">
          <Lock className="size-8" aria-hidden />
        </span>
        <h1 className="mt-6 text-2xl font-bold text-slate-900 sm:text-3xl">
          Sign in required
        </h1>
        <p className="mx-auto mt-3 max-w-xs text-slate-600">
          Please sign in to access this page. It is available only to signed-in
          users.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Button
            to="/login"
            state={{ from: location.pathname }}
            className="min-w-40"
          >
            Sign In
          </Button>
          <Button to="/signup" variant="outline">
            Create Account
          </Button>
        </div>
      </Card>
    </div>
  )
}

export default ProtectedRoute