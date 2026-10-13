import { useState } from 'react'
import {
  ClipboardPlus,
  History,
  House,
  Info,
  Leaf,
  LogIn,
  LogOut,
  Menu,
  Pill,
  ScanLine,
  Sparkles,
  UserPlus,
  X,
} from 'lucide-react'
import { NavLink, useNavigate } from 'react-router-dom'

import BrandLogo from './BrandLogo.jsx'
import LanguageSelector from './LanguageSelector.jsx'
import useAuth from '../context/useAuth.js'
import useLanguage from '../context/useLanguage.js'

const navLinks = [
  { to: '/', labelKey: 'nav.home', icon: House, end: true },
  { to: '/leaf-detection', labelKey: 'nav.leaf', icon: ScanLine },
  { to: '/tablet-detection', labelKey: 'nav.tablet', icon: Pill },
  { to: '/prescription', labelKey: 'nav.prescription', icon: ClipboardPlus },
  { to: '/history', labelKey: 'nav.history', icon: History },
  { to: '/how-it-works', labelKey: 'nav.howItWorks', icon: Sparkles },
  { to: '/about', labelKey: 'nav.about', icon: Info },
]

function Navbar() {
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const { language, changeLanguage, t } = useLanguage()
  const [isMobileOpen, setIsMobileOpen] = useState(false)

  function handleLogout() {
    setIsMobileOpen(false)
    logout()
    navigate('/login', { replace: true })
  }

  const desktopLinkClasses = ({ isActive }) =>
    `relative px-3 py-1.5 text-sm font-medium transition-colors duration-200 after:absolute after:inset-x-3 after:-bottom-0.5 after:h-0.5 after:rounded-full after:transition-all after:duration-300 ${
      isActive
        ? 'text-emerald-700 after:bg-emerald-600 after:w-6'
        : 'text-slate-600 after:bg-emerald-600 after:w-0 hover:text-emerald-700 hover:after:w-6'
    }`

  const mobileLinkClasses = ({ isActive }) =>
    `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors duration-200 ${
      isActive
        ? 'bg-emerald-50 text-emerald-700'
        : 'text-slate-600 hover:bg-slate-50 hover:text-emerald-700'
    }`

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/80 backdrop-blur-md">
      <nav className="mx-auto flex h-16 w-full max-w-7xl items-center justify-between gap-3 px-4 sm:px-6 lg:px-8">
        <BrandLogo />

        <ul className="hidden items-center gap-0.5 lg:flex">
          {navLinks.map((link) => (
            <li key={link.to}>
              <NavLink to={link.to} end={link.end} className={desktopLinkClasses}>
                {t(link.labelKey)}
              </NavLink>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-2">
          <LanguageSelector value={language} onChange={changeLanguage} />

          <div className="hidden items-center gap-2 md:flex">
            {user ? (
              <>
                <NavLink
                  to="/profile"
                  onClick={() => setIsMobileOpen(false)}
                  className="flex items-center gap-2 rounded-full border border-slate-200 bg-white py-1.5 pl-1.5 pr-3 text-sm font-semibold text-slate-700 transition-all duration-200 hover:border-emerald-300 hover:text-emerald-700"
                >
                  <span className="grid size-7 place-items-center rounded-full bg-emerald-100 text-xs font-bold text-emerald-700">
                    {initials(user.name)}
                  </span>
                  <span className="hidden max-w-24 truncate xl:inline">
                    {user.name.split(' ')[0]}
                  </span>
                </NavLink>
                <button
                  type="button"
                  onClick={handleLogout}
                  aria-label={t('nav.logOut')}
                  title={t('nav.logOut')}
                  className="grid size-10 place-items-center rounded-full border border-slate-200 bg-white text-slate-600 transition-all duration-200 hover:border-rose-300 hover:text-rose-600"
                >
                  <LogOut className="size-4.5" />
                </button>
              </>
            ) : (
              <>
                <NavLink
                  to="/login"
                  className="inline-flex items-center gap-1.5 rounded-full border-2 border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition-all duration-200 hover:border-emerald-300 hover:text-emerald-700"
                >
                  <LogIn className="size-4" />
                  {t('nav.signIn')}
                </NavLink>
                <NavLink
                  to="/signup"
                  className="inline-flex items-center gap-1.5 rounded-full bg-emerald-700 px-4 py-2 text-sm font-semibold text-white shadow-sm shadow-emerald-700/20 transition-all duration-200 hover:bg-emerald-800"
                >
                  <UserPlus className="size-4" />
                  {t('nav.signUp')}
                </NavLink>
              </>
            )}
          </div>

          <button
            type="button"
            aria-label="Toggle navigation menu"
            aria-expanded={isMobileOpen}
            onClick={() => setIsMobileOpen((open) => !open)}
            className="flex size-10 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-600 transition-all duration-200 hover:border-emerald-300 hover:text-emerald-700 lg:hidden"
          >
            {isMobileOpen ? (
              <X className="size-5" />
            ) : (
              <Menu className="size-5" />
            )}
          </button>
        </div>
      </nav>

      {isMobileOpen && (
        <div className="absolute inset-x-0 top-full max-h-[calc(100dvh-4rem)] overflow-y-auto border-t border-slate-100 bg-white shadow-lg shadow-slate-200/60 lg:hidden">
          <ul className="space-y-1 px-4 py-4">
            {navLinks.map((link) => (
              <li key={link.to}>
                <NavLink
                  to={link.to}
                  end={link.end}
                  onClick={() => setIsMobileOpen(false)}
                  className={mobileLinkClasses}
                >
                  <link.icon className="size-4.5 text-emerald-600" />
                  {t(link.labelKey)}
                </NavLink>
              </li>
            ))}
          </ul>

          <div className="border-t border-slate-100 px-4 py-4">
            {user ? (
              <>
                <NavLink
                  to="/profile"
                  onClick={() => setIsMobileOpen(false)}
                  className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50 hover:text-emerald-700"
                >
                  <span className="grid size-9 place-items-center rounded-full bg-emerald-100 text-sm font-bold text-emerald-700">
                    {initials(user.name)}
                  </span>
                  <span className="min-w-0">
                    <span className="block truncate font-semibold">
                      {user.name}
                    </span>
                    <span className="block truncate text-xs text-slate-400">
                      {user.email}
                    </span>
                  </span>
                </NavLink>
                <button
                  type="button"
                  onClick={handleLogout}
                  className="mt-1 flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:bg-rose-50 hover:text-rose-600"
                >
                  <LogOut className="size-4.5 text-rose-500" />
                  {t('nav.logOut')}
                </button>
              </>
            ) : (
              <div className="flex flex-col gap-2">
                <NavLink
                  to="/login"
                  onClick={() => setIsMobileOpen(false)}
                  className="flex items-center justify-center gap-2 rounded-xl bg-emerald-700 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-emerald-800"
                >
                  <LogIn className="size-4" />
                  {t('nav.signIn')}
                </NavLink>
                <NavLink
                  to="/signup"
                  onClick={() => setIsMobileOpen(false)}
                  className="flex items-center justify-center gap-2 rounded-xl border-2 border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-700 transition-colors hover:border-emerald-300 hover:text-emerald-700"
                >
                  <UserPlus className="size-4" />
                  {t('nav.signUp')}
                </NavLink>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  )
}

function initials(name) {
  if (!name) return '?'
  return name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')
}

export default Navbar