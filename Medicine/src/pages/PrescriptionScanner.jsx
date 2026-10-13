import { useState } from 'react'
import { FileText, PenLine, ScanText } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import useImageFile from '../hooks/useImageFile.js'
import useLanguage from '../context/useLanguage.js'
import BackButton from '../components/BackButton.jsx'
import Button from '../components/Button.jsx'
import Card from '../components/Card.jsx'
import Disclaimer from '../components/Disclaimer.jsx'
import ErrorMessage from '../components/ErrorMessage.jsx'
import ImageUploader from '../components/ImageUploader.jsx'
import SectionHeader from '../components/SectionHeader.jsx'
import { scanPrescription } from '../services/api.js'

const SCANNER_ACCEPT_TYPES = ['image/jpeg', 'image/png', 'image/webp']
const SCANNER_FORMATS_MSG =
  'Only JPG, JPEG, PNG and WEBP image files are supported.'

function OcrOverlay() {
  const { t } = useLanguage()
  return (
    <div className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-3 overflow-hidden rounded-2xl border-2 border-emerald-400/40 bg-slate-900/85 text-center backdrop-blur-sm">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-x-4 h-px animate-[scanline_1.6s_ease-in-out_infinite] bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_14px_rgba(52,211,153,0.9)]"
      />
      <span
        aria-hidden
        className="absolute left-2 top-2 size-4 rounded-tl-lg border-l-2 border-t-2 border-emerald-400/80"
      />
      <span
        aria-hidden
        className="absolute right-2 top-2 size-4 rounded-tr-lg border-r-2 border-t-2 border-emerald-400/80"
      />
      <span
        aria-hidden
        className="absolute bottom-2 left-2 size-4 rounded-bl-lg border-b-2 border-l-2 border-emerald-400/80"
      />
      <span
        aria-hidden
        className="absolute bottom-2 right-2 size-4 rounded-br-lg border-b-2 border-r-2 border-emerald-400/80"
      />

      <div className="relative">
        <span className="grid size-16 place-items-center rounded-2xl bg-emerald-400/10 text-emerald-300">
          <ScanText className="size-8" />
        </span>
        <span
          aria-hidden
          className="absolute inset-0 animate-ping rounded-2xl bg-emerald-500/20"
        />
      </div>

      <div>
        <p className="text-xs font-bold uppercase tracking-[0.3em] text-emerald-300">
          {t('rxScanner.overlayTitle')}
        </p>
        <p className="mt-1 text-sm text-slate-300">
          {t('rxScanner.overlayDesc')}
        </p>
      </div>
    </div>
  )
}

function PrescriptionScanner() {
  const navigate = useNavigate()
  const { t } = useLanguage()
  const {
    file,
    previewUrl,
    error,
    handleFile,
    handleRemove,
    clearError,
    reportError,
    fileToDataUrl,
  } = useImageFile({
    acceptTypes: SCANNER_ACCEPT_TYPES,
    formatsMessage: SCANNER_FORMATS_MSG,
  })
  const [isLoading, setIsLoading] = useState(false)

  async function handleScan() {
    if (!file || isLoading) return

    setIsLoading(true)
    clearError()

    try {
      const response = await scanPrescription(file)
      setIsLoading(false)

      if (!response.success) {
        reportError(
          response.message ?? t('rxScanner.error'),
        )
        return
      }

      const imageUrl = await fileToDataUrl(file)
      navigate('/result/prescription', { state: { response, imageUrl } })
    } catch {
      setIsLoading(false)
      reportError(t('rxScanner.genericError'))
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
      <BackButton className="mb-10" />

      <div className="mb-12">
        <SectionHeader
          eyebrow={t('rxScanner.eyebrow')}
          title={t('rxScanner.title')}
          subtitle={t('rxScanner.subtitle')}
        />
      </div>

      <div className="mx-auto max-w-3xl">
        <Card className="p-6 sm:p-8">
          <div className="flex items-center justify-between gap-4">
            <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900">
              <span className="grid size-9 place-items-center rounded-xl bg-violet-100 text-violet-700">
                <FileText className="size-5" />
              </span>
              {t('rxScanner.uploadTitle')}
            </h3>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-violet-50 px-3 py-1.5 text-xs font-bold uppercase tracking-wider text-violet-700 ring-1 ring-violet-200">
              <PenLine className="size-3.5" />
              {t('rxScanner.handwritten')}
            </span>
          </div>

          <div className="relative mt-5">
            <ImageUploader
              onFile={handleFile}
              accept="image/jpeg,image/png,image/webp"
              label={t('rxScanner.uploadLabel')}
              hint={t('rxScanner.uploadHint')}
              preview={previewUrl}
              onClearPreview={handleRemove}
              changeLabel={t('rxScanner.changeImage')}
              disabled={isLoading}
            />
            {isLoading && previewUrl && <OcrOverlay />}
          </div>

          <p className="mt-4 text-xs text-slate-500">
            {t('rxScanner.supportedFormats')}
          </p>

          {error && (
            <ErrorMessage
              className="mt-4"
              message={error}
              onDismiss={clearError}
            />
          )}

          <Button
            onClick={handleScan}
            size="lg"
            icon={ScanText}
            className="mt-6 w-full"
            disabled={!file}
            loading={isLoading}
          >
            {isLoading ? t('rxScanner.scanning') : t('rxScanner.scan')}
          </Button>
        </Card>

        <div className="mt-8 flex justify-center">
          <Disclaimer />
        </div>
      </div>
    </div>
  )
}

export default PrescriptionScanner