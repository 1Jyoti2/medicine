import { useState } from 'react'
import { AlertCircle, Check, FileDown } from 'lucide-react'

import LoadingSpinner from './LoadingSpinner.jsx'

function DownloadPdfButton({
  onGenerate,
  fileName = 'Report.pdf',
  label = 'Download PDF Report',
  className = '',
}) {
  const [status, setStatus] = useState('idle')

  async function handleClick() {
    if (status === 'loading') return
    setStatus('loading')
    try {
      const doc = await onGenerate()
      doc.save(fileName)
      setStatus('success')
      window.setTimeout(() => setStatus('idle'), 3000)
    } catch {
      setStatus('error')
      window.setTimeout(() => setStatus('idle'), 3000)
    }
  }

  const isBusy = status === 'loading'

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={isBusy}
      aria-live="polite"
      className={`inline-flex items-center justify-center gap-2 rounded-xl border-2 border-emerald-600 bg-white px-5 py-2.5 text-sm font-semibold text-emerald-700 transition-all duration-300 hover:-translate-y-0.5 hover:bg-emerald-50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 disabled:cursor-not-allowed disabled:opacity-60 ${className}`}
    >
      {status === 'loading' ? (
        <LoadingSpinner size="sm" />
      ) : status === 'success' ? (
        <Check aria-hidden className="size-4.5 text-emerald-600" />
      ) : status === 'error' ? (
        <AlertCircle aria-hidden className="size-4.5 text-rose-600" />
      ) : (
        <FileDown aria-hidden className="size-4.5" />
      )}
      <span>
        {status === 'loading'
          ? 'Generating PDF…'
          : status === 'success'
            ? 'Report downloaded'
            : status === 'error'
              ? 'Download failed'
              : label}
      </span>
    </button>
  )
}

export default DownloadPdfButton