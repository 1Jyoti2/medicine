function highlightAmpersands(title) {
  if (typeof title !== 'string') return title

  const parts = title.split(/(\s+)/)
  return parts.map((part, index) =>
    part.trim() === '&' ? (
      <span key={index} className="text-emerald-600">
        {part.trim()}
      </span>
    ) : (
      part
    ),
  )
}

function Banner({ eyebrow, title, subtitle, className = '' }) {
  return (
    <section
      className={`relative overflow-hidden rounded-3xl border border-emerald-100 bg-gradient-to-br from-emerald-50/80 via-slate-50 to-white px-6 py-16 sm:px-12 sm:py-20 ${className}`}
    >
      <div aria-hidden className="pointer-events-none absolute inset-0">
        <div className="absolute -left-16 -top-16 size-56 rounded-full bg-emerald-200/40 blur-3xl" />
        <div className="absolute -bottom-20 -right-10 size-64 rounded-full bg-teal-200/30 blur-3xl" />
        <div className="absolute right-16 top-1/3 hidden size-24 rounded-3xl border border-emerald-200/60 bg-white/60 sm:block" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(16,185,129,0.1)_1px,transparent_0)] bg-[size:22px_22px]" />
      </div>

      <div className="relative max-w-3xl">
        {eyebrow && (
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-white px-4 py-1.5 text-xs font-bold uppercase tracking-widest text-emerald-700 shadow-sm">
            <span aria-hidden className="size-1.5 rounded-full bg-emerald-500" />
            {eyebrow}
          </span>
        )}

        {title && (
          <h1 className="mt-6 text-3xl font-extrabold leading-tight tracking-tight text-slate-900 sm:text-4xl lg:text-5xl">
            {highlightAmpersands(title)}
          </h1>
        )}

        {subtitle && (
          <p className="mt-5 max-w-2xl text-base leading-relaxed text-slate-600 sm:text-lg">
            {subtitle}
          </p>
        )}
      </div>
    </section>
  )
}

export default Banner