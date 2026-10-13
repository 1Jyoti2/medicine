import { useRef, useState } from 'react'
import { ImagePlus, RefreshCw, Upload, X } from 'lucide-react'

function ImageUploader({
  onFile,
  accept = 'image/*',
  label = 'Upload an image',
  hint,
  preview,
  onClearPreview,
  changeLabel,
  disabled = false,
  className = '',
}) {
  const inputRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)

  function handleFiles(fileList) {
    const file = fileList?.[0]
    if (file && onFile) onFile(file)
  }

  return (
    <div className={className}>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        disabled={disabled}
        aria-label={label}
        className="sr-only"
        onChange={(event) => handleFiles(event.target.files)}
      />

      {preview ? (
        <div className="relative overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <img
            src={preview}
            alt="Uploaded image preview"
            className="max-h-96 w-full object-cover"
          />
          <div className="absolute inset-x-0 bottom-0 flex items-center justify-between gap-3 bg-gradient-to-t from-slate-900/70 to-transparent p-4">
            <p className="text-sm font-medium text-white">
              Image ready for analysis
            </p>
            <div className="flex items-center gap-2">
              {changeLabel && (
                <button
                  type="button"
                  aria-label={changeLabel}
                  onClick={() => inputRef.current?.click()}
                  disabled={disabled}
                  className="inline-flex items-center gap-1.5 rounded-xl border border-white/30 px-3 py-2 text-xs font-semibold text-white transition-colors duration-200 hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  <RefreshCw className="size-3.5" />
                  {changeLabel}
                </button>
              )}
              {onClearPreview && (
                <button
                  type="button"
                  aria-label="Remove image"
                  onClick={onClearPreview}
                  disabled={disabled}
                  className="inline-flex items-center gap-1.5 rounded-xl border border-white/30 px-3 py-2 text-xs font-semibold text-white transition-colors duration-200 hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  <X className="size-3.5" />
                  Remove
                </button>
              )}
            </div>
          </div>
        </div>
      ) : (
        <button
          type="button"
          disabled={disabled}
          onClick={() => inputRef.current?.click()}
          onDragOver={(event) => {
            event.preventDefault()
            setIsDragging(true)
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(event) => {
            event.preventDefault()
            setIsDragging(false)
            handleFiles(event.dataTransfer.files)
          }}
          className={`flex min-h-56 w-full flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed p-8 text-center transition-colors duration-200 disabled:cursor-not-allowed disabled:opacity-60 ${
            isDragging
              ? 'border-emerald-500 bg-emerald-50'
              : 'border-slate-300 bg-white hover:border-emerald-400 hover:bg-emerald-50/50'
          }`}
        >
          <span className="grid size-14 place-items-center rounded-2xl bg-emerald-100 text-emerald-700">
            {isDragging ? (
              <Upload aria-hidden className="size-7" />
            ) : (
              <ImagePlus aria-hidden className="size-7" />
            )}
          </span>
          <span className="text-sm font-semibold text-slate-800">{label}</span>
          {hint && <span className="text-xs text-slate-500">{hint}</span>}
          <span className="mt-1 rounded-full bg-slate-900 px-3 py-1 text-xs font-medium text-white">
            Browse files
          </span>
        </button>
      )}
    </div>
  )
}

export default ImageUploader