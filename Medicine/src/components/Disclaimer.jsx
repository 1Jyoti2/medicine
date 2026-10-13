import { ShieldAlert } from 'lucide-react'

import useLanguage from '../context/useLanguage.js'

function Disclaimer({ children, className = '' }) {
  const { t } = useLanguage()
  return (
    <p
      className={`inline-flex w-fit max-w-full items-start gap-2 rounded-lg border border-amber-200 bg-amber-50 px-3.5 py-2 text-left text-xs font-medium text-amber-800 ${className}`}
    >
      <ShieldAlert aria-hidden className="mt-0.5 size-4 shrink-0 text-amber-600" />
      <span>{children ?? t('disclaimer')}</span>
    </p>
  )
}

export default Disclaimer