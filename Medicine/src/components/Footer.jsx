import {
  BookOpen,
  Globe,
  Heart,
  Mail,
  MapPin,
  MessageCircle,
  Phone,
  ShieldCheck,
  Sparkles,
} from 'lucide-react'
import { Link } from 'react-router-dom'

import BrandLogo from './BrandLogo.jsx'
import useLanguage from '../context/useLanguage.js'

const exploreLinks = [
  { to: '/', labelKey: 'nav.home' },
  { to: '/leaf-detection', labelKey: 'nav.leaf' },
  { to: '/tablet-detection', labelKey: 'nav.tablet' },
  { to: '/prescription', labelKey: 'nav.prescription' },
  { to: '/history', labelKey: 'nav.history' },
]

const learnLinks = [
  { to: '/how-it-works', labelKey: 'nav.howItWorks' },
  { to: '/about', labelKey: 'nav.about' },
]

const socialLinks = [
  { href: '#', label: 'Mail us', icon: Mail },
  { href: '#', label: 'Community', icon: MessageCircle },
  { href: '#', label: 'Visit site', icon: Globe },
]

function FooterLink({ to, children }) {
  return (
    <Link
      to={to}
      className="text-sm text-slate-400 transition-colors duration-200 hover:text-emerald-400"
    >
      {children}
    </Link>
  )
}

function Footer() {
  const { t } = useLanguage()
  return (
    <footer className="bg-slate-950 text-slate-300">
      <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <BrandLogo isDark={true} />
            <p className="mt-4 text-sm leading-relaxed text-slate-400">
              {t('footer.desc')}
            </p>
            <div className="mt-5 flex items-center gap-3">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  aria-label={social.label}
                  className="grid size-9 place-items-center rounded-full border border-slate-800 bg-slate-900 text-slate-400 transition-all duration-200 hover:border-emerald-500 hover:text-emerald-400"
                >
                  <social.icon className="size-4" />
                </a>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white">
              {t('footer.explore')}
            </h3>
            <ul className="mt-4 space-y-3">
              {exploreLinks.map((link) => (
                <li key={link.to + link.labelKey}>
                  <FooterLink to={link.to}>{t(link.labelKey)}</FooterLink>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white">
              {t('footer.learnMore')}
            </h3>
            <ul className="mt-4 space-y-3">
              {learnLinks.map((link) => (
                <li key={link.to + link.labelKey}>
                  <FooterLink to={link.to}>{t(link.labelKey)}</FooterLink>
                </li>
              ))}
              <li>
                <a
                  href="#"
                  className="flex items-center gap-2 text-sm text-slate-400 transition-colors duration-200 hover:text-emerald-400"
                >
                  <ShieldCheck className="size-4" />
                  {t('footer.privacy')}
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="flex items-center gap-2 text-sm text-slate-400 transition-colors duration-200 hover:text-emerald-400"
                >
                  <BookOpen className="size-4" />
                  {t('footer.terms')}
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white">
              {t('footer.getInTouch')}
            </h3>
            <ul className="mt-4 space-y-3 text-sm text-slate-400">
              <li className="flex items-start gap-3">
                <MapPin className="mt-0.5 size-4 shrink-0 text-emerald-400" />
                {t('footer.address')}
              </li>
              <li className="flex items-center gap-3">
                <Mail className="size-4 shrink-0 text-emerald-400" />
                hello@medscan.ai
              </li>
              <li className="flex items-center gap-3">
                <Phone className="size-4 shrink-0 text-emerald-400" />
                +94 77 000 0000
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-slate-800 pt-6 sm:flex-row">
          <p className="text-sm text-slate-500">
            &copy; {new Date().getFullYear()} {t('footer.allRights')}
          </p>
          <p className="flex items-center gap-1.5 text-sm text-slate-500">
            {t('footer.builtWithPrefix')}
            <Heart className="size-4 fill-emerald-500 text-emerald-500" />
            {t('footer.and')}
            <Sparkles className="size-4 text-emerald-400" />
            {t('footer.builtWithSuffix')}
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer