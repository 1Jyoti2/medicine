import axios from 'axios'

import {
  detectionHistory,
  getLeafResultById,
  getPrescriptionById,
  getTabletResultById,
  medicinalPlants,
  pharmaceuticalMedicines,
} from '../data/mockData.js'

export { getLeafResultById, getPrescriptionById, getTabletResultById }

// Real API Mode connected to FastAPI backend
const MOCK_MODE = false

const api = axios.create({
  baseURL: import.meta.env?.VITE_API_BASE_URL || '',
  timeout: 60000,
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error)
  },
)

function createRequestId() {
  return `req_${Date.now()}`
}

function rejectEnvelope(message, requestId) {
  return { success: false, requestId, message }
}

function findNamed(collection, name, keys) {
  const query = String(name ?? '').trim().toLowerCase()
  if (!query) return null

  return collection.find((item) =>
    keys.some(
      (key) =>
        String(item[key] ?? '').toLowerCase() === query ||
        String(item[key] ?? '').toLowerCase().includes(query),
    ),
  )
}

let historyStore = [...detectionHistory]
const handwrittenResultStore = []

export function getHandwrittenPrescriptionById(id) {
  return handwrittenResultStore.find((item) => item.id === id) ?? null
}

/**
 * Real Leaf Classification API Call.
 * Sends uploaded leaf image to POST /predict/leaf via multipart/form-data.
 */
export async function predictLeaf(image) {
  const requestId = createRequestId()
  if (!image) {
    return rejectEnvelope('No image provided for leaf prediction.', requestId)
  }

  try {
    const formData = new FormData()
    formData.append('file', image)
    formData.append('image', image)

    const { data } = await api.post('/predict/leaf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return data
  } catch (error) {
    const message =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      'Failed to connect to leaf classification service.'
    return rejectEnvelope(message, requestId)
  }
}

/**
 * Real Pill / Tablet Identification API Call.
 * Sends uploaded pill image to POST /predict/pill via multipart/form-data.
 */
export async function predictTablet(image) {
  const requestId = createRequestId()
  if (!image) {
    return rejectEnvelope('No image provided for tablet prediction.', requestId)
  }

  try {
    const formData = new FormData()
    formData.append('file', image)
    formData.append('image', image)

    const { data } = await api.post('/predict/pill', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return data
  } catch (error) {
    const message =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      'Failed to connect to pill identification service.'
    return rejectEnvelope(message, requestId)
  }
}

/**
 * Real Prescription OCR API Call.
 * Sends uploaded prescription image to POST /predict/prescription via multipart/form-data.
 */
export async function scanPrescription(image) {
  const requestId = createRequestId()
  if (!image) {
    return rejectEnvelope('No image provided for prescription scan.', requestId)
  }

  try {
    const formData = new FormData()
    formData.append('file', image)
    formData.append('image', image)

    const { data } = await api.post('/predict/prescription', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return data
  } catch (error) {
    const message =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      'Failed to connect to prescription OCR service.'
    return rejectEnvelope(message, requestId)
  }
}

export async function scanHandwrittenPrescription(image, imageUrl = null) {
  return scanPrescription(image)
}

/**
 * Get Plant Details from API or Local Knowledge Base.
 */
export async function getPlantDetails(name) {
  const requestId = createRequestId()
  try {
    const { data } = await api.get('/plants/details', { params: { name } })
    return data
  } catch {
    const plant = findNamed(medicinalPlants, name, ['name', 'scientificName'])
    if (!plant) {
      return rejectEnvelope(`No plant details found for "${name}".`, requestId)
    }
    return {
      success: true,
      requestId,
      message: 'Plant details retrieved.',
      data: plant,
    }
  }
}

/**
 * Get Medicine Details from API or Local Knowledge Base.
 */
export async function getMedicineDetails(name) {
  const requestId = createRequestId()
  try {
    const { data } = await api.get('/medicines/details', { params: { name } })
    return data
  } catch {
    const medicine = findNamed(pharmaceuticalMedicines, name, [
      'name',
      'genericName',
    ])
    if (!medicine) {
      return rejectEnvelope(
        `No medicine details found for "${name}".`,
        requestId,
      )
    }
    return {
      success: true,
      requestId,
      message: 'Medicine details retrieved.',
      data: medicine,
    }
  }
}

/**
 * Get Detection History.
 */
export async function getHistory() {
  const requestId = createRequestId()
  try {
    const { data } = await api.get('/history')
    if (data && data.success && Array.isArray(data.data) && data.data.length > 0) {
      return data
    }
  } catch {
    // Fallback to local store
  }
  return {
    success: true,
    requestId,
    message: 'Detection history retrieved.',
    data: historyStore,
  }
}

export default api