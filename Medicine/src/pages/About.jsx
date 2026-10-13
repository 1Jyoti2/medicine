import {
  Bot,
  Camera,
  FileSearch,
  FlaskConical,
  GraduationCap,
  Leaf,
  Pill,
  ScanLine,
  Server,
  Shield,
  Sparkles,
} from 'lucide-react'

import Card from '../components/Card.jsx'
import Banner from '../components/Banner.jsx'
import BackButton from '../components/BackButton.jsx'
import Disclaimer from '../components/Disclaimer.jsx'
import useLanguage from '../context/useLanguage.js'

const features = [
  {
    icon: Leaf,
    titleKey: 'about.capabilities.leaf.title',
    descriptionKey: 'about.capabilities.leaf.desc',
    color: 'bg-emerald-100 text-emerald-700',
  },
  {
    icon: Pill,
    titleKey: 'about.capabilities.tablet.title',
    descriptionKey: 'about.capabilities.tablet.desc',
    color: 'bg-sky-100 text-sky-700',
  },
  {
    icon: FileSearch,
    titleKey: 'about.capabilities.rx.title',
    descriptionKey: 'about.capabilities.rx.desc',
    color: 'bg-violet-100 text-violet-700',
  },
  {
    icon: Shield,
    titleKey: 'about.capabilities.ai.title',
    descriptionKey: 'about.capabilities.ai.desc',
    color: 'bg-amber-100 text-amber-700',
  },
]

const futureItems = [
  {
    icon: Bot,
    titleKey: 'about.roadmap.ml.title',
    descriptionKey: 'about.roadmap.ml.desc',
  },
  {
    icon: Server,
    titleKey: 'about.roadmap.backend.title',
    descriptionKey: 'about.roadmap.backend.desc',
  },
  {
    icon: FlaskConical,
    titleKey: 'about.roadmap.eval.title',
    descriptionKey: 'about.roadmap.eval.desc',
  },
  {
    icon: Sparkles,
    titleKey: 'about.roadmap.improve.title',
    descriptionKey: 'about.roadmap.improve.desc',
  },
]

function About() {
  const { t } = useLanguage()
  return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6 lg:px-8">
      <BackButton className="mb-10" />

      <div className="mb-14">
        <Banner eyebrow={t('about.eyebrow')} title={t('banner.title')} />
      </div>

      <Card className="p-8 sm:p-10">
        <div className="flex items-start gap-4">
          <span className="grid size-14 shrink-0 place-items-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 text-white shadow-lg">
            <GraduationCap aria-hidden className="size-7" />
          </span>
          <div>
            <h2 className="text-xl font-bold text-slate-900">
              {t('about.projectTitle')}
            </h2>
            <p className="mt-1 text-sm text-slate-500">
              {t('about.department')}
            </p>
          </div>
        </div>

        <div className="mt-6 space-y-4 text-sm leading-relaxed text-slate-600">
          <p>
            <strong className="text-slate-800">{t('about.title')}</strong>{' '}
            {t('about.para1')}
          </p>
          <p>{t('about.para2')}</p>
        </div>
      </Card>

      <div className="mt-14">
        <div className="mb-8 text-center">
          <h2 className="text-2xl font-bold text-slate-900">
            {t('about.coreTitle')}
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            {t('about.coreSubtitle')}
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {features.map((feature) => {
            const { icon: Icon, titleKey, descriptionKey, color } = feature
            return (
              <Card key={titleKey} className="p-6">
                <div className="flex items-start gap-4">
                  <span
                    className={`grid size-11 shrink-0 place-items-center rounded-xl ${color}`}
                  >
                    <Icon aria-hidden className="size-5.5" />
                  </span>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      {t(titleKey)}
                    </h3>
                    <p className="mt-1.5 text-sm leading-relaxed text-slate-600">
                      {t(descriptionKey)}
                    </p>
                  </div>
                </div>
              </Card>
            )
          })}
        </div>
      </div>

      <div className="mt-14">
        <div className="mb-8 text-center">
          <h2 className="text-2xl font-bold text-slate-900">
            {t('about.howItWorksTitle')}
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            {t('about.howItWorksSubtitle')}
          </p>
        </div>

        <Card className="p-8 sm:p-10">
          <div className="grid items-center gap-8 sm:grid-cols-[1fr_auto_1fr]">
            <div className="text-center">
              <span className="mx-auto grid size-12 place-items-center rounded-2xl bg-emerald-50 text-emerald-700">
                <Camera className="size-6" />
              </span>
              <h4 className="mt-3 text-sm font-bold text-slate-900">
                {t('about.step1.title')}
              </h4>
              <p className="mt-1 text-xs text-slate-500">
                {t('about.step1.desc')}
              </p>
            </div>

            <ArrowDivider />

            <div className="text-center">
              <span className="mx-auto grid size-12 place-items-center rounded-2xl bg-sky-50 text-sky-700">
                <ScanLine className="size-6" />
              </span>
              <h4 className="mt-3 text-sm font-bold text-slate-900">
                {t('about.step2.title')}
              </h4>
              <p className="mt-1 text-xs text-slate-500">
                {t('about.step2.desc')}
              </p>
            </div>

            <ArrowDivider />

            <div className="text-center">
              <span className="mx-auto grid size-12 place-items-center rounded-2xl bg-violet-50 text-violet-700">
                <Bot className="size-6" />
              </span>
              <h4 className="mt-3 text-sm font-bold text-slate-900">
                {t('about.step3.title')}
              </h4>
              <p className="mt-1 text-xs text-slate-500">
                {t('about.step3.desc')}
              </p>
            </div>

            <ArrowDivider />

            <div className="text-center">
              <span className="mx-auto grid size-12 place-items-center rounded-2xl bg-amber-50 text-amber-700">
                <Sparkles className="size-6" />
              </span>
              <h4 className="mt-3 text-sm font-bold text-slate-900">
                {t('about.step4.title')}
              </h4>
              <p className="mt-1 text-xs text-slate-500">
                {t('about.step4.desc')}
              </p>
            </div>
          </div>
        </Card>
      </div>

      <div className="mt-14">
        <div className="mb-8 text-center">
          <h2 className="text-2xl font-bold text-slate-900">
            {t('about.roadmapTitle')}
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            {t('about.roadmapSubtitle')}
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {futureItems.map((item) => {
            const { icon: Icon, titleKey, descriptionKey } = item
            return (
              <Card key={titleKey} className="p-6">
                <div className="flex items-start gap-4">
                  <span className="grid size-11 shrink-0 place-items-center rounded-xl bg-slate-100 text-slate-700">
                    <Icon aria-hidden className="size-5.5" />
                  </span>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      {t(titleKey)}
                    </h3>
                    <p className="mt-1.5 text-sm leading-relaxed text-slate-600">
                      {t(descriptionKey)}
                    </p>
                  </div>
                </div>
              </Card>
            )
          })}
        </div>
      </div>

      <div className="mt-12 flex justify-center">
        <Disclaimer />
      </div>
    </div>
  )
}

function ArrowDivider() {
  return (
    <div className="flex items-center justify-center sm:col-span-full">
      <div className="hidden h-0.5 w-8 rounded-full bg-slate-200 sm:block" />
      <span className="block size-1 rounded-full bg-slate-300 sm:hidden" />
    </div>
  )
}

export default About