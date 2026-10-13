import ConfidenceBar from './ConfidenceBar.jsx'

function ResultCard({
  icon: Icon,
  title,
  subtitle,
  badge,
  confidence,
  children,
  actions,
  className = '',
}) {
  const hasIcon = Boolean(Icon)

  return (
    <div
      className={`rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8 ${className}`}
    >
      <div className="flex flex-wrap items-start justify-between gap-5">
        <div className="flex items-center gap-4">
          {hasIcon && (
            <span className="grid size-14 shrink-0 place-items-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 text-white shadow-lg">
              <Icon aria-hidden className="size-7" />
            </span>
          )}
          <div className={hasIcon ? '' : 'w-full'}>
            {badge && (
              <span className="rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-semibold text-emerald-700">
                {badge}
              </span>
            )}
            <h3 className="mt-1 text-xl font-bold text-slate-900">{title}</h3>
            {subtitle && (
              <p className="text-sm italic text-slate-500">{subtitle}</p>
            )}
          </div>
        </div>

        {typeof confidence === 'number' && (
          <ConfidenceBar
            value={confidence}
            label="Confidence"
            className="w-36 sm:w-40"
          />
        )}
      </div>

      {children && <div className="mt-6">{children}</div>}
      {actions && <div className="mt-6 flex flex-wrap gap-3">{actions}</div>}
    </div>
  )
}

export default ResultCard