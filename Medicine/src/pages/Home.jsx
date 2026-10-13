import { useEffect, useRef, useState } from 'react'
import {
  ArrowRight,
  BrainCircuit,
  CloudUpload,
  FileText,
  Leaf,
  Pill,
  Scan,
  ScanLine,
  ScanText,
  Sparkles,
} from 'lucide-react'

import Button from '../components/Button.jsx'
import Card from '../components/Card.jsx'
import Disclaimer from '../components/Disclaimer.jsx'
import SectionHeader from '../components/SectionHeader.jsx'
import useLanguage from '../context/useLanguage.js'

const features = [
  {
    icon: Leaf,
    titleKey: 'features.leaf.title',
    descriptionKey: 'features.leaf.desc',
    ctaKey: 'features.leaf.cta',
    to: '/leaf-detection',
    accent: 'from-emerald-500 to-teal-600',
    ring: 'group-hover:shadow-emerald-500/20',
    text: 'text-emerald-700',
  },
  {
    icon: Pill,
    titleKey: 'features.tablet.title',
    descriptionKey: 'features.tablet.desc',
    ctaKey: 'features.tablet.cta',
    to: '/tablet-detection',
    accent: 'from-sky-500 to-blue-600',
    ring: 'group-hover:shadow-sky-500/20',
    text: 'text-sky-700',
  },
  {
    icon: ScanText,
    titleKey: 'features.rx.title',
    descriptionKey: 'features.rx.desc',
    ctaKey: 'features.rx.cta',
    to: '/prescription',
    accent: 'from-violet-500 to-fuchsia-600',
    ring: 'group-hover:shadow-violet-500/20',
    text: 'text-violet-700',
  },
]

const steps = [
  {
    number: '01',
    icon: CloudUpload,
    titleKey: 'home.steps.upload.title',
    descriptionKey: 'home.steps.upload.desc',
  },
  {
    number: '02',
    icon: Scan,
    titleKey: 'home.steps.analysis.title',
    descriptionKey: 'home.steps.analysis.desc',
  },
  {
    number: '03',
    icon: BrainCircuit,
    titleKey: 'home.steps.prediction.title',
    descriptionKey: 'home.steps.prediction.desc',
  },
  {
    number: '04',
    icon: FileText,
    titleKey: 'home.steps.display.title',
    descriptionKey: 'home.steps.display.desc',
  },
]

function useInView(threshold = 0.15) {
  const ref = useRef(null)
  const [inView, setInView] = useState(false)

  useEffect(() => {
    const element = ref.current
    if (!element) return undefined

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true)
          observer.unobserve(element)
        }
      },
      { threshold },
    )

    observer.observe(element)
    return () => observer.disconnect()
  }, [threshold])

  return [ref, inView]
}

function Reveal({ children, delay = 0, className = '' }) {
  const [ref, inView] = useInView()

  return (
    <div
      ref={ref}
      style={{ transitionDelay: `${delay}ms` }}
      className={`transition-all duration-700 ease-out will-change-transform ${
        inView ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'
      } ${className}`}
    >
      {children}
    </div>
  )
}

