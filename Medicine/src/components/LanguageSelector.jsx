import { useEffect, useRef, useState } from 'react'
import { Check, ChevronDown, Languages } from 'lucide-react'

import useLanguage from '../context/useLanguage.js'

const languages = [
  { code: 'en', labelKey: 'lang.en', short: 'EN' },
  { code: 'kn', labelKey: 'lang.kn', short: 'KN' },
  { code: 'hi', labelKey: 'lang.hi', short: 'HI' },
  { code: 'ml', labelKey: 'lang.ml', short: 'ML' },
]

function LanguageSelector({
  value = 'en',
  onChange,
  className = '',
  ariaLabel = 'Select language',
}) {
  const { t } = useLanguage()
  const [isOpen, setIsOpen] = useState(false)
  const ref = useRef(null)

  const selected = languages.find((lang) => lang.code === value) ?? languages[0]

  useEffect(() => {
    function handleClickOutside(event) {
      if (ref.current && !ref.current.contains(event.target)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div ref={ref} className={`relative ${className}`}>
      <button
        type="button"
        aria-label={ariaLabel}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        onClick={() => setIsOpen((open) => !open)}
        className="flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-600 transition-all duration-200 hover:border-emerald-300 hover:text-emerald-700"
      >
        <Languages aria-hidden className="size-4" />
        <span className="hidden sm:inline">{selected.short}</span>
        <ChevronDown
          aria-hidden
          className={`size-4 transition-transform duration-200 ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </button>

      {isOpen && (
        <div
          role="listbox"
          aria-label="Languages"
          className="absolute right-0 top-full z-50 mt-2 w-40 overflow-hidden rounded-xl border border-slate-100 bg-white py-1 shadow-xl shadow-slate-200/60"
        >
          {languages.map((lang) => (
            <button
              key={lang.code}
              type="button"
              role="option"
              aria-selected={lang.code === selected.code}
              onClick={() => {
                onChange?.(lang.code)
                setIsOpen(false)
              }}
              className={`flex w-full items-center justify-between px-4 py-2 text-sm transition-colors duration-150 ${
                lang.code === selected.code
                  ? 'bg-emerald-50 font-medium text-emerald-700'
                  : 'text-slate-600 hover:bg-slate-50'
              }`}
            >
              {t(lang.labelKey)}
              {lang.code === selected.code && (
                <Check aria-hidden className="size-4" />
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default LanguageSelector