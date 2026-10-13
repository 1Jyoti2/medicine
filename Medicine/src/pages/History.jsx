import { useEffect, useMemo, useState } from 'react'
import {
  ArrowDownAZ,
  ArrowUpAZ,
  CalendarArrowDown,
  CalendarArrowUp,
  Search,
  TrendingDown,
  TrendingUp,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import Card from '../components/Card.jsx'
import BackButton from '../components/BackButton.jsx'
import HistoryTable from '../components/HistoryTable.jsx'
import SectionHeader from '../components/SectionHeader.jsx'
import {
  getHistory,
  getHandwrittenPrescriptionById,
  getLeafResultById,
  getPrescriptionById,
  getTabletResultById,
} from '../services/api.js'

const typeFilters = ['All', 'Leaf', 'Tablet', 'Prescription']

const sortOptions = [
  { value: 'date-desc', label: 'Newest First', Icon: CalendarArrowDown },
  { value: 'date-asc', label: 'Oldest First', Icon: CalendarArrowUp },
  { value: 'confidence-desc', label: 'Confidence ↓', Icon: TrendingUp },
  { value: 'confidence-asc', label: 'Confidence ↑', Icon: TrendingDown },
  { value: 'name-asc', label: 'Name A → Z', Icon: ArrowDownAZ },
  { value: 'name-desc', label: 'Name Z → A', Icon: ArrowUpAZ },
]

function compareDate(a, b, ascending) {
  const diff = new Date(a).getTime() - new Date(b).getTime()
  return ascending ? diff : -diff
}

function compareConfidence(a, b, ascending) {
  const aVal = typeof a === 'number' ? a : -Infinity
  const bVal = typeof b === 'number' ? b : -Infinity
  return ascending ? aVal - bVal : bVal - aVal
}

function buildResponse(entry, result) {
  return {
    success: true,
    requestId: `req_hist_${entry.id}`,
    message: 'History result loaded.',
    data: result,
  }
}

function HistoryPage() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [activeType, setActiveType] = useState('All')
  const [sortValue, setSortValue] = useState('date-desc')
  const [entries, setEntries] = useState(null)

  const isLoading = entries === null

  useEffect(() => {
    let active = true

    getHistory()
      .then((response) => {
        if (!active) return
        if (response.success && Array.isArray(response.data)) {
          setEntries(response.data)
        } else {
          setEntries([])
        }
      })
      .catch(() => {
        if (!active) return
        setEntries([])
      })

    return () => {
      active = false
    }
  }, [])

  const filteredEntries = useMemo(() => {
    const query = search.trim().toLowerCase()

    let items = entries ?? []

    if (activeType !== 'All') {
      items = items.filter((entry) => entry.type === activeType)
    }

    if (query) {
      items = items.filter(
        (entry) =>
          entry.name.toLowerCase().includes(query) ||
          entry.type.toLowerCase().includes(query) ||
          entry.date.toLowerCase().includes(query),
      )
    }

    const [sortKey, direction] = sortValue.split('-')
    const ascending = direction === 'asc'

    return [...items].sort((a, b) => {
      if (sortKey === 'date') {
        return compareDate(a.date, b.date, ascending)
      }
      if (sortKey === 'confidence') {
        return compareConfidence(a.confidence, b.confidence, ascending)
      }
      if (sortKey === 'name') {
        return ascending
          ? a.name.localeCompare(b.name)
          : b.name.localeCompare(a.name)
      }
      return 0
    })
  }, [entries, search, activeType, sortValue])

  function handleView(entry) {
    if (entry.type === 'Leaf') {
      const result = getLeafResultById(entry.resultId)
      if (result) {
        navigate('/result/leaf', {
          state: {
            response: buildResponse(entry, result),
            imageUrl: entry.imageUrl,
          },
        })
      }
    } else if (entry.type === 'Tablet') {
      const result = getTabletResultById(entry.resultId)
      if (result) {
        navigate('/result/tablet', {
          state: {
            response: buildResponse(entry, result),
            imageUrl: entry.imageUrl,
          },
        })
      }
    } else if (entry.type === 'Prescription') {
      const result = entry.handwritten
        ? getHandwrittenPrescriptionById(entry.resultId)
        : getPrescriptionById(entry.resultId)
      if (result) {
        navigate('/result/prescription', {
          state: {
            response: buildResponse(entry, result),
            imageUrl: entry.imageUrl,
          },
        })
      }
    }
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 lg:px-8">
      <BackButton className="mb-10" />

      <div className="mb-10">
        <SectionHeader
          eyebrow="Records"
          title="Detection History"
          subtitle="Browse your past detection and prescription scan results."
        />
      </div>

      <Card className="p-4 sm:p-6">
        <div className="flex flex-col gap-4">
          <div className="relative">
            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search by name, type or date…"
              className="w-full rounded-xl border border-slate-200 bg-white py-2.5 pl-10 pr-4 text-sm text-slate-800 shadow-sm transition-colors placeholder:text-slate-400 focus:border-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-400/30"
            />
            <Search
              aria-hidden
              className="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-400"
            />
            {search && (
              <button
                type="button"
                aria-label="Clear search"
                onClick={() => setSearch('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 rounded-md px-1.5 py-0.5 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600"
              >
                Clear
              </button>
            )}
          </div>

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex flex-wrap gap-1.5">
              {typeFilters.map((type) => {
                const isActive = activeType === type
                return (
                  <button
                    key={type}
                    type="button"
                    onClick={() => setActiveType(type)}
                    className={`rounded-full px-3.5 py-1.5 text-xs font-semibold transition-colors ${
                      isActive
                        ? 'bg-emerald-700 text-white shadow-sm'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {type}
                  </button>
                )
              })}
            </div>

            <select
              value={sortValue}
              onChange={(event) => setSortValue(event.target.value)}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-slate-700 shadow-sm focus:border-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-400/30"
            >
              {sortOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="mt-6">
          {isLoading ? (
            <div className="flex min-h-[200px] items-center justify-center">
              <span className="flex items-center gap-2 text-sm text-slate-500">
                <span className="size-4 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
                Loading history…
              </span>
            </div>
          ) : (
            <HistoryTable
              rows={filteredEntries}
              onView={handleView}
              emptyTitle="No matching history"
              emptyDescription="Try adjusting your search, filter or sort settings."
            />
          )}
        </div>

        {!isLoading && (
          <p className="mt-5 text-center text-xs text-slate-400">
            Showing {filteredEntries.length} of {entries.length} records
          </p>
        )}
      </Card>
    </div>
  )
}

export default HistoryPage