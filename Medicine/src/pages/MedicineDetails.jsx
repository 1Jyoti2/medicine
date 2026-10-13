import { useEffect, useState } from 'react'
import {
  Archive,
  ClipboardList,
  Pill,
  ScanLine,
  ShieldAlert,
  Sparkles,
} from 'lucide-react'
import { useParams } from 'react-router-dom'

import Button from '../components/Button.jsx'
import BackButton from '../components/BackButton.jsx'
import Card from '../components/Card.jsx'
import Disclaimer from '../components/Disclaimer.jsx'
import EmptyState from '../components/EmptyState.jsx'
import LoadingSpinner from '../components/LoadingSpinner.jsx'
import SectionHeader from '../components/SectionHeader.jsx'
import { getMedicineDetails } from '../services/api.js'

function MedicineImage({ imageUrl, name }) {
  const [failed, setFailed] = useState(false)

  if (!imageUrl || failed) {
    return (
      <div className="grid aspect-square w-full place-items-center bg-gradient-to-br from-sky-500 to-indigo-700 md:h-full md:aspect-auto">
        <Pill aria-hidden className="size-20 text-white/90" />
        <span className="sr-only">{name}</span>
      </div>
    )
  }

  return (
    <img
      src={imageUrl}
      alt={`${name} tablet`}
      onError={() => setFailed(true)}
      className="aspect-square w-full rounded-t-3xl object-cover md:h-full md:rounded-l-3xl md:rounded-tr-none"
    />
  )
}

function SectionCard({ title, icon: Icon, iconClasses, className = '', children }) {
  return (
    <Card className={`p-6 ${className}`}>
      <h3 className="flex items-center gap-2 text-sm font-bold uppercase tracking-wide text-slate-500">
        <span
          className={`grid size-8 shrink-0 place-items-center rounded-lg ${iconClasses}`}
        >
          <Icon aria-hidden className="size-4.5" />
        </span>
        {title}
      </h3>
      <div className="mt-4">{children}</div>
    </Card>
  )
}

function ItemList({ items, dotClass }) {
  return (
    <ul className="space-y-2">
      {items.map((item) => (
        <li key={item} className="flex items-start gap-2 text-sm text-slate-700">
          <span className={`mt-1.5 size-1.5 shrink-0 rounded-full ${dotClass}`} />
          {item}
        </li>
      ))}
    </ul>
  )
}

function MedicineDetails() {
  const { name } = useParams()
  const [request, setRequest] = useState({
    name: null,
    error: null,
    medicine: null,
  })

  useEffect(() => {
    let active = true

    getMedicineDetails(name)
      .then((response) => {
        if (!active) return
        if (!response.success) {
          setRequest({
            name,
            error: response.message ?? 'Medicine details could not be found.',
            medicine: null,
          })
        } else {
          setRequest({ name, error: null, medicine: response.data })
        }
      })
      .catch(() => {
        if (!active) return
        setRequest({
          name,
          error: 'Unable to load medicine details. Please try again later.',
          medicine: null,
        })
      })

    return () => {
      active = false
    }
  }, [name])

  const isLoading = request.name !== name

  if (isLoading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center px-4">
        <LoadingSpinner size="lg" label="Loading medicine details…" />
      </div>
    )
  }

  if (request.error || !request.medicine) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
        <EmptyState
          icon={Pill}
          title="Medicine not found"
          description={request.error}
          action={
            <Button to="/" variant="outline">
              Back to Home
            </Button>
          }
        />
      </div>
    )
  }

  const medicine = request.medicine

  return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6 lg:px-8">
      <BackButton className="mb-10" />

      <div className="mb-10">
        <SectionHeader
          eyebrow="Medicine Guide"
          title={medicine.name}
          subtitle={`${medicine.genericName} · ${medicine.category}`}
        />
      </div>

      <Card className="overflow-hidden p-0">
        <div className="grid md:grid-cols-[minmax(0,320px)_1fr]">
          <MedicineImage imageUrl={medicine.imageUrl} name={medicine.name} />
          <div className="flex flex-col p-6 sm:p-8">
            <span className="rounded-full bg-sky-50 px-3 py-1 text-xs font-semibold text-sky-700">
              Pharmaceutical Tablet
            </span>
            <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900">
              {medicine.name}
            </h2>
            <p className="mt-1 text-lg italic text-slate-500">
              {medicine.genericName}
            </p>

            {medicine.composition && (
              <p className="mt-2 text-xs font-medium text-slate-500">
                Composition: {medicine.composition}
              </p>
            )}

            <p className="mt-4 text-sm leading-relaxed text-slate-600">
              {medicine.description}
            </p>

            <div className="mt-6 flex flex-wrap gap-2">
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600">
                Category: {medicine.category}
              </span>
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600">
                Strength: {medicine.dosage}
              </span>
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600">
                By {medicine.manufacturer}
              </span>
            </div>

            <div className="mt-auto flex flex-wrap gap-3 pt-6">
              <Button to="/tablet-detection" icon={ScanLine}>
                Try Tablet Detection
              </Button>
              <Button to="/" variant="outline">
                Back to Home
              </Button>
            </div>
          </div>
        </div>
      </Card>

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <SectionCard
          title="Uses"
          icon={Sparkles}
          iconClasses="bg-sky-100 text-sky-700"
        >
          <ItemList items={medicine.uses} dotClass="bg-sky-500" />
        </SectionCard>

        <SectionCard
          title="Dosage Information"
          icon={ClipboardList}
          iconClasses="bg-violet-100 text-violet-700"
        >
          <dl className="space-y-2 text-sm">
            <div className="flex justify-between gap-4">
              <dt className="text-slate-500">Typical strength</dt>
              <dd className="font-medium text-slate-800">{medicine.dosage}</dd>
            </div>
            <div className="flex justify-between gap-4">
              <dt className="text-slate-500">Form</dt>
              <dd className="font-medium text-slate-800">Tablet</dd>
            </div>
          </dl>
          <p className="mt-4 rounded-xl bg-violet-50 px-3.5 py-2.5 text-xs leading-relaxed text-violet-800">
            Always take exactly as prescribed by your healthcare provider. Never
            exceed the recommended dose.
          </p>
        </SectionCard>

        <SectionCard
          title="Precautions"
          icon={ShieldAlert}
          iconClasses="bg-amber-100 text-amber-700"
        >
          <ItemList items={medicine.precautions} dotClass="bg-amber-500" />
        </SectionCard>

        <SectionCard
          title="Side Effects"
          icon={Pill}
          iconClasses="bg-rose-100 text-rose-700"
        >
          <ItemList items={medicine.sideEffects} dotClass="bg-rose-400" />
        </SectionCard>

        <SectionCard
          title="Storage"
          icon={Archive}
          iconClasses="bg-teal-100 text-teal-700"
          className="md:col-span-2"
        >
          <p className="text-sm leading-relaxed text-slate-700">
            {medicine.storage}
          </p>
        </SectionCard>
      </div>

      <div className="mt-8 flex justify-center">
        <Disclaimer />
      </div>
    </div>
  )
}

export default MedicineDetails