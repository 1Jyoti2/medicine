import { createContext, useCallback, useMemo, useState } from 'react'

import translations from '../data/translations.js'

const LanguageContext = createContext(null)

const STORAGE_KEY = 'medleaf-lang'

function getInitialLanguage() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored && translations[stored]) return stored
  } catch {
    // localStorage may be unavailable (SSR, private browsing edge cases).
  }
  return 'en'
}

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(getInitialLanguage)

  const changeLanguage = useCallback((code) => {
    if (translations[code]) {
      setLanguage(code)
      try {
        localStorage.setItem(STORAGE_KEY, code)
      } catch {
        // Silently ignore storage errors.
      }
      document.documentElement.lang = code
    }
  }, [])

  const t = useCallback(
    (key) => translations[language]?.[key] ?? translations.en[key] ?? key,
    [language],
  )

  const value = useMemo(
    () => ({ language, changeLanguage, t }),
    [language, changeLanguage, t],
  )

  return (
    <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>
  )
}

export default LanguageContext