function Card({
  children,
  className = '',
  hover = false,
  onClick,
  ...props
}) {
  const base =
    'rounded-3xl border border-slate-200 bg-white p-6 transition-all duration-300'
  const surface = hover
    ? 'hover:-translate-y-1.5 hover:shadow-2xl'
    : 'shadow-sm'

  if (onClick) {
    return (
      <button
        type="button"
        onClick={onClick}
        className={`${base} ${surface} w-full text-left ${className}`}
        {...props}
      >
        {children}
      </button>
    )
  }

  return (
    <div className={`${base} ${surface} ${className}`} {...props}>
      {children}
    </div>
  )
}

export default Card