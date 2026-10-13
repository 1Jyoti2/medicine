import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-24 text-center">
      <h1 className="text-6xl font-bold text-slate-900">404</h1>
      <p className="mt-4 text-slate-600">Page not found.</p>
      <Link
        to="/"
        className="mt-6 inline-block rounded-lg bg-emerald-700 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-800"
      >
        Back to Home
      </Link>
    </div>
  )
}