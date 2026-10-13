import { useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'
import { X } from 'lucide-react'

const sizes = {
  sm: 'max-w-md',
  md: 'max-w-lg',
  lg: 'max-w-3xl',
}

function Modal({
  open,
  onClose,
  title,
  description,
  children,
  footer,
  size = 'md',
  className = '',
}) {
  const closeRef = useRef(null)

  useEffect(() => {
    if (!open) return undefined

    function handleKey(event) {
      if (event.key === 'Escape') onClose?.()
    }

    document.addEventListener('keydown', handleKey)
    document.body.style.overflow = 'hidden'
    closeRef.current?.focus()

    return () => {
      document.removeEventListener('keydown', handleKey)
      document.body.style.overflow = ''
    }
  }, [open, onClose])

  if (!open) return null

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div
        aria-hidden
        className="absolute inset-0 bg-slate-900/60 backdrop-blur-sm"
        onClick={onClose}
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? 'modal-title' : undefined}
        className={`relative w-full ${sizes[size]} rounded-3xl bg-white shadow-2xl ${className}`}
      >
        {(title || onClose) && (
          <div className="flex items-start justify-between gap-4 border-b border-slate-100 px-6 py-4">
            <div>
              {title && (
                <h2 id="modal-title" className="text-lg font-bold text-slate-900">
                  {title}
                </h2>
              )}
              {description && (
                <p className="mt-1 text-sm text-slate-500">{description}</p>
              )}
            </div>
            <button
              ref={closeRef}
              type="button"
              onClick={onClose}
              aria-label="Close modal"
              className="grid size-9 shrink-0 place-items-center rounded-full text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-800"
            >
              <X className="size-5" />
            </button>
          </div>
        )}
        <div className="max-h-[70vh] overflow-y-auto px-6 py-5">{children}</div>
        {footer && (
          <div className="flex flex-wrap justify-end gap-3 border-t border-slate-100 px-6 py-4">
            {footer}
          </div>
        )}
      </div>
    </div>,
    document.body,
  )
}

export default Modal