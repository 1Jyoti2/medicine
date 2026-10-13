import { Link } from 'react-router-dom'

import LoadingSpinner from './LoadingSpinner.jsx'

const variants = {
  primary:
    'bg-emerald-700 text-white shadow-lg shadow-emerald-700/20 hover:-translate-y-0.5 hover:bg-emerald-800 hover:shadow-xl',
  secondary:
    'border-2 border-emerald-600 bg-white text-emerald-700 hover:-translate-y-0.5 hover:bg-emerald-50',
  outline:
    'border-2 border-slate-200 bg-white text-slate-700 hover:-translate-y-0.5 hover:border-emerald-300 hover:text-emerald-700',
  ghost: 'text-emerald-700 hover:bg-emerald-50',
  danger: 'bg-rose-600 text-white shadow-lg shadow-rose-600/20 hover:-translate-y-0.5 hover:bg-rose-700',
  light: 'bg-white text-emerald-700 shadow-lg hover:-translate-y-0.5 hover:shadow-xl',
}

const sizes = {
  sm: 'px-3.5 py-2 text-xs',
  md: 'px-5 py-2.5 text-sm',
  lg: 'px-6 py-3 text-sm',
}

function Button({
  to,
  href,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  iconPosition = 'left',
  loading = false,
  fullWidth = false,
  className = '',
  children,
  disabled,
  type,
  ...props
}) {
  const classes = [
    'inline-flex items-center justify-center gap-2 rounded-xl font-semibold transition-all duration-300 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 disabled:cursor-not-allowed disabled:opacity-60',
    variants[variant],
    sizes[size],
    fullWidth ? 'w-full' : '',
    className,
  ]
    .filter(Boolean)
    .join(' ')

  const content = (
    <>
      {loading ? (
        <LoadingSpinner size="sm" />
      ) : (
        Icon &&
        iconPosition === 'left' && <Icon aria-hidden className="size-4.5" />
      )}
      <span>{children}</span>
      {!loading && Icon && iconPosition === 'right' && (
        <Icon aria-hidden className="size-4.5" />
      )}
    </>
  )

  if (to) {
    return (
      <Link to={to} className={classes} {...props}>
        {content}
      </Link>
    )
  }

  if (href) {
    return (
      <a href={href} className={classes} {...props}>
        {content}
      </a>
    )
  }

  return (
    <button
      type={type ?? 'button'}
      className={classes}
      disabled={disabled || loading}
      {...props}
    >
      {content}
    </button>
  )
}

export default Button