function HeroVisual() {
  const { t } = useLanguage()
  const [activeTab, setActiveTab] = useState(0)

  // Auto-cycle through the 3 modalities every 3 seconds
  useEffect(() => {
    const timer = setInterval(() => {
      setActiveTab((prev) => (prev + 1) % 3)
    }, 3200)
    return () => clearInterval(timer)
  }, [])

  return (
    <div className="relative mx-auto w-full max-w-lg">
      <div
        aria-hidden
        className="absolute -inset-6 rounded-[2.5rem] bg-gradient-to-tr from-emerald-500/20 via-teal-400/10 to-sky-400/20 blur-2xl"
      />

      <div className="relative rounded-3xl border border-slate-200 bg-white/80 p-4 shadow-2xl shadow-emerald-500/10 backdrop-blur sm:p-5">
        {/* Main Multi-Modal Dark Viewfinder */}
        <div className="relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 p-4 sm:p-5 shadow-[inset_0_0_40px_rgba(0,0,0,0.9)]">
          {/* Top HUD Status Bar */}
          <div className="relative z-10 flex items-center justify-between pb-3 border-b border-slate-800/80">
            <div className="flex items-center gap-2 rounded-md bg-emerald-400/10 px-2.5 py-1 text-[10px] font-semibold tracking-widest text-emerald-300 backdrop-blur">
              <span className="size-1.5 animate-pulse rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,1)]" />
              {t('hero.visual.scanning')} • MULTI-TARGET
            </div>
            <div className="flex items-center gap-1 text-[10px] font-mono text-slate-400">
              <span className="size-1.5 rounded-full bg-emerald-500" />
              <span>3/3 ONLINE</span>
            </div>
          </div>

          {/* Grid of All 3 Scanning Targets (Leaf, Tablet, Prescription) */}
          <div className="relative z-10 my-4 grid grid-cols-3 gap-2.5 sm:gap-3 py-2">
            {/* Target 1: Medicinal Leaf */}
            <div
              className={`relative flex flex-col items-center justify-center rounded-xl p-3 sm:p-4 transition-all duration-300 ${
                activeTab === 0
                  ? 'border-2 border-emerald-400/80 bg-emerald-950/40 shadow-[0_0_20px_rgba(16,185,129,0.25)] scale-[1.03]'
                  : 'border border-slate-800 bg-slate-900/60 opacity-80'
              }`}
            >
              {/* Corner Reticles */}
              <span className="absolute left-1 top-1 size-2 border-l-2 border-t-2 border-emerald-400" />
              <span className="absolute right-1 top-1 size-2 border-r-2 border-t-2 border-emerald-400" />
              <span className="absolute bottom-1 left-1 size-2 border-b-2 border-l-2 border-emerald-400" />
              <span className="absolute bottom-1 right-1 size-2 border-b-2 border-r-2 border-emerald-400" />

              <div className="relative my-1 grid size-12 sm:size-14 place-items-center rounded-2xl bg-emerald-500/10">
                <Leaf className="size-8 sm:size-9 text-emerald-400 drop-shadow-[0_0_12px_rgba(52,211,153,0.8)]" />
              </div>
              <span className="mt-2 text-[10px] font-bold uppercase tracking-wider text-emerald-300">
                Leaf
              </span>
              <span className="mt-0.5 rounded bg-emerald-400/20 px-1.5 py-0.2 text-[9px] font-mono font-bold text-emerald-200">
                98.6%
              </span>
            </div>

            {/* Target 2: Pharmaceutical Tablet */}
            <div
              className={`relative flex flex-col items-center justify-center rounded-xl p-3 sm:p-4 transition-all duration-300 ${
                activeTab === 1
                  ? 'border-2 border-sky-400/80 bg-sky-950/40 shadow-[0_0_20px_rgba(56,189,248,0.25)] scale-[1.03]'
                  : 'border border-slate-800 bg-slate-900/60 opacity-80'
              }`}
            >
              {/* Corner Reticles */}
              <span className="absolute left-1 top-1 size-2 border-l-2 border-t-2 border-sky-400" />
              <span className="absolute right-1 top-1 size-2 border-r-2 border-t-2 border-sky-400" />
              <span className="absolute bottom-1 left-1 size-2 border-b-2 border-l-2 border-sky-400" />
              <span className="absolute bottom-1 right-1 size-2 border-b-2 border-r-2 border-sky-400" />

              <div className="relative my-1 grid size-12 sm:size-14 place-items-center rounded-2xl bg-sky-500/10">
                <Pill className="size-8 sm:size-9 text-sky-400 drop-shadow-[0_0_12px_rgba(56,189,248,0.8)]" />
              </div>
              <span className="mt-2 text-[10px] font-bold uppercase tracking-wider text-sky-300">
                Tablet
              </span>
              <span className="mt-0.5 rounded bg-sky-400/20 px-1.5 py-0.2 text-[9px] font-mono font-bold text-sky-200">
                97.4%
              </span>
            </div>

            {/* Target 3: Prescription OCR */}
            <div
              className={`relative flex flex-col items-center justify-center rounded-xl p-3 sm:p-4 transition-all duration-300 ${
                activeTab === 2
                  ? 'border-2 border-violet-400/80 bg-violet-950/40 shadow-[0_0_20px_rgba(167,139,250,0.25)] scale-[1.03]'
                  : 'border border-slate-800 bg-slate-900/60 opacity-80'
              }`}
            >
              {/* Corner Reticles */}
              <span className="absolute left-1 top-1 size-2 border-l-2 border-t-2 border-violet-400" />
              <span className="absolute right-1 top-1 size-2 border-r-2 border-t-2 border-violet-400" />
              <span className="absolute bottom-1 left-1 size-2 border-b-2 border-l-2 border-violet-400" />
              <span className="absolute bottom-1 right-1 size-2 border-b-2 border-r-2 border-violet-400" />

              <div className="relative my-1 grid size-12 sm:size-14 place-items-center rounded-2xl bg-violet-500/10">
                <FileText className="size-8 sm:size-9 text-violet-400 drop-shadow-[0_0_12px_rgba(167,139,250,0.8)]" />
              </div>
              <span className="mt-2 text-[10px] font-bold uppercase tracking-wider text-violet-300">
                Rx OCR
              </span>
              <span className="mt-0.5 rounded bg-violet-400/20 px-1.5 py-0.2 text-[9px] font-mono font-bold text-violet-200">
                99.1%
              </span>
            </div>
          </div>

          {/* Bottom Scanner Readout Bar */}
          <div className="relative z-10 flex items-center justify-between pt-2.5 border-t border-slate-800/80 text-[10px] font-mono text-slate-400">
            <span className="text-emerald-400">
              {activeTab === 0
                ? 'SCAN: Stephania / Flora Active'
                : activeTab === 1
                  ? 'SCAN: Paracetamol 500mg Match'
                  : 'SCAN: Clinical Text Parsed'}
            </span>
            <span className="text-slate-500">OOD: VALID</span>
          </div>

          {/* Background Grid Pattern */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_right,rgba(16,185,129,0.08)_1px,transparent_1px),linear-gradient(to_bottom,rgba(16,185,129,0.08)_1px,transparent_1px)] bg-[size:16px_16px]"
          />

          {/* Animated Sweeping Laser Scan Line */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-x-0 h-0.5 animate-[scanline_3.2s_ease-in-out_infinite] bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_16px_rgba(52,211,153,0.9)]"
          />

          {/* Viewfinder Outer Corner Brackets */}
          <span
            aria-hidden
            className="absolute left-2 top-2 size-3.5 rounded-tl-lg border-l-2 border-t-2 border-emerald-400/80"
          />
          <span
            aria-hidden
            className="absolute right-2 top-2 size-3.5 rounded-tr-lg border-r-2 border-t-2 border-emerald-400/80"
          />
          <span
            aria-hidden
            className="absolute bottom-2 left-2 size-3.5 rounded-bl-lg border-b-2 border-l-2 border-emerald-400/80"
          />
          <span
            aria-hidden
            className="absolute bottom-2 right-2 size-3.5 rounded-br-lg border-b-2 border-r-2 border-emerald-400/80"
          />
        </div>

        {/* 3 Interactive Buttons below scanner */}
        <div className="mt-4 grid grid-cols-3 gap-2.5 sm:gap-3">
          <button
            type="button"
            onClick={() => setActiveTab(0)}
            className={`rounded-xl border p-2.5 text-center transition-all cursor-pointer ${
              activeTab === 0
                ? 'border-emerald-300 bg-emerald-100/80 ring-2 ring-emerald-400/30'
                : 'border-emerald-100 bg-emerald-50/60 hover:bg-emerald-100/60'
            }`}
          >
            <ScanLine className="mx-auto size-4 text-emerald-600" />
            <p className="mt-1 text-[10px] font-semibold text-emerald-900">
              {t('hero.visual.leafDetected')}
            </p>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab(1)}
            className={`rounded-xl border p-2.5 text-center transition-all cursor-pointer ${
              activeTab === 1
                ? 'border-sky-300 bg-sky-100/80 ring-2 ring-sky-400/30'
                : 'border-sky-100 bg-sky-50/60 hover:bg-sky-100/60'
            }`}
          >
            <Pill className="mx-auto size-4 text-sky-600" />
            <p className="mt-1 text-[10px] font-semibold text-sky-900">
              {t('hero.visual.tabletMatched')}
            </p>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab(2)}
            className={`rounded-xl border p-2.5 text-center transition-all cursor-pointer ${
              activeTab === 2
                ? 'border-violet-300 bg-violet-100/80 ring-2 ring-violet-400/30'
                : 'border-violet-100 bg-violet-50/60 hover:bg-violet-100/60'
            }`}
          >
            <FileText className="mx-auto size-4 text-violet-600" />
            <p className="mt-1 text-[10px] font-semibold text-violet-900">
              {t('hero.visual.rxExtracted')}
            </p>
          </button>
        </div>
      </div>

      {/* Floating Status Badges */}
      <div className="absolute -top-5 right-6 flex items-center gap-1.5 rounded-full border border-slate-100 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-lg shadow-slate-200/60">
        <Sparkles className="size-3.5 text-emerald-600" />
        {t('hero.visual.aiActive')}
      </div>

      <div className="absolute -left-3 top-12 hidden sm:block animate-[floaty_5s_ease-in-out_infinite] rounded-2xl border border-slate-100 bg-white p-3 shadow-xl shadow-slate-200/70 sm:-left-8">
        <div className="flex items-center gap-2.5">
          <span className="grid size-9 place-items-center rounded-xl bg-sky-500/10 text-sky-600">
            <Pill className="size-4.5" />
          </span>
          <div>
            <p className="text-[10px] uppercase tracking-wide text-slate-400">
              {t('hero.visual.tablet')}
            </p>
            <p className="text-xs font-semibold text-slate-800">
              {t('hero.visual.paracetamol')}
            </p>
          </div>
          <span className="ml-1 rounded-md bg-emerald-50 px-1.5 py-0.5 text-[10px] font-bold text-emerald-700">
            94%
          </span>
        </div>
      </div>

      <div className="absolute -right-3 bottom-24 hidden animate-[floaty_6s_ease-in-out_infinite] rounded-2xl border border-slate-100 bg-white p-3 shadow-xl shadow-slate-200/70 sm:-right-8 sm:block">
        <div className="flex items-center gap-2.5">
          <span className="grid size-9 place-items-center rounded-xl bg-violet-500/10 text-violet-600">
            <FileText className="size-4.5" />
          </span>
          <div>
            <p className="text-[10px] uppercase tracking-wide text-slate-400">
              {t('hero.visual.prescription')}
            </p>
            <p className="text-xs font-semibold text-slate-800">
              {t('hero.visual.rx')}
            </p>
          </div>
        </div>
      </div>

      <div className="absolute -bottom-5 left-8 hidden items-center gap-2 rounded-full border border-slate-100 bg-white px-3 py-2 shadow-xl shadow-slate-200/70 sm:flex">
        <BrainCircuit className="size-4 text-emerald-600" />
        <span className="text-xs font-semibold text-slate-700">
          {t('hero.visual.confidence')}
        </span>
      </div>
    </div>
  )
}

