import { useEffect, useRef, useState } from 'react'
import { Camera, CameraOff, Video } from 'lucide-react'

import useLanguage from '../context/useLanguage.js'
import Button from './Button.jsx'
import ErrorMessage from './ErrorMessage.jsx'

function getUiErrorMessage(err, t) {
  switch (err?.name) {
    case 'NotAllowedError':
      return t('camera.notAllowed')
    case 'NotFoundError':
    case 'OverconstrainedError':
      return t('camera.notFound')
    case 'NotReadableError':
      return t('camera.notReadable')
    case 'SecurityError':
      return t('camera.security')
    case 'AbortError':
      return t('camera.aborted')
    default:
      return t('camera.generic')
  }
}

function CameraCapture({ onCapture, disabled = false, className = '' }) {
  const { t } = useLanguage()
  const videoRef = useRef(null)
  const streamRef = useRef(null)
  const mountedRef = useRef(true)
  const pendingRef = useRef(false)
  const [isReady, setIsReady] = useState(false)
  const [isStarting, setIsStarting] = useState(false)
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)
  const [isSupported] = useState(
    () =>
      typeof navigator !== 'undefined' &&
      Boolean(navigator.mediaDevices?.getUserMedia),
  )
  const [isSecureContext] = useState(
    () =>
      typeof window !== 'undefined' &&
      (typeof window.isSecureContext === 'undefined'
        ? window.location.protocol === 'https:' ||
          window.location.hostname === 'localhost' ||
          window.location.hostname === '127.0.0.1'
        : window.isSecureContext),
  )

  function setStarting(value) {
    if (mountedRef.current) setIsStarting(value)
  }

  function stopStream() {
    const stream = streamRef.current
    if (stream) {
      stream.getTracks().forEach((track) => track.stop())
    }
    streamRef.current = null
    if (videoRef.current) {
      videoRef.current.srcObject = null
      videoRef.current.onloadedmetadata = null
      videoRef.current.oncanplay = null
    }
  }

  /**
   * Waits for the video to actually have a frame before resolving.
   * Avoids checking readyState prematurely.
   */
  function waitForVideoReady(video) {
    return new Promise((resolve, reject) => {
      if (video.readyState >= 2 && video.videoWidth > 0) {
        resolve()
        return
      }
      const onReady = () => {
        cleanup()
        resolve()
      }
      const onError = () => {
        cleanup()
        reject(new Error(t('camera.streamError')))
      }
      const cleanup = () => {
        video.removeEventListener('loadeddata', onReady)
        video.removeEventListener('loadedmetadata', onReady)
        video.removeEventListener('canplay', onReady)
        video.removeEventListener('error', onError)
      }
      video.addEventListener('loadeddata', onReady)
      video.addEventListener('loadedmetadata', onReady)
      video.addEventListener('canplay', onReady)
      video.addEventListener('error', onError)
    })
  }

  async function handleCapture() {
    if (pendingRef.current) return
    setError(null)
    setStatus(null)

    if (!isSupported) {
      setError(
        window.isSecureContext === false
          ? t('camera.insecure')
          : t('camera.unsupported'),
      )
      return
    }
    if (!isSecureContext) {
      setError(t('camera.insecure'))
      return
    }

    setStarting(true)
    pendingRef.current = true
    setStatus(t('camera.requesting'))

    const video = videoRef.current
    if (!video) {
      pendingRef.current = false
      setStarting(false)
      setError(t('camera.previewNotReady'))
      return
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment',
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
      })

      if (!mountedRef.current) {
        stream.getTracks().forEach((track) => track.stop())
        pendingRef.current = false
        setStarting(false)
        return
      }

      streamRef.current = stream
      setStatus(t('camera.opening'))

      // Attach the stream to the already-mounted <video> element.
      video.srcObject = stream

      // Wait for the video to report it actually has frames.
      await waitForVideoReady(video)

      // Play may be needed on some browsers even with autoPlay.
      try {
        await video.play()
      } catch {
        // Ignore; autoPlay already handles playback in most browsers.
      }

      if (!mountedRef.current) {
        stopStream()
        pendingRef.current = false
        setStarting(false)
        setIsReady(false)
        return
      }

      pendingRef.current = false
      setStarting(false)
      setIsReady(true)
      setError(null)
      setStatus(t('camera.ready'))
    } catch (err) {
      pendingRef.current = false
      setStarting(false)
      stopStream()
      setIsReady(false)
      setError(getUiErrorMessage(err, t))
    }
  }

  function handleStop() {
    stopStream()
    setIsReady(false)
    setStatus(null)
  }

  function handleCaptureFrame() {
    const video = videoRef.current
    if (!video || video.videoWidth === 0 || !isReady) {
      setError(t('camera.notReady'))
      return
    }

    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    canvas
      .getContext('2d')
      .drawImage(video, 0, 0, canvas.width, canvas.height)

    canvas.toBlob(
      (blob) => {
        if (blob) {
          onCapture?.(
            new File([blob], `capture-${Date.now()}.jpg`, {
              type: 'image/jpeg',
            }),
          )
          setStatus(t('camera.captured'))
          handleStop()
        } else {
          setError(t('camera.captureFailed'))
        }
      },
      'image/jpeg',
      0.9,
    )
  }

  useEffect(() => {
    mountedRef.current = true
    return () => {
      mountedRef.current = false
      pendingRef.current = false
      stopStream()
    }
  }, [])

  if (!isSupported) {
    return <ErrorMessage message={t('camera.unsupported')} />
  }

  return (
    <div className={className}>
      <div className="relative overflow-hidden rounded-2xl border border-slate-200 bg-slate-900">
        {/* The <video> is ALWAYS rendered so videoRef.current exists when the
            stream is attached. It only becomes visible once the feed is ready. */}
        <video
          ref={videoRef}
          className={`aspect-video w-full object-cover transition-opacity duration-300 ${
            isReady ? 'opacity-100' : 'opacity-0'
          }`}
          autoPlay
          playsInline
          muted
        />
        {!isReady && (
          <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center gap-3 text-slate-400">
            <Video aria-hidden className="size-10" />
            <span className="text-sm font-medium">
              {isStarting ? t('camera.starting') : t('detect.cameraPreview')}
            </span>
          </div>
        )}
      </div>

      {status && !error && (
        <p className="mt-3 text-sm text-emerald-700">{status}</p>
      )}

      {error && <ErrorMessage className="mt-3" message={error} />}

      <div className="mt-4 flex flex-wrap gap-3">
        {isReady ? (
          <>
            <Button
              onClick={handleCaptureFrame}
              icon={Camera}
              disabled={disabled}
            >
              {t('camera.capture')}
            </Button>
            <Button variant="outline" onClick={handleStop} icon={CameraOff}>
              {t('camera.stop')}
            </Button>
          </>
        ) : (
          <Button
            onClick={handleCapture}
            icon={Camera}
            disabled={disabled || isStarting}
            loading={isStarting}
          >
            {isStarting ? t('camera.starting') : t('camera.capture')}
          </Button>
        )}
      </div>
    </div>
  )
}

export default CameraCapture