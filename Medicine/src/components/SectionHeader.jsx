function SectionHeader({
  eyebrow,
  title,
  subtitle,
  align = 'center',
  className = '',
}) {
  const isCentered = align === 'center'

  return (
    <div
      className={`max-w-2xl ${isCentered ? 'mx-auto text-center' : 'text-left'} ${className}`}
    >
      {eyebrow && (
        <span className="text-xs font-bold uppercase tracking-widest text-emerald-600">
          {eyebrow}
        </span>
      )}
      {title && (
        <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          {title}
        </h2>
      )}
      {subtitle && (
        <p className={`mt-4 text-slate-600 ${isCentered ? 'mx-auto' : ''}`}>
          {subtitle}
        </p>
      )}
    </div>
  )
}

export default SectionHeader