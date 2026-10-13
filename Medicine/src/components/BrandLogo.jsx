import { Link } from 'react-router-dom'

/**
 * 3-in-1 Multi-Modal Emblem Icon
 * Seamlessly integrates Leaf, Tablet (Pill), and Prescription (Rx)
 */
export function MultiModalIcon({ size = 'md', className = '' }) {
  const sizeClasses =
    size === 'sm'
      ? 'size-8 rounded-lg p-1'
      : size === 'lg'
        ? 'size-11 rounded-2xl p-1.5'
        : 'size-9.5 rounded-xl p-1'

  return (
    <span
      className={`relative grid ${sizeClasses} shrink-0 place-items-center bg-gradient-to-br from-emerald-600 via-teal-700 to-slate-900 shadow-md shadow-emerald-600/30 transition-transform duration-300 group-hover:scale-105 ${className}`}
    >
      <svg
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="size-full drop-shadow-sm"
        aria-hidden="true"
      >
        {/* Subtle background glow circle */}
        <circle cx="20" cy="20" r="18" fill="white" fillOpacity="0.07" />

        {/* 1. Botanical Leaf (Top-Left & Center) */}
        <g>
          <path
            d="M8 25.5C8 16.5 15 9.5 24 9.5C24 18.5 17 25.5 8 25.5Z"
            fill="#34D399"
            fillOpacity="0.95"
          />
          <path
            d="M8 25.5C13 22 17.5 17.5 24 9.5"
            stroke="#064E3B"
            strokeWidth="1.6"
            strokeLinecap="round"
          />
          <path
            d="M13.5 19.5C16.5 19 18.5 17 20 15"
            stroke="#064E3B"
            strokeWidth="1.1"
            strokeLinecap="round"
          />
        </g>

        {/* 2. Pharmaceutical Capsule / Pill (Top-Right) */}
        <g transform="translate(20, 6) rotate(32)">
          <rect
            x="0"
            y="0"
            width="7.5"
            height="14"
            rx="3.75"
            fill="#38BDF8"
            stroke="white"
            strokeWidth="1.2"
          />
          <path
            d="M0 7H7.5V10.25C7.5 12.32 5.82 14 3.75 14C1.68 14 0 12.32 0 10.25V7Z"
            fill="#0284C7"
          />
          <line
            x1="0"
            y1="7"
            x2="7.5"
            y2="7"
            stroke="white"
            strokeWidth="1.2"
          />
        </g>

        {/* 3. Prescription Document / Rx (Bottom-Right) */}
        <g transform="translate(18.5, 18.5)">
          <rect
            x="0"
            y="0"
            width="13.5"
            height="15.5"
            rx="3"
            fill="#8B5CF6"
            stroke="white"
            strokeWidth="1.2"
          />
          {/* Rx clinical text lines */}
          <line
            x1="3"
            y1="4.5"
            x2="9.5"
            y2="4.5"
            stroke="white"
            strokeWidth="1.3"
            strokeLinecap="round"
          />
          <line
            x1="3"
            y1="7.5"
            x2="8.5"
            y2="7.5"
            stroke="white"
            strokeWidth="1.3"
            strokeLinecap="round"
          />
          <line
            x1="3"
            y1="10.5"
            x2="6"
            y2="10.5"
            stroke="white"
            strokeWidth="1.3"
            strokeLinecap="round"
          />
          {/* Small medical cross badge */}
          <circle cx="10" cy="11.5" r="2.2" fill="#EC4899" />
          <path
            d="M10 10.4V12.6M8.9 11.5H11.1"
            stroke="white"
            strokeWidth="0.8"
            strokeLinecap="round"
          />
        </g>
      </svg>
    </span>
  )
}

function BrandLogo({ size = 'md', isDark = false, className = '' }) {
  const isLg = size === 'lg'
  const isSm = size === 'sm'

  return (
    <Link
      to="/"
      className={`group flex shrink-0 items-center gap-2.5 ${className}`}
      aria-label="MedScan AI home"
    >
      <MultiModalIcon size={size} />
      <span
        className={`font-extrabold tracking-tight ${
          isLg ? 'text-2xl' : isSm ? 'text-base' : 'text-lg'
        } ${isDark ? 'text-white' : 'text-slate-900'}`}
      >
        Med<span className={isDark ? 'text-emerald-400' : 'text-emerald-700'}>Scan</span>
        <span
          className={`ml-1.5 rounded-md px-1.5 py-0.5 text-[0.65rem] font-bold tracking-wider ${
            isDark ? 'bg-white/10 text-emerald-400' : 'bg-slate-900 text-white'
          }`}
        >
          AI
        </span>
      </span>
    </Link>
  )
}

export default BrandLogo
