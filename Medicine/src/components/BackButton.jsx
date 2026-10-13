import { ArrowLeft } from 'lucide-react'
import { useLocation, useNavigate } from 'react-router-dom'

import useLanguage from '../context/useLanguage.js'

function BackButton({ fallbackPath = '/', className = '' }) {
  const navigate = useNavigate()
  const location = useLocation()
  const { t } = useLanguage()

  function handleClick() {
    const hasInAppHistory =
      location.key !== 'default' && window.history.length > 1
    if (hasInAppHistory) {
      navigate(-1)
    } else {
      navigate(fallbackPath)
    }
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      aria-label={t('common.back')}
      className={`group inline-flex items-center gap-2 rounded-xl border-2 border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition-all duration-300 hover:-translate-y-0.5 hover:border-emerald-300 hover:text-emerald-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 ${className}`}
    >
      <ArrowLeft
        aria-hidden
        className="size-4.5 transition-transform duration-300 group-hover:-translate-x-0.5"
      />
      <span>{t('common.back')}</span>
    </button>
  )
}

export default BackButton