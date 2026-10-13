import { Calendar, LogOut, Mail, ShieldCheck, User as UserIcon } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import Button from '../components/Button.jsx'
import BackButton from '../components/BackButton.jsx'
import Card from '../components/Card.jsx'
import SectionHeader from '../components/SectionHeader.jsx'
import useAuth from '../context/useAuth.js'

function initials(name) {
  if (!name) return '?'
  return name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')
}

function Profile() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  if (!user) return null

  const joinedAt = user.createdAt
    ? new Date(user.createdAt).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : null

  function handleLogout() {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
      <BackButton className="mb-10" />

      <div className="mb-10">
        <SectionHeader
          eyebrow="Account"
          title="Your Profile"
          subtitle="View the details of your MedScan AI account."
        />
      </div>

      <Card className="overflow-hidden p-0">
        <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-900 px-6 py-8 sm:px-8">
          <div className="flex flex-wrap items-center gap-4">
            <span className="grid size-16 place-items-center rounded-2xl bg-white/10 text-2xl font-extrabold text-emerald-300 ring-1 ring-white/10">
              {initials(user.name)}
            </span>
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-emerald-300">
                Welcome back
              </p>
              <h2 className="mt-0.5 text-2xl font-extrabold text-white">
                {user.name}
              </h2>
              <p className="text-sm text-slate-400">{user.email}</p>
            </div>
          </div>
        </div>

        <div className="p-6 sm:p-8">
          <h3 className="text-sm font-bold uppercase tracking-wide text-slate-500">
            Account Details
          </h3>

          <dl className="mt-4 space-y-3">
            <div className="flex items-start gap-3 rounded-xl border border-slate-100 bg-slate-50 px-4 py-3">
              <UserIcon className="mt-0.5 size-5 shrink-0 text-emerald-600" />
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500">
                  Full name
                </dt>
                <dd className="font-semibold text-slate-800">{user.name}</dd>
              </div>
            </div>

            <div className="flex items-start gap-3 rounded-xl border border-slate-100 bg-slate-50 px-4 py-3">
              <Mail className="mt-0.5 size-5 shrink-0 text-emerald-600" />
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500">
                  Email address
                </dt>
                <dd className="font-semibold text-slate-800">{user.email}</dd>
              </div>
            </div>

            <div className="flex items-start gap-3 rounded-xl border border-slate-100 bg-slate-50 px-4 py-3">
              <Calendar className="mt-0.5 size-5 shrink-0 text-emerald-600" />
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500">
                  Member since
                </dt>
                <dd className="font-semibold text-slate-800">
                  {joinedAt ?? '—'}
                </dd>
              </div>
            </div>
          </dl>

          <div className="mt-6 flex items-start gap-3 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3">
            <ShieldCheck className="mt-0.5 size-5 shrink-0 text-emerald-600" />
            <p className="text-xs leading-relaxed text-emerald-800">
              This is a mock account stored only in your browser&apos;s local
              storage. No personal data is sent to or stored on any server.
            </p>
          </div>

          <div className="mt-8 flex flex-wrap gap-3">
            <Button onClick={handleLogout} variant="danger" icon={LogOut}>
              Log Out
            </Button>
            <Button to="/" variant="outline">
              Back to Home
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}

export default Profile