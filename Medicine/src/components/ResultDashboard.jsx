import { useRef, useState } from 'react'
import { Download, Eye, EyeOff, ScanLine, ShieldCheck } from 'lucide-react'

import Button from './Button.jsx'
import BackButton from './BackButton.jsx'
import Card from './Card.jsx'
import ConfidenceBar from './ConfidenceBar.jsx'
import Disclaimer from './Disclaimer.jsx'
import DownloadPdfButton from './DownloadPdfButton.jsx'
import SectionHeader from './SectionHeader.jsx'

const statusStyles = {
  success: {
    label: 'Successful',
    badge: 'bg-emerald-400/10 text-emerald-300 ring-emerald-400/25',
  },
  processed: {
    label: 'Processed',
    badge: 'bg-emerald-400/10 text-emerald-300 ring-emerald-400/25',
  },
  low_confidence: {
    label: 'Low confidence',
    badge: 'bg-amber-400/10 text-amber-300 ring-amber-400/25',
  },
  pending: {
    label: 'Pending',
    badge: 'bg-amber-400/10 text-amber-300 ring-amber-400/25',
  },
  reading: {
    label: 'Reading',
    badge: 'bg-amber-400/10 text-amber-300 ring-amber-400/25',
  },
  uncertain: {
    label: 'Uncertain',
    badge: 'bg-rose-400/10 text-rose-300 ring-rose-400/25',
  },
  failed: {
    label: 'Failed',
    badge: 'bg-rose-400/10 text-rose-300 ring-rose-400/25',
  },
}

function ImageWithFallback({ src, alt, icon: Icon }) {
  const [failed, setFailed] = useState(false)

  if (!src || failed) {
    return (
      <div className="grid aspect-square w-full place-items-center rounded-2xl border-2 border-dashed border-slate-200 bg-slate-50">
        <div className="p-4 text-center">
          <Icon aria-hidden className="mx-auto size-9 text-slate-300" />
          <p className="mt-2 text-xs text-slate-400">No image available</p>
        </div>
      </div>
    )
  }

  return (
    <img
      src={src}
      alt={alt}
      onError={() => setFailed(true)}
      className="aspect-square w-full rounded-2xl border border-slate-200 bg-slate-50 object-cover shadow-sm"
    />
  )
}

