import { useEffect, useState } from 'react'
import {
  Archive,
  FlaskConical,
  Leaf,
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
import TraditionalRemedies from '../components/TraditionalRemedies.jsx'
import { getPlantDetails } from '../services/api.js'

function PlantImage({ imageUrl, name }) {
  const [failed, setFailed] = useState(false)

  if (!imageUrl || failed) {
    return (
      <div className="grid aspect-square w-full place-items-center bg-gradient-to-br from-emerald-500 to-teal-700 md:h-full md:aspect-auto">
        <Leaf aria-hidden className="size-20 text-white/90" />
        <span className="sr-only">{name}</span>
      </div>
    )
  }

  return (
    <img
      src={imageUrl}
      alt={`${name} plant`}
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

function scrollToRemedies() {
  document
    .getElementById('traditional-remedies')
    ?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function PlantDetails() {
  const { name } = useParams()
  const [request, setRequest] = useState({
    name: null,
    error: null,
    plant: null,
  })

  useEffect(() => {
    let active = true

    getPlantDetails(name)
      .then((response) => {
        if (!active) return
        if (!response.success) {
          setRequest({
            name,
            error: response.message ?? 'Plant details could not be found.',
            plant: null,
          })
        } else {
          setRequest({ name, error: null, plant: response.data })
        }
      })
      .catch(() => {
        if (!active) return
        setRequest({
          name,
          error: 'Unable to load plant details. Please try again later.',
          plant: null,
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
        <LoadingSpinner size="lg" label="Loading plant details…" />
      </div>
    )
  }

  if (request.error || !request.plant) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
        <EmptyState
          icon={Leaf}
          title="Plant not found"
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

  const plant = request.plant

  return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6 lg:px-8">
      <BackButton className="mb-10" />

      <div className="mb-10">
        <SectionHeader
          eyebrow="Medicinal Plant Guide"
          title={plant.name}
          subtitle={`${plant.scientificName} · ${plant.family}`}
        />
      </div>

      <Card className="overflow-hidden p-0">
        <div className="grid md:grid-cols-[minmax(0,320px)_1fr]">
          <PlantImage imageUrl={plant.imageUrl} name={plant.name} />
          <div className="flex flex-col p-6 sm:p-8">
            <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
              Medicinal Plant
            </span>
            <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900">
              {plant.name}
            </h2>
            <p className="mt-1 text-lg italic text-slate-500">
              {plant.scientificName}
            </p>
            <p className="mt-4 text-sm leading-relaxed text-slate-600">
              {plant.description}
            </p>

            <div className="mt-6 flex flex-wrap gap-2">
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600">
                Native: {plant.nativeRegion}
              </span>
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600">
                Parts used: {plant.partsUsed}
              </span>
            </div>

            <div className="mt-auto flex flex-wrap gap-3 pt-6">
              {plant.remedies?.length > 0 && (
                <Button
                  onClick={scrollToRemedies}
                  icon={Sparkles}
                  variant="secondary"
                >
                  View Traditional Remedies
                </Button>
              )}
              <Button to="/leaf-detection" icon={ScanLine}>
                Try Leaf Detection
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
          title="Medicinal Uses"
          icon={Sparkles}
          iconClasses="bg-emerald-100 text-emerald-700"
        >
          <ItemList items={plant.uses} dotClass="bg-emerald-500" />
        </SectionCard>

        <SectionCard
          title="Active Compounds"
          icon={FlaskConical}
          iconClasses="bg-teal-100 text-teal-700"
        >
          <div className="flex flex-wrap gap-2">
            {plant.activeCompounds.map((compound) => (
              <span
                key={compound}
                className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700"
              >
                {compound}
              </span>
            ))}
          </div>
        </SectionCard>

        <SectionCard
          title="Precautions"
          icon={ShieldAlert}
          iconClasses="bg-amber-100 text-amber-700"
        >
          <ItemList items={plant.precautions} dotClass="bg-amber-500" />
        </SectionCard>

        <SectionCard
          title="Side Effects"
          icon={Leaf}
          iconClasses="bg-rose-100 text-rose-700"
        >
          <ItemList items={plant.sideEffects} dotClass="bg-rose-400" />
        </SectionCard>

        <SectionCard
          title="Storage Information"
          icon={Archive}
          iconClasses="bg-sky-100 text-sky-700"
          className="md:col-span-2"
        >
          {plant.storage ? (
            <p className="text-sm leading-relaxed text-slate-700">
              {plant.storage}
            </p>
          ) : (
            <p className="text-sm text-slate-500">
              No specific storage information available.
            </p>
          )}
        </SectionCard>
      </div>

      <TraditionalRemedies remedies={plant.remedies} />

      <div className="mt-16 flex justify-center">
        <Disclaimer />
      </div>
    </div>
  )
}

export default PlantDetails