import { Leaf, ScanLine } from 'lucide-react'
import { useLocation } from 'react-router-dom'

import Button from '../components/Button.jsx'
import Card from '../components/Card.jsx'
import EmptyState from '../components/EmptyState.jsx'
import ResultDashboard from '../components/ResultDashboard.jsx'
import TraditionalRemedies from '../components/TraditionalRemedies.jsx'
import { getPlantRemedies } from '../utils/plantRemedies.js'
import {
  buildLeafReport,
  LEAF_FILE_NAME,
} from '../utils/pdfReport.js'

function LeafResult() {
  const location = useLocation()
  const { response, imageUrl } = location.state ?? {}
  const result = response?.data
  const plant = result?.plant
  const remedies = getPlantRemedies(plant)
  const enrichedPlant = plant ? { ...plant, remedies } : null

  if (!response || !plant) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
        <EmptyState
          icon={Leaf}
          title="No result to display"
          description="Run a leaf detection first, then your result will appear here."
          action={
            <Button to="/leaf-detection" icon={ScanLine}>
              Go to Leaf Detection
            </Button>
          }
        />
      </div>
    )
  }

  return (
    <ResultDashboard
      icon={Leaf}
      eyebrow="Prediction Result"
      title="Medicinal Leaf Identification"
      typeLabel="Medicinal Leaf"
      resultName={plant.name}
      resultDetail={plant.scientificName}
      confidence={result.confidence}
      imageUrl={imageUrl}
      imageAlt={`Uploaded leaf image identified as ${plant.name}`}
      status={result.status}
      response={response}
      result={result}
      scanAnotherPath="/leaf-detection"
      scanAnotherLabel="Scan Another Leaf"
      onDownloadReport={() =>
        buildLeafReport({ plant: enrichedPlant, result, imageUrl })
      }
      pdfFileName={LEAF_FILE_NAME}
    >
      <div className="grid gap-6 sm:grid-cols-2">
        <Card className="p-5">
          <h4 className="text-sm font-bold uppercase tracking-wide text-slate-500">
            Common Uses
          </h4>
          <ul className="mt-3 space-y-2">
            {plant.uses.map((use) => (
              <li
                key={use}
                className="flex items-start gap-2 text-sm text-slate-700"
              >
                <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-emerald-500" />
                {use}
              </li>
            ))}
          </ul>

          {plant.sideEffects?.length > 0 && (
            <>
              <h4 className="mt-5 text-sm font-bold uppercase tracking-wide text-slate-500">
                Possible Side Effects
              </h4>
              <ul className="mt-3 space-y-2">
                {plant.sideEffects.map((sideEffect) => (
                  <li
                    key={sideEffect}
                    className="flex items-start gap-2 text-sm text-slate-700"
                  >
                    <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-rose-400" />
                    {sideEffect}
                  </li>
                ))}
              </ul>
            </>
          )}
        </Card>

        <div className="space-y-6">
          <Card className="p-5">
            <h4 className="text-sm font-bold uppercase tracking-wide text-slate-500">
              Active Compounds
            </h4>
            <div className="mt-3 flex flex-wrap gap-2">
              {plant.activeCompounds.map((compound) => (
                <span
                  key={compound}
                  className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700"
                >
                  {compound}
                </span>
              ))}
            </div>
          </Card>

          <Card className="p-5">
            <h4 className="text-sm font-bold uppercase tracking-wide text-slate-500">
              Plant Details
            </h4>
            <dl className="mt-3 space-y-2 text-sm">
              <div className="flex justify-between gap-4">
                <dt className="text-slate-500">Family</dt>
                <dd className="font-medium text-slate-800">{plant.family}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-slate-500">Native region</dt>
                <dd className="text-right font-medium text-slate-800">
                  {plant.nativeRegion}
                </dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-slate-500">Parts used</dt>
                <dd className="text-right font-medium text-slate-800">
                  {plant.partsUsed}
                </dd>
              </div>
            </dl>
          </Card>
        </div>
      </div>

      <p className="mt-6 text-sm leading-relaxed text-slate-500">
        {plant.description}
      </p>

      {plant.precautions?.length > 0 && (
        <p className="mt-3 text-xs text-slate-500">
          Precautions: {plant.precautions.join(', ')}
        </p>
      )}

      {remedies.length > 0 && (
        <div className="mt-8 border-t border-slate-100 pt-6">
          <TraditionalRemedies remedies={remedies} id="leaf-result-remedies" />
        </div>
      )}

      <div className="mt-8 flex flex-wrap items-center justify-between gap-4 border-t border-slate-100 pt-5">
        <p className="text-sm text-slate-500">
          Want the full profile, storage and care information?
        </p>
        <Button
          to={`/plant/${encodeURIComponent(plant.name)}`}
          variant="secondary"
          size="sm"
        >
          Open Plant Guide
        </Button>
      </div>
    </ResultDashboard>
  )
}

export default LeafResult