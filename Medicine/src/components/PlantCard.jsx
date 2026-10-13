import { Leaf } from 'lucide-react'

import Card from './Card.jsx'

function PlantCard({ plant, onSelect, className = '' }) {
  return (
    <Card hover onClick={onSelect} className={className}>
      <div className="flex items-center gap-4">
        <span className="grid size-12 shrink-0 place-items-center rounded-2xl bg-emerald-100 text-emerald-700">
          <Leaf aria-hidden className="size-6" />
        </span>
        <div className="min-w-0">
          <h3 className="truncate text-lg font-bold text-slate-900">
            {plant.name}
          </h3>
          <p className="truncate text-sm italic text-slate-500">
            {plant.scientificName}
          </p>
        </div>
      </div>
      <ul className="mt-4 space-y-1.5">
        {plant.uses.map((use) => (
          <li
            key={use}
            className="flex items-start gap-2 text-sm text-slate-600"
          >
            <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-emerald-500" />
            {use}
          </li>
        ))}
      </ul>
      <p className="mt-3 text-xs text-slate-400">
        {plant.partsUsed} &middot; {plant.nativeRegion}
      </p>
    </Card>
  )
}

export default PlantCard