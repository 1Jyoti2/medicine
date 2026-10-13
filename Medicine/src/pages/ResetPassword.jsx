import { useState } from 'react'
import { Eye, EyeOff, LockKeyhole } from 'lucide-react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import AuthLayout from '../components/AuthLayout.jsx'
import { inputClassName } from '../components/authClassNames.js'
import Button from '../components/Button.jsx'
import ErrorMessage from '../components/ErrorMessage.jsx'
import useAuth from '../context/useAuth.js'

function PasswordField({
  id,
  label,
  value,
  onChange,
  onBlur,
  placeholder,
  error,
  toggleLabel,
}) {
  const [visible, setVisible] = useState(false)

  return (
    <div>
      <label
        htmlFor={id}
        className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-600"
      >
        {label}
      </label>
      <div className="relative">
        <input
          id={id}
          type={visible ? 'text' : 'password'}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          placeholder={placeholder}
          className={`${inputClassName} pr-11`}
          autoComplete="new-password"
        />
        <button
          type="button"
          aria-label={toggleLabel}
          onClick={() => setVisible((prev) => !prev)}
          className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 transition-colors hover:text-emerald-700"
        >
          {visible ? (
            <EyeOff aria-hidden className="size-4.5" />
          ) : (
            <Eye aria-hidden className="size-4.5" />
          )}
        </button>
      </div>
      {error && <p className="mt-1 text-xs font-medium text-rose-600">{error}</p>}
    </div>
  )
}

function ResetPassword() {
  const navigate = useNavigate()
  const location = useLocation()
  const { resetPassword } = useAuth()

  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState(null)
  const [resetting, setResetting] = useState(false)

  const passwordValid = password.length >= 8
  const passwordsMatch = password !== '' && password === confirmPassword
  const canSubmit = passwordValid && passwordsMatch

  function validate(field) {
    const nextErrors = {}
    if (field === 'password' || field === 'all') {
      if (!password) nextErrors.password = 'Enter your password.'
      else if (password.length < 8)
        nextErrors.password = 'Password must be at least 8 characters.'
    }
    if (field === 'confirmPassword' || field === 'all') {
      if (!confirmPassword)
        nextErrors.confirmPassword = 'Confirm your password.'
      else if (password !== confirmPassword)
        nextErrors.confirmPassword = 'Passwords do not match.'
    }
    setErrors(nextErrors)
  }

  function handleSubmit(event) {
    event.preventDefault()
    setFormError(null)
    if (!canSubmit) {
      validate('all')
      return
    }

    const emailFromState =
      typeof location.state?.email === 'string' ? location.state.email : ''

    setResetting(true)
    setTimeout(() => {
      const result = resetPassword({ email: emailFromState, password })
      setResetting(false)

      if (!result.ok) {
        setFormError(result.error)
        return
      }

      navigate('/login', {
        replace: true,
        state: {
          message:
            'Password reset successfully. Please sign in with your new password.',
        },
      })
    }, 700)
  }

  return (
    <AuthLayout
      title="Reset Password"
      subtitle="Set a new password for your account."
      footer={
        <Link
          to="/login"
          className="font-semibold text-emerald-700 hover:text-emerald-800"
        >
          Back to sign in
        </Link>
      }
    >
      <form onSubmit={handleSubmit} noValidate className="space-y-4">
        {formError && (
          <ErrorMessage
            message={formError}
            onDismiss={() => setFormError(null)}
          />
        )}

        <PasswordField
          id="password"
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onBlur={() => validate('password')}
          placeholder="Enter password"
          error={errors.password}
          toggleLabel="Toggle password visibility"
        />

        <PasswordField
          id="confirm-password"
          label="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          onBlur={() => validate('confirmPassword')}
          placeholder="Confirm password"
          error={errors.confirmPassword}
          toggleLabel="Toggle confirm password visibility"
        />

        <Button
          type="submit"
          size="lg"
          fullWidth
          icon={LockKeyhole}
          loading={resetting}
          disabled={!canSubmit}
        >
          {resetting ? 'Resetting…' : 'Reset Password'}
        </Button>
      </form>
    </AuthLayout>
  )
}

export default ResetPassword