import { Camera, ImagePlus, ScanLine } from 'lucide-react'

import DetectionPage from '../components/DetectionPage.jsx'
import useLanguage from '../context/useLanguage.js'
import { predictLeaf } from '../services/api.js'

function LeafDetection() {
  const { t } = useLanguage()
  return (
    <DetectionPage
      eyebrow={t('leafDetection.eyebrow')}
      title={t('leafDetection.title')}
      subtitle={t('leafDetection.subtitle')}
      predict={predictLeaf}
      resultPath="/result/leaf"
      analyzeLabel={t('detect.analyzeLeaf')}
      analyzingLabel={t('detect.analyzing')}
      uploadIcon={ImagePlus}
      captureIcon={Camera}
      analyzeIcon={ScanLine}
      uploadIconClasses="bg-emerald-100 text-emerald-700"
      captureIconClasses="bg-teal-100 text-teal-700"
    />
  )
}

export default LeafDetection