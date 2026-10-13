import { Loader2 } from 'lucide-react'

const sizeClasses = {
  sm: 'size-4',
  md: 'size-6',
  lg: 'size-8',
}

function LoadingSpinner({ size = 'md', label, className = '' }) {
  return (
    <div role="status" className={`flex items-center justify-center gap-2 ${className}`}>
      <Loader2 aria-hidden className={`${sizeClasses[size]} animate-spin text-emerald-600`} />
      {label && <span className="text-sm font-medium text-slate-600">{label}</span>}
      <span className="sr-only">Loading</span>
    </div>
  )
}

export default LoadingSpinner