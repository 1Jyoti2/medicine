import { useId } from 'react'

function Field({ label, hint, error, children }) {
  const id = useId()
  return (
    <div>
      <label
        htmlFor={id}
        className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-600"
      >
        {label}
      </label>
      {children(id)}
      {hint && !error && <p className="mt-1 text-xs text-slate-400">{hint}</p>}
      {error && <p className="mt-1 text-xs font-medium text-rose-600">{error}</p>}
    </div>
  )
}

export default Field