function Hero() {
  const { t } = useLanguage()
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-emerald-50/80 via-slate-50 to-white">
      <div aria-hidden className="pointer-events-none absolute inset-0">
        <div className="absolute -left-24 -top-24 size-72 rounded-full bg-emerald-200/40 blur-3xl" />
        <div className="absolute -right-24 top-1/3 size-80 rounded-full bg-teal-200/40 blur-3xl" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(16,185,129,0.08)_1px,transparent_0)] bg-[size:22px_22px]" />
      </div>

      <div className="relative mx-auto grid max-w-7xl items-center gap-14 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:px-8 lg:py-24">
        <div>
          <Reveal>
            <span className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-white px-4 py-1.5 text-xs font-semibold text-emerald-700 shadow-sm">
              <Sparkles className="size-3.5" />
              {t('hero.badge')}
            </span>
          </Reveal>

          <Reveal delay={100}>
            <h1 className="mt-6 text-4xl font-extrabold leading-tight tracking-tight text-slate-900 sm:text-5xl">
              <span className="block">{t('hero.title.line1')}</span>
              <span className="block">
                {t('hero.title.line2')}{' '}
                <span className="text-emerald-700">{t('hero.title.amp')}</span>{' '}
                {t('hero.title.line3')}
              </span>
            </h1>
          </Reveal>

          <Reveal delay={200}>
            <p className="mt-5 max-w-xl text-lg leading-relaxed text-slate-600">
              {t('hero.subtitle')}
            </p>
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Button to="/leaf-detection" size="lg" icon={ScanLine}>
                {t('hero.ctaLeaf')}
              </Button>
              <Button
                to="/tablet-detection"
                size="lg"
                variant="secondary"
                icon={Pill}
              >
                {t('hero.ctaTablet')}
              </Button>
              <Button
                to="/prescription"
                size="lg"
                variant="outline"
                icon={ScanText}
              >
                {t('hero.ctaPrescription')}
              </Button>
            </div>
          </Reveal>

          <Reveal delay={400}>
            <div className="mt-6">
              <Disclaimer />
            </div>
          </Reveal>
        </div>

        <Reveal delay={250}>
          <HeroVisual />
        </Reveal>
      </div>
    </section>
  )
}

