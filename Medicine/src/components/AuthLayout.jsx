import BackButton from './BackButton.jsx'
import BrandLogo from './BrandLogo.jsx'

function AuthLayout({ eyebrow, title, subtitle, children, footer }) {
  return (
    <div className="flex min-h-[80vh] items-center justify-center bg-gradient-to-b from-emerald-50/60 via-white to-white px-4 py-16 sm:px-6">
      <div className="w-full max-w-md">
        <div className="mb-8 flex flex-col items-center text-center">
          <BrandLogo size="lg" />
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/40 sm:p-8">
          <BackButton className="mb-6" />

          {eyebrow && (
            <p className="text-xs font-bold uppercase tracking-widest text-emerald-600">
              {eyebrow}
            </p>
          )}
          {title && (
            <h1 className="mt-2 text-2xl font-extrabold tracking-tight text-slate-900">
              {title}
            </h1>
          )}
          {subtitle && (
            <p className="mt-2 text-sm leading-relaxed text-slate-500">
              {subtitle}
            </p>
          )}

          <div className="mt-6">{children}</div>

          {footer && (
            <div className="mt-6 border-t border-slate-100 pt-5 text-center text-sm text-slate-500">
              {footer}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AuthLayout