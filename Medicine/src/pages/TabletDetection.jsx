import { Camera, ImagePlus, Pill } from 'lucide-react'

import DetectionPage from '../components/DetectionPage.jsx'
import useLanguage from '../context/useLanguage.js'
import { predictTablet } from '../services/api.js'

function TabletDetection() {
  const { t } = useLanguage()
  return (
    <DetectionPage
      eyebrow={t('tabletDetection.eyebrow')}
      title={t('tabletDetection.title')}
      subtitle={t('tabletDetection.subtitle')}
      predict={predictTablet}
      resultPath="/result/tablet"
      analyzeLabel={t('detect.analyzeTablet')}
      analyzingLabel={t('detect.analyzing')}
      uploadIcon={ImagePlus}
      captureIcon={Camera}
      analyzeIcon={Pill}
      uploadIconClasses="bg-sky-100 text-sky-700"
      captureIconClasses="bg-blue-100 text-blue-700"
    />
  )
}

export default TabletDetection