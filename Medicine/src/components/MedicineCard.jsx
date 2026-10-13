import { Pill } from 'lucide-react'

import Card from './Card.jsx'

function MedicineCard({ medicine, onSelect, className = '' }) {
  return (
    <Card hover onClick={onSelect} className={className}>
      <div className="flex items-center gap-4">
        <span className="grid size-12 shrink-0 place-items-center rounded-2xl bg-sky-100 text-sky-700">
          <Pill aria-hidden className="size-6" />
        </span>
        <div className="min-w-0">
          <h3 className="truncate text-lg font-bold text-slate-900">
            {medicine.name}
          </h3>
          <p className="truncate text-sm italic text-slate-500">
            {medicine.genericName}
          </p>
        </div>
      </div>
      <ul className="mt-4 space-y-1.5">
        {medicine.uses.map((use) => (
          <li
            key={use}
            className="flex items-start gap-2 text-sm text-slate-600"
          >
            <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-sky-500" />
            {use}
          </li>
        ))}
      </ul>
      <p className="mt-3 text-xs text-slate-400">
        {medicine.category} &middot; {medicine.dosage}
      </p>
    </Card>
  )
}

export default MedicineCard