function Features() {
  const { t } = useLanguage()
  return (
    <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
      <Reveal>
        <SectionHeader
          eyebrow={t('features.eyebrow')}
          title={t('features.title')}
          subtitle={t('features.subtitle')}
        />
      </Reveal>

      <div className="mt-14 grid gap-8 md:grid-cols-3">
        {features.map((feature, index) => (
          <Reveal key={feature.titleKey} delay={index * 120}>
            <Card
              hover
              className={`group flex h-full flex-col p-8 ${feature.ring}`}
            >
              <span
                className={`grid size-14 place-items-center rounded-2xl bg-gradient-to-br ${feature.accent} text-white shadow-lg transition-transform duration-300 group-hover:scale-105`}
              >
                <feature.icon className="size-7" />
              </span>

              <h3 className="mt-6 text-xl font-bold text-slate-900">
                {t(feature.titleKey)}
              </h3>
              <p className="mt-3 flex-1 leading-relaxed text-slate-600">
                {t(feature.descriptionKey)}
              </p>

              <Button
                to={feature.to}
                variant="ghost"
                icon={ArrowRight}
                iconPosition="right"
                className="mt-6 self-start"
              >
                {t(feature.ctaKey)}
              </Button>
            </Card>
          </Reveal>
        ))}
      </div>
    </section>
  )
}

