import { FlaskConical, Leaf, ShieldAlert, Sparkles } from 'lucide-react'

import Card from './Card.jsx'

function RemedyDetail({ icon: Icon, iconClasses, title, children }) {
  return (
    <div>
      <h4 className="flex items-center gap-2 text-sm font-bold uppercase tracking-wide text-slate-500">
        <span
          className={`grid size-7 shrink-0 place-items-center rounded-lg ${iconClasses}`}
        >
          <Icon aria-hidden className="size-4" />
        </span>
        {title}
      </h4>
      <div className="mt-2 pl-9">{children}</div>
    </div>
  )
}

function RemedyCard({ remedy, className = '' }) {
  return (
    <Card className={`flex h-full flex-col p-5 ${className}`}>
      <div className="flex items-center gap-3">
        <span className="grid size-10 shrink-0 place-items-center rounded-xl bg-emerald-100 text-emerald-700">
          <Leaf aria-hidden className="size-5" />
        </span>
        <h3 className="text-lg font-bold tracking-tight text-slate-900">
          {remedy.name}
        </h3>
      </div>

      <div className="mt-5 flex flex-1 flex-col gap-5">
        <RemedyDetail
          icon={Sparkles}
          iconClasses="bg-emerald-100 text-emerald-700"
          title="Ingredients"
        >
          <ul className="space-y-1.5">
            {remedy.ingredients.map((ingredient) => (
              <li
                key={ingredient}
                className="flex items-start gap-2 text-sm text-slate-700"
              >
                <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-emerald-500" />
                {ingredient}
              </li>
            ))}
          </ul>
        </RemedyDetail>

        <RemedyDetail
          icon={FlaskConical}
          iconClasses="bg-teal-100 text-teal-700"
          title="Preparation"
        >
          <p className="text-sm leading-relaxed text-slate-700">
            {remedy.preparation}
          </p>
        </RemedyDetail>

        <RemedyDetail
          icon={Leaf}
          iconClasses="bg-sky-100 text-sky-700"
          title="Traditional Use"
        >
          <p className="text-sm leading-relaxed text-slate-700">
            {remedy.traditionalUse}
          </p>
        </RemedyDetail>

        <RemedyDetail
          icon={ShieldAlert}
          iconClasses="bg-amber-100 text-amber-700"
          title="Precautions"
        >
          <p className="text-sm leading-relaxed text-amber-800">
            {remedy.precautions}
          </p>
        </RemedyDetail>
      </div>
    </Card>
  )
}

export default RemedyCard