function ResultDashboard({
  icon: Icon = ShieldCheck,
  eyebrow,
  title,
  subtitle,
  typeLabel,
  resultName,
  resultDetail,
  confidence,
  imageUrl,
  imageAlt = 'Uploaded image',
  status,
  response,
  result,
  meta,
  scanAnotherPath,
  scanAnotherLabel = 'Scan Another',
  onDownloadReport,
  pdfFileName,
  children,
  disclaimer,
}) {
  const detailsRef = useRef(null)
  const [showDetails, setShowDetails] = useState(false)

  const statusInfo = statusStyles[status] ?? null
  const clamped = Math.max(0, Math.min(100, confidence ?? 0))
  const levelColor =
    clamped >= 80
      ? 'text-emerald-600'
      : clamped >= 50
        ? 'text-amber-600'
        : 'text-rose-600'
  const levelLabel =
    clamped >= 80
      ? 'High confidence'
      : clamped >= 50
        ? 'Moderate confidence'
        : 'Low confidence'
  const levelBadgeBg =
    clamped >= 80
      ? 'bg-emerald-50'
      : clamped >= 50
        ? 'bg-amber-50'
        : 'bg-rose-50'

  const metaItems = []
  if (response?.requestId) {
    metaItems.push({ label: 'Request ID', value: response.requestId })
  }
  if (result?.model) {
    metaItems.push({ label: 'Model', value: result.model })
  }
  if (result?.imageName) {
    metaItems.push({ label: 'Image file', value: result.imageName })
  }
  if (result?.analyzedAt) {
    metaItems.push({
      label: 'Analyzed at',
      value: new Date(result.analyzedAt).toLocaleString(),
    })
  }
  if (Array.isArray(meta)) {
    metaItems.push(...meta)
  }

  function toggleDetails() {
    const next = !showDetails
    setShowDetails(next)
    if (next && detailsRef.current) {
      requestAnimationFrame(() => {
        detailsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      })
    }
  }

  function handleSave() {
    const payload = {
      exportedAt: new Date().toISOString(),
      ...(response ?? {}),
      data: response?.data ?? result,
    }
    if (!payload.data) return

    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `medleaf-result-${result?.id ?? 'export'}.json`
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6 lg:px-8">
      <BackButton className="mb-8" />

      <div className="mb-10">
        <SectionHeader eyebrow={eyebrow} title={title} subtitle={subtitle} />
      </div>

      <Card className="overflow-hidden p-0">
        <div className="flex flex-wrap items-center justify-between gap-4 bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-900 px-6 py-5 sm:px-8">
          <div className="flex items-center gap-3">
            <span className="grid size-12 shrink-0 place-items-center rounded-2xl bg-white/10 text-emerald-300 ring-1 ring-white/10">
              <Icon aria-hidden className="size-6" />
            </span>
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-emerald-300">
                {typeLabel}
              </p>
              <h2 className="mt-0.5 text-xl font-bold text-white sm:text-2xl">
                {resultName}
              </h2>
              {resultDetail && (
                <p className="text-sm italic text-slate-400">{resultDetail}</p>
              )}
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {statusInfo && (
              <span
                className={`rounded-full px-3 py-1 text-xs font-semibold capitalize shadow-sm ring-1 ${statusInfo.badge}`}
              >
                {statusInfo.label}
              </span>
            )}
            {typeof confidence === 'number' && (
              <span className="text-2xl font-extrabold text-emerald-300">
                {clamped.toFixed(1)}%
              </span>
            )}
          </div>
        </div>

        <div className="grid gap-6 p-6 sm:p-8 md:grid-cols-[minmax(0,280px)_1fr]">
          <div>
            <ImageWithFallback src={imageUrl} alt={imageAlt} icon={Icon} />
          </div>

          <div className="flex flex-col">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                  {typeLabel}
                </span>
                <h3 className="mt-2 text-2xl font-extrabold text-slate-900">
                  {resultName}
                </h3>
                {resultDetail && (
                  <p className="mt-1 text-sm italic text-slate-500">
                    {resultDetail}
                  </p>
                )}
              </div>
              {typeof confidence === 'number' && (
                <div
                  className={`min-w-24 rounded-2xl px-4 py-3 text-center ${levelBadgeBg}`}
                >
                  <span className={`text-2xl font-extrabold ${levelColor}`}>
                    {clamped.toFixed(1)}%
                  </span>
                  <p className="mt-0.5 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
                    {levelLabel}
                  </p>
                </div>
              )}
            </div>

            {typeof confidence === 'number' && (
              <div className="mt-5">
                <ConfidenceBar value={confidence} label="Prediction confidence" />
              </div>
            )}

            {metaItems.length > 0 && (
              <dl className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
                {metaItems.map((item) => (
                  <div
                    key={item.label}
                    className="rounded-xl border border-slate-100 bg-slate-50 px-3.5 py-2.5"
                  >
                    <dt className="text-[11px] font-semibold uppercase tracking-wide text-slate-500">
                      {item.label}
                    </dt>
                    <dd className="mt-0.5 truncate text-sm font-medium text-slate-800">
                      {item.value}
                    </dd>
                  </div>
                ))}
              </dl>
            )}

            <div className="mt-auto flex flex-wrap gap-3 pt-6">
              <Button to={scanAnotherPath} icon={ScanLine}>
                {scanAnotherLabel}
              </Button>
              {children && (
                <Button
                  onClick={toggleDetails}
                  variant="secondary"
                  icon={showDetails ? EyeOff : Eye}
                >
                  {showDetails ? 'Hide Details' : 'View Details'}
                </Button>
              )}
              <Button onClick={handleSave} variant="outline" icon={Download}>
                Save Result
              </Button>
              {onDownloadReport && (
                <DownloadPdfButton
                  onGenerate={onDownloadReport}
                  fileName={pdfFileName}
                />
              )}
            </div>
          </div>
        </div>
      </Card>

      {children && (
        <div className="mt-8">
          <h3 className="mb-4 text-lg font-bold text-slate-900">
            Detailed Information
          </h3>
          {showDetails ? (
            <div ref={detailsRef} className="scroll-mt-24">
              {children}
            </div>
          ) : (
            <button
              type="button"
              onClick={toggleDetails}
              className="flex w-full items-center justify-between gap-4 rounded-3xl border-2 border-dashed border-slate-200 bg-white px-6 py-5 text-sm font-medium text-slate-500 transition-colors duration-300 hover:border-emerald-300 hover:text-emerald-700"
            >
              <span>Expand to view properties, uses, composition and more.</span>
              <Eye aria-hidden className="size-4.5 shrink-0" />
            </button>
          )}
        </div>
      )}

      <div className="mt-8 flex justify-center">
        <Disclaimer>{disclaimer}</Disclaimer>
      </div>
    </div>
  )
}

export default ResultDashboard