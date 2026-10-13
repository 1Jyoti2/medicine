import { Mic, MicOff } from 'lucide-react'

function VoiceButton({
  active = false,
  onToggle,
  disabled = false,
  label = 'Voice input',
  listeningLabel = 'Listening…',
  className = '',
}) {
  return (
    <div className={`relative ${className}`}>
      <button
        type="button"
        aria-label={active ? listeningLabel : label}
        aria-pressed={active}
        disabled={disabled}
        onClick={() => onToggle?.(!active)}
        className={`relative flex size-10 items-center justify-center rounded-full border transition-all duration-200 hover:scale-105 disabled:cursor-not-allowed disabled:opacity-50 ${
          active
            ? 'border-emerald-600 bg-emerald-600 text-white shadow-md shadow-emerald-500/30'
            : 'border-slate-200 bg-white text-slate-600 hover:border-emerald-300 hover:text-emerald-700'
        }`}
      >
        {active ? (
          <MicOff className="size-4.5" aria-hidden />
        ) : (
          <Mic className="size-4.5" aria-hidden />
        )}

        {active && (
          <>
            <span
              aria-hidden
              className="absolute inset-0 -z-10 animate-ping rounded-full bg-emerald-400/40"
            />
            <span
              aria-hidden
              className="absolute inset-0 -z-10 animate-pulse rounded-full bg-emerald-400/20"
            />
          </>
        )}
      </button>

      {active && (
        <span className="pointer-events-none absolute left-1/2 top-full z-50 mt-2 -translate-x-1/2 whitespace-nowrap rounded-lg bg-slate-900 px-2.5 py-1 text-[0.65rem] font-semibold tracking-wide text-white shadow-lg">
          {listeningLabel}
        </span>
      )}
    </div>
  )
}

export default VoiceButton