import { useState } from 'react'
import {
  ChevronRight,
  Eye,
  FileText,
  Leaf,
  PenLine,
  Pill,
} from 'lucide-react'

import ConfidenceBar from './ConfidenceBar.jsx'
import EmptyState from './EmptyState.jsx'

const typeStyles = {
  Leaf: {
    tile: 'bg-emerald-100 text-emerald-700',
    badge: 'bg-emerald-50 text-emerald-700',
    Icon: Leaf,
  },
  Tablet: {
    tile: 'bg-sky-100 text-sky-700',
    badge: 'bg-sky-50 text-sky-700',
    Icon: Pill,
  },
  Prescription: {
    tile: 'bg-violet-100 text-violet-700',
    badge: 'bg-violet-50 text-violet-700',
    Icon: FileText,
  },
}

function HistoryThumb({ row, size = 'md' }) {
  const [failed, setFailed] = useState(false)
  const style = typeStyles[row.type] ?? typeStyles.Tablet
  const { Icon } = style
  const isLarge = size === 'lg'
  const sizeClasses = isLarge ? 'size-14' : 'size-10'
  const rounded = isLarge ? 'rounded-xl' : 'rounded-lg'

  if (!row.imageUrl || failed) {
    return (
      <span
        className={`grid ${sizeClasses} shrink-0 place-items-center ${rounded} ${style.tile}`}
        aria-hidden
      >
        <Icon className="size-5" />
      </span>
    )
  }

  return (
    <img
      src={row.imageUrl}
      alt={row.name}
      onError={() => setFailed(true)}
      className={`${sizeClasses} shrink-0 ${rounded} object-cover ring-1 ring-slate-200`}
    />
  )
}

function TypeBadge({ type }) {
  const style = typeStyles[type] ?? typeStyles.Tablet
  return (
    <span
      className={`rounded-full px-2.5 py-1 text-xs font-semibold ${style.badge}`}
    >
      {type}
    </span>
  )
}

function HandwrittenBadge() {
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-700 ring-1 ring-amber-200">
      <PenLine className="size-3" />
      Handwritten
    </span>
  )
}

function ConfidenceCell({ confidence }) {
  if (typeof confidence !== 'number') {
    return <span className="text-slate-400">&mdash;</span>
  }
  return <ConfidenceBar value={confidence} className="w-28" />
}

function HistoryTable({
  rows = [],
  onView,
  emptyTitle = 'No history found',
  emptyDescription = 'Your detection and prescription records will appear here once you use the scanner.',
  className = '',
}) {
  if (rows.length === 0) {
    return <EmptyState title={emptyTitle} description={emptyDescription} />
  }

  return (
    <div className={className}>
      <div className="hidden overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm md:block">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[720px] text-left text-sm">
            <caption className="sr-only">Detection and prescription history</caption>
            <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th scope="col" className="px-5 py-3 font-semibold">
                  Date
                </th>
                <th scope="col" className="px-5 py-3 font-semibold">
                  Type
                </th>
                <th scope="col" className="px-5 py-3 font-semibold">
                  Image
                </th>
                <th scope="col" className="px-5 py-3 font-semibold">
                  Detected Name
                </th>
                <th scope="col" className="px-5 py-3 font-semibold">
                  Confidence
                </th>
                <th scope="col" className="px-5 py-3 text-right font-semibold">
                  Action
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {rows.map((row) => (
                <tr
                  key={row.id}
                  onClick={() => onView?.(row)}
                  className="cursor-pointer transition-colors hover:bg-slate-50/70"
                >
                  <td className="px-5 py-4 whitespace-nowrap text-slate-600">
                    {row.date}
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex flex-wrap items-center gap-1.5">
                      <TypeBadge type={row.type} />
                      {row.handwritten && <HandwrittenBadge />}
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <HistoryThumb row={row} />
                  </td>
                  <td className="px-5 py-4">
                    <p className="font-medium text-slate-800">{row.name}</p>
                    {row.handwritten && row.doctorName && (
                      <p className="mt-0.5 text-xs text-slate-500">
                        {row.doctorName}
                      </p>
                    )}
                  </td>
                  <td className="px-5 py-4">
                    <ConfidenceCell confidence={row.confidence} />
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex justify-end">
                      <button
                        type="button"
                        aria-label={`View ${row.name}`}
                        onClick={() => onView?.(row)}
                        className="inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-slate-600 transition-colors hover:bg-emerald-50 hover:text-emerald-700"
                      >
                        <Eye className="size-3.5" />
                        View
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <ul className="space-y-4 md:hidden">
        {rows.map((row) => (
          <li key={row.id}>
            <button
              type="button"
              onClick={() => onView?.(row)}
              className="flex w-full items-center gap-4 rounded-2xl border border-slate-200 bg-white p-4 text-left shadow-sm transition-colors duration-300 hover:border-emerald-300"
            >
              <HistoryThumb row={row} size="lg" />
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <p className="truncate font-semibold text-slate-800">
                    {row.name}
                  </p>
                  <TypeBadge type={row.type} />
                  {row.handwritten && <HandwrittenBadge />}
                </div>
                {row.handwritten && row.doctorName && (
                  <p className="mt-1 truncate text-xs text-slate-500">
                    {row.doctorName}
                  </p>
                )}
                <p className="mt-1 text-xs text-slate-500">{row.date}</p>
                {typeof row.confidence === 'number' ? (
                  <ConfidenceBar value={row.confidence} className="mt-2 w-32" />
                ) : (
                  <span className="mt-1 block text-xs text-slate-400">
                    No confidence score
                  </span>
                )}
              </div>
              <ChevronRight
                aria-hidden
                className="size-5 shrink-0 text-slate-300"
              />
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default HistoryTable