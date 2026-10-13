import { useState } from 'react'
import { Mail } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'

import AuthLayout from '../components/AuthLayout.jsx'
import Field from '../components/AuthField.jsx'
import { inputClassName } from '../components/authClassNames.js'
import Button from '../components/Button.jsx'
import ErrorMessage from '../components/ErrorMessage.jsx'

function ForgotPassword() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [error, setError] = useState(null)

  function handleSubmit(event) {
    event.preventDefault()
    setError(null)

    if (!email.trim()) {
      setError('Please enter your email address.')
      return
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      setError('Enter a valid email address.')
      return
    }

    navigate('/reset-password', { state: { email: email.trim() } })
  }

  return (
    <AuthLayout
      eyebrow="Password Recovery"
      title="Forgot your password?"
      subtitle="Enter the email associated with your account to set a new password."
      footer={
        <>
          Remembered it?{' '}
          <Link
            to="/login"
            className="font-semibold text-emerald-700 hover:text-emerald-800"
          >
            Back to sign in
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} noValidate className="space-y-4">
        {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

        <Field label="Email address" error={null}>
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

        <Button type="submit" size="lg" fullWidth icon={Mail}>
          Continue
        </Button>
      </form>
    </AuthLayout>
  )
}

export default ForgotPassword