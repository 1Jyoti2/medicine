import { Inbox } from 'lucide-react'

function EmptyState({
  icon: Icon = Inbox,
  title = 'Nothing here yet',
  description,
  action,
  className = '',
}) {
  return (
    <div
      className={`flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-200 bg-white px-6 py-14 text-center ${className}`}
    >
      <span className="grid size-14 place-items-center rounded-2xl bg-slate-100 text-slate-400">
        <Icon aria-hidden className="size-7" />
      </span>
      {title && (
        <h3 className="mt-4 text-lg font-bold text-slate-800">{title}</h3>
      )}
      {description && (
        <p className="mt-2 max-w-sm text-sm text-slate-500">{description}</p>
      )}
      {action && <div className="mt-6">{action}</div>}
    </div>
  )
}

export default EmptyState