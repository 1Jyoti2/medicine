import { Construction, ScanLine } from 'lucide-react'

import Button from '../components/Button.jsx'
import Card from '../components/Card.jsx'

function ComingSoon({ title, description }) {
  return (
    <div className="flex min-h-[70vh] items-center justify-center px-4 py-16">
      <Card className="max-w-xl p-10 text-center">
        <span className="mx-auto grid size-16 place-items-center rounded-2xl bg-emerald-50 text-emerald-600">
          <Construction className="size-8" />
        </span>
        <h1 className="mt-6 text-2xl font-bold text-slate-900 sm:text-3xl">
          {title}
        </h1>
        <p className="mx-auto mt-3 max-w-md text-slate-600">
          {description ??
            'This feature is still under construction and will be available soon.'}
        </p>
        <Button to="/" icon={ScanLine} className="mt-8">
          Back to Home
        </Button>
      </Card>
    </div>
  )
}

export default ComingSoon