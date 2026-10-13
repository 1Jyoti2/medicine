import {
  ArrowRight,
  Bot,
  Camera,
  Database,
  FileSearch,
  Layers,
  Microscope,
  Upload,
} from 'lucide-react'

import Card from '../components/Card.jsx'
import BackButton from '../components/BackButton.jsx'
import Disclaimer from '../components/Disclaimer.jsx'
import SectionHeader from '../components/SectionHeader.jsx'
import useLanguage from '../context/useLanguage.js'

const steps = [
  {
    number: '01',
    titleKey: 'hiw.steps.upload.title',
    descriptionKey: 'hiw.steps.upload.desc',
    icon: Upload,
    color: 'from-emerald-500 to-teal-600',
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    accent: 'bg-emerald-500',
  },
  {
    number: '02',
    titleKey: 'hiw.steps.analysis.title',
    descriptionKey: 'hiw.steps.analysis.desc',
    icon: Microscope,
    color: 'from-sky-500 to-blue-600',
    bg: 'bg-sky-50',
    text: 'text-sky-700',
    accent: 'bg-sky-500',
  },
  {
    number: '03',
    titleKey: 'hiw.steps.prediction.title',
    descriptionKey: 'hiw.steps.prediction.desc',
    icon: Bot,
    color: 'from-violet-500 to-indigo-600',
    bg: 'bg-violet-50',
    text: 'text-violet-700',
    accent: 'bg-violet-500',
  },
  {
    number: '04',
    titleKey: 'hiw.steps.display.title',
    descriptionKey: 'hiw.steps.display.desc',
    icon: Layers,
    color: 'from-amber-500 to-orange-600',
    bg: 'bg-amber-50',
    text: 'text-amber-700',
    accent: 'bg-amber-500',
  },
]

function StepCard({ step, isLast, t }) {
  const { number, titleKey, descriptionKey, icon: Icon, color } = step

  return (
    <div className="relative grid gap-6 md:grid-cols-[auto_1fr]">
      <div className="flex flex-col items-center">
        <span
          className={`grid size-14 place-items-center rounded-2xl bg-gradient-to-br ${color} text-white shadow-lg`}
        >
          <Icon aria-hidden className="size-7" />
        </span>
        {!isLast && (
          <div className="mt-2 hidden w-0.5 flex-1 rounded-full bg-slate-200 md:block" />
        )}
      </div>

      <Card className="p-6 sm:p-7">
        <div className="flex items-center gap-3">
          <span className="rounded-lg bg-slate-900 px-2 py-0.5 text-xs font-bold tabular-nums text-white">
            {number}
          </span>
          <h3 className="text-lg font-bold text-slate-900">{t(titleKey)}</h3>
        </div>
        <p className="mt-3 text-sm leading-relaxed text-slate-600">
          {t(descriptionKey)}
        </p>
      </Card>

      {!isLast && (
        <div className="flex justify-center md:hidden">
          <ArrowRight aria-hidden className="size-5 rotate-90 text-slate-300" />
        </div>
      )}
    </div>
  )
}

function HowItWorks() {
  const { t } = useLanguage()
  return (
    <div className="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:px-8">
      <BackButton className="mb-12" />

      <div className="mb-14">
        <SectionHeader
          eyebrow={t('hiw.eyebrow')}
          title={t('hiw.title')}
          subtitle={t('hiw.subtitle')}
        />
      </div>

      <div className="relative space-y-6 md:space-y-0">
        {steps.map((step, index) => (
          <StepCard
            key={step.number}
            step={step}
            isLast={index === steps.length - 1}
            t={t}
          />
        ))}
      </div>

      <div className="mt-14 grid gap-6 sm:grid-cols-3">
        <Card className="p-6 text-center">
          <span className="mx-auto grid size-11 place-items-center rounded-xl bg-emerald-100 text-emerald-700">
            <Camera className="size-5.5" />
          </span>
          <h4 className="mt-3 text-sm font-bold text-slate-900">
            {t('hiw.cards.camera.title')}
          </h4>
          <p className="mt-1.5 text-xs leading-relaxed text-slate-500">
            {t('hiw.cards.camera.desc')}
          </p>
        </Card>

        <Card className="p-6 text-center">
          <span className="mx-auto grid size-11 place-items-center rounded-xl bg-sky-100 text-sky-700">
            <FileSearch className="size-5.5" />
          </span>
          <h4 className="mt-3 text-sm font-bold text-slate-900">
            {t('hiw.cards.ocr.title')}
          </h4>
          <p className="mt-1.5 text-xs leading-relaxed text-slate-500">
            {t('hiw.cards.ocr.desc')}
          </p>
        </Card>

        <Card className="p-6 text-center">
          <span className="mx-auto grid size-11 place-items-center rounded-xl bg-violet-100 text-violet-700">
            <Database className="size-5.5" />
          </span>
          <h4 className="mt-3 text-sm font-bold text-slate-900">
            {t('hiw.cards.details.title')}
          </h4>
          <p className="mt-1.5 text-xs leading-relaxed text-slate-500">
            {t('hiw.cards.details.desc')}
          </p>
        </Card>
      </div>

      <div className="mt-10 flex justify-center">
        <Disclaimer />
      </div>
    </div>
  )
}

export default HowItWorks