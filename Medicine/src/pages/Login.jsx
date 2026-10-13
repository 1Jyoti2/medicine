import { useState } from 'react'
import { CheckCircle2, LogIn } from 'lucide-react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import AuthLayout from '../components/AuthLayout.jsx'
import Field from '../components/AuthField.jsx'
import { inputClassName } from '../components/authClassNames.js'
import Button from '../components/Button.jsx'
import ErrorMessage from '../components/ErrorMessage.jsx'
import useAuth from '../context/useAuth.js'

function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useAuth()

  const from = location.state?.from ?? '/'
  const notice = location.state?.message ?? null

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  function handleSubmit(event) {
    event.preventDefault()
    setFormError(null)

    const nextErrors = {}
    if (!email.trim()) nextErrors.email = 'Email is required.'
    if (!password) nextErrors.password = 'Password is required.'
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length > 0) return

    setIsSubmitting(true)
    const result = login({ email, password })
    setIsSubmitting(false)

    if (!result.ok) {
      setFormError(result.error)
      return
    }
    navigate(from, { replace: true })
  }

  return (
    <AuthLayout
      eyebrow="Welcome Back"
      title="Sign in to MedScan AI"
      subtitle="Access leaf detection, tablet recognition, prescription scanning and your history."
      footer={
        <>
          Don&apos;t have an account?{' '}
          <Link
            to="/signup"
            className="font-semibold text-emerald-700 hover:text-emerald-800"
          >
            Sign up for free
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} noValidate className="space-y-4">
        {notice && (
          <div
            role="status"
            className="flex items-start gap-3 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800"
          >
            <CheckCircle2
              aria-hidden
              className="mt-0.5 size-5 shrink-0 text-emerald-600"
            />
            <p className="flex-1">{notice}</p>
          </div>
        )}
        {formError && (
          <ErrorMessage
            message={formError}
            onDismiss={() => setFormError(null)}
          />
        )}

        <Field label="Email address" error={errors.email}>
          {(id) => (
            <input
              id={id}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className={inputClassName}
              autoComplete="email"
            />
          )}
        </Field>

        <Field label="Password" error={errors.password}>
          {(id) => (
            <input
              id={id}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className={inputClassName}
              autoComplete="current-password"
            />
          )}
        </Field>

        <div className="flex items-center justify-end">
          <Link
            to="/forgot-password"
            className="text-xs font-semibold text-emerald-700 hover:text-emerald-800"
          >
            Forgot password?
          </Link>
        </div>

        <Button
          type="submit"
          size="lg"
          fullWidth
          icon={LogIn}
          loading={isSubmitting}
        >
          {isSubmitting ? 'Signing in…' : 'Sign In'}
        </Button>
      </form>
    </AuthLayout>
  )
}

export default Login