function HowItWorks() {
  const { t } = useLanguage()
  return (
    <section className="border-y border-slate-100 bg-white py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <Reveal>
          <SectionHeader
            eyebrow={t('home.howItWorks.eyebrow')}
            title={t('home.howItWorks.title')}
            subtitle={t('home.howItWorks.subtitle')}
          />
        </Reveal>

        <div className="relative mt-14 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <div
            aria-hidden
            className="absolute left-10 right-10 top-8 hidden border-t-2 border-dashed border-emerald-200 lg:block"
          />
          {steps.map((step, index) => (
            <Reveal key={step.number} delay={index * 120}>
              <div className="group relative text-center">
                <div className="relative mx-auto grid size-16 place-items-center">
                  <span
                    aria-hidden
                    className="absolute inset-0 rounded-2xl bg-emerald-100 transition-transform duration-300 group-hover:rotate-6 group-hover:scale-110"
                  />
                  <step.icon className="relative size-7 text-emerald-700" />
                  <span className="absolute -right-2 -top-2 grid size-6 place-items-center rounded-full bg-emerald-700 text-[0.6rem] font-bold text-white shadow-md shadow-emerald-700/30">
                    {step.number}
                  </span>
                </div>
                <h3 className="mt-5 text-lg font-bold text-slate-900">
                  {t(step.titleKey)}
                </h3>
                <p className="mx-auto mt-2 max-w-[16rem] text-sm leading-relaxed text-slate-600">
                  {t(step.descriptionKey)}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}

function Cta() {
  const { t } = useLanguage()
  return (
    <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
      <Reveal>
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-700 via-emerald-600 to-teal-600 px-8 py-16 text-center shadow-2xl shadow-emerald-700/20">
          <div aria-hidden className="pointer-events-none absolute inset-0">
            <div className="absolute -left-16 -top-16 size-56 rounded-full bg-white/10 blur-3xl" />
            <div className="absolute -bottom-20 -right-10 size-64 rounded-full bg-teal-300/20 blur-3xl" />
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(255,255,255,0.12)_1px,transparent_0)] bg-[size:20px_20px]" />
          </div>

          <div className="relative">
            <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
              {t('cta.title')}
            </h2>
            <p className="mx-auto mt-4 max-w-xl text-emerald-100">
              {t('cta.subtitle')}
            </p>
            <Button
              to="/leaf-detection"
              size="lg"
              variant="light"
              icon={ArrowRight}
              iconPosition="right"
              className="mt-8"
            >
              {t('cta.button')}
            </Button>
          </div>
        </div>
      </Reveal>
    </section>
  )
}

function Home() {
  return (
    <div className="overflow-x-clip">
      <Hero />
      <Features />
      <HowItWorks />
      <Cta />
    </div>
  )
}

export default Home