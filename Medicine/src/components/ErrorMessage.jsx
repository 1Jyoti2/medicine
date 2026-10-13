import { AlertCircle, X } from 'lucide-react'

function ErrorMessage({ message, onDismiss, className = '' }) {
  if (!message) return null

  return (
    <div
      role="alert"
      className={`flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800 ${className}`}
    >
      <AlertCircle aria-hidden className="mt-0.5 size-5 shrink-0 text-rose-600" />
      <p className="flex-1">{message}</p>
      {onDismiss && (
        <button
          type="button"
          aria-label="Dismiss error"
          onClick={onDismiss}
          className="rounded-md p-1 text-rose-500 transition-colors hover:bg-rose-100 hover:text-rose-700"
        >
          <X className="size-4" />
        </button>
      )}
    </div>
  )
}

export default ErrorMessage