import { FileText, PenLine, Pill, ScanText } from 'lucide-react'
import { useLocation } from 'react-router-dom'

import Button from '../components/Button.jsx'
import Card from '../components/Card.jsx'
import EmptyState from '../components/EmptyState.jsx'
import ResultDashboard from '../components/ResultDashboard.jsx'
import {
  buildHandwrittenPrescriptionReport,
  buildPrescriptionReport,
  HANDWRITTEN_PRESCRIPTION_FILE_NAME,
  PRESCRIPTION_FILE_NAME,
} from '../utils/pdfReport.js'
import {
  getMedicineUsage,
  getMedicineSideEffects,
} from '../utils/medicineLookup.js'

function PrescriptionResult() {
  const location = useLocation()
  const { response, imageUrl } = location.state ?? {}
  const prescription = response?.data
  const isHandwritten = Boolean(prescription?.isHandwritten)

  if (!response || !prescription || !Array.isArray(prescription.medicines)) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
        <EmptyState
          icon={FileText}
          title="No prescription to display"
          description="Scan a prescription first, then the extracted medicine information will appear here."
          action={
            <Button to="/prescription" icon={ScanText}>
              Go to Prescription Scanner
            </Button>
          }
        />
      </div>
    )
  }

  const meta = isHandwritten
    ? [
        { label: 'Patient', value: prescription.patientName },
        { label: 'Doctor', value: prescription.doctorName },
        { label: 'Organization', value: prescription.organization },
        { label: 'Prescription No.', value: prescription.prescriptionNumber },
        { label: 'Date', value: prescription.issuedDate },
      ].filter((item) => Boolean(item.value))
    : [
        {
          label: 'Patient',
          value: `${prescription.patientName} (${prescription.patientAge})`,
        },
        { label: 'Doctor', value: prescription.doctorName },
        { label: 'Organization', value: prescription.organization },
        { label: 'Prescription No.', value: prescription.prescriptionNumber },
      ]

  return (
    <ResultDashboard
      icon={isHandwritten ? PenLine : FileText}
      eyebrow={isHandwritten ? 'Handwritten Prescription' : 'OCR Result'}
      title={
        isHandwritten ? 'Handwritten Prescription' : 'Prescription Extracted'
      }
      typeLabel={isHandwritten ? 'Handwritten Prescription' : 'Prescription'}
      resultName={prescription.prescriptionNumber}
      resultDetail={`Issued on ${prescription.issuedDate}`}
      confidence={null}
      imageUrl={imageUrl}
      imageAlt="Uploaded handwritten prescription image"
      status={prescription.status}
      response={response}
      result={prescription}
      meta={meta}
      scanAnotherPath="/prescription"
      scanAnotherLabel="Scan Another Prescription"
      onDownloadReport={() =>
        isHandwritten
          ? buildHandwrittenPrescriptionReport({
              prescription,
              imageUrl,
              disclaimerText:
                'Prescription information shown here is for demonstration purposes only. Handwritten prescriptions should be verified by a qualified healthcare professional before taking any medication.',
            })
          : buildPrescriptionReport({
              prescription,
              imageUrl,
              disclaimerText:
                'Some prescription text may be unclear. Please verify the extracted information.',
            })
      }
      pdfFileName={
        isHandwritten
          ? HANDWRITTEN_PRESCRIPTION_FILE_NAME
          : PRESCRIPTION_FILE_NAME
      }
      disclaimer={
        isHandwritten
          ? 'Prescription information shown here is for demonstration purposes only. Handwritten prescriptions should be verified by a qualified healthcare professional before taking any medication.'
          : 'Some prescription text may be unclear. Please verify the extracted information.'
      }
    >
      <div className="space-y-8">

        <div>
          <h4 className="text-sm font-bold uppercase tracking-wide text-slate-500">
            Detected Medicines
          </h4>
          <div className="mt-4 grid gap-6 md:grid-cols-2">
            {prescription.medicines.map((medicine, index) => (
              <Card key={`${medicine.medicineName}-${index}`} className="p-6">
                <div className="flex items-center gap-3">
                  <span className="grid size-11 shrink-0 place-items-center rounded-xl bg-sky-100 text-sky-700">
                    <Pill aria-hidden className="size-5" />
                  </span>
                  <div className="min-w-0">
                    <p className="text-xs uppercase tracking-wide text-slate-400">
                      Medicine {index + 1}
                    </p>
                    <h3 className="truncate font-bold text-slate-900">
                      {medicine.medicineName}
                    </h3>
                  </div>
                </div>

                <dl className="mt-4 divide-y divide-slate-100 text-sm">
                  <div className="flex items-center justify-between gap-4 py-2.5">
                    <dt className="font-medium text-slate-500">Tablet name</dt>
                    <dd className="font-semibold text-slate-800 text-right">
                      {medicine.medicineName}
                    </dd>
                  </div>
                  <div className="flex items-center justify-between gap-4 py-2.5">
                    <dt className="font-medium text-slate-500">Dosage</dt>
                    <dd className="font-medium text-slate-800 text-right">
                      {medicine.dosage || 'As prescribed'}
                    </dd>
                  </div>
                  <div className="flex items-start justify-between gap-4 py-2.5">
                    <dt className="font-medium text-slate-500">Usage</dt>
                    <dd className="max-w-[65%] text-right font-medium text-slate-800">
                      {getMedicineUsage(medicine)}
                    </dd>
                  </div>
                  <div className="flex items-center justify-between gap-4 py-2.5">
                    <dt className="font-medium text-slate-500">Duration</dt>
                    <dd className="font-medium text-slate-800 text-right">
                      {medicine.duration || 'Course duration'}
                    </dd>
                  </div>
                  <div className="flex items-start justify-between gap-4 py-2.5">
                    <dt className="font-medium text-slate-500">Side effects</dt>
                    <dd className="max-w-[65%] text-right font-medium text-rose-600">
                      {getMedicineSideEffects(medicine)}
                    </dd>
                  </div>
                </dl>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </ResultDashboard>
  )
}

export default PrescriptionResult