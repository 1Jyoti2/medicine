import { Pill } from 'lucide-react'
import { useLocation } from 'react-router-dom'

import Button from '../components/Button.jsx'
import Card from '../components/Card.jsx'
import EmptyState from '../components/EmptyState.jsx'
import ResultDashboard from '../components/ResultDashboard.jsx'
import {
  buildTabletReport,
  TABLET_FILE_NAME,
} from '../utils/pdfReport.js'

function TabletResult() {
  const location = useLocation()
  const { response, imageUrl } = location.state ?? {}
  const result = response?.data
  const medicine = result?.medicine

  if (!response || !medicine) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
        <EmptyState
          icon={Pill}
          title="No result to display"
          description="Run a tablet detection first, then your result will appear here."
          action={
            <Button to="/tablet-detection">Go to Tablet Detection</Button>
          }
        />
      </div>
    )
  }

  return (
    <ResultDashboard
      icon={Pill}
      eyebrow="Prediction Result"
      title="Pharmaceutical Tablet Identification"
      typeLabel="Pharmaceutical Tablet"
      resultName={medicine.name}
      resultDetail={medicine.genericName}
      confidence={result.confidence}
      imageUrl={imageUrl}
      imageAlt={`Uploaded tablet image identified as ${medicine.name}`}
      status={result.status}
      response={response}
      result={result}
      scanAnotherPath="/tablet-detection"
      scanAnotherLabel="Scan Another Tablet"
      onDownloadReport={() =>
        buildTabletReport({ medicine, result, imageUrl })
      }
      pdfFileName={TABLET_FILE_NAME}
    >
      <div className="grid gap-6 sm:grid-cols-2">
        <Card className="p-5">
          <h4 className="text-sm font-bold uppercase tracking-wide text-slate-500">
            Common Uses
          </h4>
          <ul className="mt-3 space-y-2">
            {medicine.uses.map((use) => (
              <li
                key={use}
                className="flex items-start gap-2 text-sm text-slate-700"
              >
                <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-sky-500" />
                {use}
              </li>
            ))}
          </ul>

          <h4 className="mt-5 text-sm font-bold uppercase tracking-wide text-slate-500">
            Possible Side Effects
          </h4>
          <ul className="mt-3 space-y-2">
            {medicine.sideEffects.map((sideEffect) => (
              <li
                key={sideEffect}
                className="flex items-start gap-2 text-sm text-slate-700"
              >
                <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-rose-400" />
                {sideEffect}
              </li>
            ))}
          </ul>
        </Card>

        <Card className="p-5">
          <h4 className="text-sm font-bold uppercase tracking-wide text-slate-500">
            Details
          </h4>
          <dl className="mt-3 space-y-2 text-sm">
            <div className="flex justify-between gap-4">
              <dt className="text-slate-500">Category</dt>
              <dd className="text-right font-medium text-slate-800">
                {medicine.category}
              </dd>
            </div>
            <div className="flex justify-between gap-4">
              <dt className="text-slate-500">Composition</dt>
              <dd className="text-right font-medium text-slate-800">
                {medicine.composition}
              </dd>
            </div>
            <div className="flex justify-between gap-4">
              <dt className="text-slate-500">Storage</dt>
              <dd className="text-right font-medium text-slate-800">
                {medicine.storage}
              </dd>
            </div>
            <div className="flex justify-between gap-4">
              <dt className="text-slate-500">Manufacturer</dt>
              <dd className="text-right font-medium text-slate-800">
                {medicine.manufacturer}
              </dd>
            </div>
          </dl>
        </Card>
      </div>

      <p className="mt-6 text-sm leading-relaxed text-slate-500">
        {medicine.description}
      </p>

      {medicine.precautions?.length > 0 && (
        <p className="mt-3 text-xs text-amber-700">
          Precautions: {medicine.precautions.join(', ')}
        </p>
      )}

      <div className="mt-8 flex flex-wrap items-center justify-between gap-4 border-t border-slate-100 pt-5">
        <p className="text-sm text-slate-500">
          Want the full profile, dosage and storage information?
        </p>
        <Button
          to={`/medicine/${encodeURIComponent(medicine.name)}`}
          variant="secondary"
          size="sm"
        >
          Open Medicine Guide
        </Button>
      </div>
    </ResultDashboard>
  )
}

export default TabletResult