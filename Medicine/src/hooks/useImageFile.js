import { useEffect, useRef, useState } from 'react'

const SUPPORTED_FORMATS_MSG = 'Only JPG, JPEG and PNG image files are supported.'
const ACCEPT_TYPES = ['image/jpeg', 'image/png']
const EXT_PATTERNS = {
  'image/jpeg': 'jpe?g',
  'image/png': 'png',
  'image/webp': 'webp',
}

function isSupportedFile(file, acceptTypes) {
  if (!file?.type) {
    const pattern = acceptTypes
      .map((type) => EXT_PATTERNS[type])
      .filter(Boolean)
      .join('|')
    return new RegExp(`\\.(${pattern})$`, 'i').test(file?.name ?? '')
  }
  return acceptTypes.includes(file.type)
}

function fileToDataUrl(nextFile) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        resolve(reader.result)
      } else {
        reject(new Error('Unable to read image file.'))
      }
    }
    reader.onerror = () => {
      reject(reader.error ?? new Error('Unable to read image file.'))
    }
    reader.readAsDataURL(nextFile)
  })
}

function useImageFile({
  acceptTypes = ACCEPT_TYPES,
  formatsMessage = SUPPORTED_FORMATS_MSG,
} = {}) {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [error, setError] = useState(null)
  const previewUrlRef = useRef(null)

  useEffect(() => {
    return () => {
      if (previewUrlRef.current) {
        URL.revokeObjectURL(previewUrlRef.current)
      }
    }
  }, [])

  function handleFile(nextFile) {
    if (!isSupportedFile(nextFile, acceptTypes)) {
      setError(formatsMessage)
      return
    }
    setError(null)
    setFile(nextFile)
    if (previewUrlRef.current) {
      URL.revokeObjectURL(previewUrlRef.current)
    }
    const url = URL.createObjectURL(nextFile)
    previewUrlRef.current = url
    setPreviewUrl(url)
  }

  function handleRemove() {
    setFile(null)
    if (previewUrlRef.current) {
      URL.revokeObjectURL(previewUrlRef.current)
      previewUrlRef.current = null
    }
    setPreviewUrl(null)
  }

  function clearError() {
    setError(null)
  }

  function reportError(message) {
    setError(message)
  }

  return {
    file,
    previewUrl,
    error,
    handleFile,
    handleRemove,
    clearError,
    reportError,
    fileToDataUrl,
  }
}

export default useImageFile