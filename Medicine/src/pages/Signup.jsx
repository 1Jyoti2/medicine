import { useState } from 'react'
import { UserPlus } from 'lucide-react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import AuthLayout from '../components/AuthLayout.jsx'
import Field from '../components/AuthField.jsx'
import { inputClassName } from '../components/authClassNames.js'
import Button from '../components/Button.jsx'
import ErrorMessage from '../components/ErrorMessage.jsx'
import useAuth from '../context/useAuth.js'

function Signup() {
  const navigate = useNavigate()
  const location = useLocation()
  const { register } = useAuth()

  const from = location.state?.from ?? '/'

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  function handleSubmit(event) {
    event.preventDefault()
    setFormError(null)

    const nextErrors = {}
    if (!name.trim()) nextErrors.name = 'Full name is required.'
    if (!email.trim()) nextErrors.email = 'Email is required.'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      nextErrors.email = 'Enter a valid email address.'
    }
    if (!password) nextErrors.password = 'Password is required.'
    else if (password.length < 6) {
      nextErrors.password = 'Password must be at least 6 characters.'
    }
    if (confirm !== password) nextErrors.confirm = 'Passwords do not match.'
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length > 0) return

    setIsSubmitting(true)
    const result = register({ name, email, password })
    setIsSubmitting(false)

    if (!result.ok) {
      setFormError(result.error)
      return
    }
    navigate(from, { replace: true })
  }

  return (
    <AuthLayout
      eyebrow="Create Account"
      title="Create your MedScan AI account"
      subtitle="Join to run detection scans and keep a record of your results."
      footer={
        <>
          Already have an account?{' '}
          <Link
            to="/login"
            className="font-semibold text-emerald-700 hover:text-emerald-800"
          >
            Sign in
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} noValidate className="space-y-4">
        {formError && (
          <ErrorMessage
            message={formError}
            onDismiss={() => setFormError(null)}
          />
        )}

        <Field label="Full name" error={errors.name}>
          {(id) => (
            <input
              id={id}
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Kasun Perera"
              className={inputClassName}
              autoComplete="name"
            />
          )}
        </Field>

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

        <Field
          label="Password"
          error={errors.password}
          hint="At least 6 characters."
        >
          {(id) => (
            <input
              id={id}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className={inputClassName}
              autoComplete="new-password"
            />
          )}
        </Field>

        <Field label="Confirm password" error={errors.confirm}>
          {(id) => (
            <input
              id={id}
              type="password"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              placeholder="••••••••"
              className={inputClassName}
              autoComplete="new-password"
            />
          )}
        </Field>

        <Button
          type="submit"
          size="lg"
          fullWidth
          icon={UserPlus}
          loading={isSubmitting}
        >
          {isSubmitting ? 'Creating account…' : 'Sign Up'}
        </Button>
      </form>
    </AuthLayout>
  )
}

export default Signup