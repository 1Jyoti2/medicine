import { useState } from 'react'
import { Camera, ImagePlus, ScanLine } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import useImageFile from '../hooks/useImageFile.js'
import useLanguage from '../context/useLanguage.js'
import BackButton from './BackButton.jsx'
import Button from './Button.jsx'
import CameraCapture from './CameraCapture.jsx'
import Card from './Card.jsx'
import Disclaimer from './Disclaimer.jsx'
import ErrorMessage from './ErrorMessage.jsx'
import ImageUploader from './ImageUploader.jsx'
import SectionHeader from './SectionHeader.jsx'

function DetectionPage({
  eyebrow,
  title,
  subtitle,
  predict,
  resultPath,
  analyzeLabel,
  analyzingLabel,
  uploadIcon: UploadIcon = ImagePlus,
  captureIcon: CaptureIcon = Camera,
  analyzeIcon: AnalyzeIcon = ScanLine,
  uploadIconClasses = 'bg-emerald-100 text-emerald-700',
  captureIconClasses = 'bg-teal-100 text-teal-700',
}) {
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
  } = useImageFile()
  const [isLoading, setIsLoading] = useState(false)

  const finalAnalyzeLabel = analyzeLabel ?? t('detect.analyze')
  const finalAnalyzingLabel = analyzingLabel ?? t('detect.analyzing')

  async function handleAnalyze() {
    if (!file || isLoading) return

    setIsLoading(true)
    clearError()

    try {
      const response = await predict(file)
      setIsLoading(false)

      if (!response.success) {
        reportError(
          response.message ?? 'Unable to analyze the image. Please try again.',
        )
        return
      }

      const imageUrl = await fileToDataUrl(file)
      navigate(resultPath, { state: { response, imageUrl } })
    } catch {
      setIsLoading(false)
      reportError(
        'Something went wrong while analyzing the image. Please try again.',
      )
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
      <BackButton className="mb-10" />

      <div className="mb-12">
        <SectionHeader eyebrow={eyebrow} title={title} subtitle={subtitle} />
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card className="p-6 sm:p-8">
          <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900">
            <span
              className={`grid size-9 place-items-center rounded-xl ${uploadIconClasses}`}
            >
              <UploadIcon className="size-5" />
            </span>
            {t('detect.uploadTitle')}
          </h3>

          <ImageUploader
            onFile={handleFile}
            accept="image/jpeg,image/png"
            label={t('detect.uploadLabel')}
            hint={t('detect.uploadHint')}
            preview={previewUrl}
            onClearPreview={handleRemove}
            disabled={isLoading}
            className="mt-5"
          />

          <p className="mt-4 text-xs text-slate-500">
            {t('detect.supportedFormats')}
          </p>

          {error && (
            <ErrorMessage
              className="mt-4"
              message={error}
              onDismiss={clearError}
            />
          )}

          <Button
            onClick={handleAnalyze}
            size="lg"
            icon={AnalyzeIcon}
            className="mt-6 w-full"
            disabled={!file}
            loading={isLoading}
          >
            {isLoading ? finalAnalyzingLabel : finalAnalyzeLabel}
          </Button>
        </Card>

        <Card className="p-6 sm:p-8">
          <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900">
            <span
              className={`grid size-9 place-items-center rounded-xl ${captureIconClasses}`}
            >
              <CaptureIcon className="size-5" />
            </span>
            {t('detect.captureTitle')}
          </h3>

          <CameraCapture
            onCapture={handleFile}
            disabled={isLoading}
            className="mt-5"
          />

          <p className="mt-4 text-xs text-slate-500">
            {t('detect.captureHint')}
          </p>
        </Card>
      </div>

      <div className="mt-10 flex justify-center">
        <Disclaimer />
      </div>
    </div>
  )
}

export default DetectionPage