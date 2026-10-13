import { Leaf } from 'lucide-react'

import Card from './Card.jsx'
import Disclaimer from './Disclaimer.jsx'
import RemedyCard from './RemedyCard.jsx'
import SectionHeader from './SectionHeader.jsx'

const REMEDIES_DISCLAIMER =
  'These traditional preparations are provided for informational purposes only and are not a substitute for professional medical advice, diagnosis, or treatment.'

function TraditionalRemedies({ remedies = [], id = 'traditional-remedies' }) {
  if (!Array.isArray(remedies) || remedies.length === 0) {
    return (
      <section id={id} className="mt-16 scroll-mt-16">
        <SectionHeader
          eyebrow="Herbal Traditions"
          title="Traditional Remedies"
          subtitle="Traditional preparation practices shared for informational purposes."
        />
        <Card className="mx-auto mt-8 flex max-w-2xl flex-col items-center gap-3 p-8 text-center">
          <span className="grid size-12 place-items-center rounded-2xl bg-emerald-50 text-emerald-700">
            <Leaf aria-hidden className="size-6" />
          </span>
          <p className="text-sm text-slate-600">
            No traditional preparations are currently available for this plant.
          </p>
        </Card>
        <div className="mt-6 flex justify-center">
          <Disclaimer>{REMEDIES_DISCLAIMER}</Disclaimer>
        </div>
      </section>
    )
  }

  return (
    <section id={id} className="mt-16 scroll-mt-16">
      <SectionHeader
        eyebrow="Herbal Traditions"
        title="Traditional Remedies"
        subtitle="Traditional preparation practices for this plant, shared for informational purposes."
      />

      <div className="mt-10 grid gap-6 md:grid-cols-2">
        {remedies.map((remedy) => (
          <RemedyCard key={remedy.name} remedy={remedy} />
        ))}
      </div>

      <div className="mt-8 flex justify-center">
        <Disclaimer>{REMEDIES_DISCLAIMER}</Disclaimer>
      </div>
    </section>
  )
}

export default TraditionalRemedies