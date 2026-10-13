function ConfidenceBar({ value = 0, label, className = '' }) {
  const clamped = Math.max(0, Math.min(100, value))
  const level =
    clamped >= 80 ? 'bg-emerald-500' : clamped >= 50 ? 'bg-amber-500' : 'bg-rose-500'
  const textColor =
    clamped >= 80
      ? 'text-emerald-700'
      : clamped >= 50
        ? 'text-amber-700'
        : 'text-rose-700'

  return (
    <div className={className}>
      {label && (
        <div className="mb-1.5 flex items-center justify-between text-xs font-medium">
          <span className="text-slate-600">{label}</span>
          <span className={textColor}>{clamped}%</span>
        </div>
      )}
      <div
        role="progressbar"
        aria-label={label ?? 'Confidence'}
        aria-valuenow={Math.round(clamped)}
        aria-valuemin={0}
        aria-valuemax={100}
        className="h-2 w-full overflow-hidden rounded-full bg-slate-200"
      >
        <div
          className={`h-full rounded-full transition-all duration-500 ${level}`}
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  )
}

export default ConfidenceBar