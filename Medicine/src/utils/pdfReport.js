import { jsPDF } from 'jspdf'

export const APP_NAME = 'MedScan AI'
export const LEAF_FILE_NAME = 'Leaf_Detection_Report.pdf'
export const TABLET_FILE_NAME = 'Tablet_Detection_Report.pdf'
export const PRESCRIPTION_FILE_NAME = 'Prescription_Report.pdf'
export const HANDWRITTEN_PRESCRIPTION_FILE_NAME =
  'Handwritten_Prescription_Report.pdf'

import {
  getMedicineUsage,
  getMedicineSideEffects,
} from './medicineLookup.js'

const PAGE_WIDTH = 210
const PRIMARY = [15, 118, 110]
const PAGE_HEIGHT = 297
const MARGIN = 14
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2
const BOTTOM_LIMIT = PAGE_HEIGHT - 18
const FONT = 'helvetica'

const DEFAULT_DISCLAIMER =
  'This application provides AI-assisted identification for educational and informational purposes. It is not a substitute for professional medical advice.'

const REMEDIES_DISCLAIMER =
  'These traditional preparations are provided for informational purposes only and are not a substitute for professional medical advice, diagnosis, or treatment.'

function createCtx(doc) {
  return { doc, y: MARGIN }
}

function ensureSpace(ctx, height) {
  if (ctx.y + height > BOTTOM_LIMIT) {
    ctx.doc.addPage()
    ctx.y = MARGIN
  }
}

function formatDate(value) {
  const date = value ? new Date(value) : new Date()
  if (Number.isNaN(date.getTime())) return new Date().toLocaleString()
  return date.toLocaleString(undefined, {
    dateStyle: 'long',
    timeStyle: 'short',
  })
}

function formatConfidence(value) {
  const num = Number(value)
  return Number.isFinite(num) && value != null && value !== ''
    ? `${num.toFixed(1)}%`
    : null
}

function toList(items) {
  if (!Array.isArray(items)) return []
  return items.filter((item) => item != null && String(item).trim() !== '')
}

function header(ctx, eyebrow, title) {
  const { doc } = ctx
  doc.setFillColor(15, 23, 42)
  doc.roundedRect(MARGIN, MARGIN, CONTENT_WIDTH, 24, 2, 2, 'F')

  doc.setTextColor(52, 211, 153)
  doc.setFont(FONT, 'bold')
  doc.setFontSize(13)
  doc.text(APP_NAME, MARGIN + 4, MARGIN + 8)

  doc.setTextColor(226, 232, 240)
  doc.setFont(FONT, 'normal')
  doc.setFontSize(8)
  doc.text('AI-Assisted Medicinal Identification', MARGIN + 4, MARGIN + 13.5)

  doc.setTextColor(255, 255, 255)
  doc.setFont(FONT, 'bold')
  doc.setFontSize(15)
  doc.text(title, PAGE_WIDTH - MARGIN - 4, MARGIN + 11, { align: 'right' })

  doc.setFont(FONT, 'normal')
  doc.setFontSize(8)
  doc.setTextColor(148, 163, 184)
  doc.text(eyebrow, PAGE_WIDTH - MARGIN - 4, MARGIN + 16.5, { align: 'right' })

  ctx.y = MARGIN + 24 + 8
}

function section(ctx, label) {
  const { doc } = ctx
  ensureSpace(ctx, 12)
  ctx.y += 4

  doc.setFillColor(16, 185, 129)
  doc.rect(MARGIN, ctx.y - 2.5, 1.6, 4, 'F')
  doc.setTextColor(15, 23, 42)
  doc.setFont(FONT, 'bold')
  doc.setFontSize(10.5)
  doc.text(label.toUpperCase(), MARGIN + 4, ctx.y + 0.6)

  doc.setDrawColor(226, 232, 240)
  doc.setLineWidth(0.2)
  doc.line(MARGIN, ctx.y + 3, PAGE_WIDTH - MARGIN, ctx.y + 3)

  ctx.y += 7
}

function metaGrid(ctx, items) {
  const { doc } = ctx
  const rows = items.filter((item) => item != null)
  if (!rows.length) return

  ctx.y += 2
  const labelWidth = 52

  rows.forEach(([label, value]) => {
    doc.setFont(FONT, 'bold')
    doc.setFontSize(8.5)
    doc.setTextColor(100, 116, 139)
    const labelLines = doc.splitTextToSize(label, labelWidth - 6)
    doc.setFont(FONT, 'normal')
    doc.setFontSize(9)
    doc.setTextColor(51, 65, 85)
    const valueLines = doc.splitTextToSize(String(value), CONTENT_WIDTH - labelWidth - 8)
    const boxHeight = Math.max(labelLines.length, valueLines.length) * 4 + 5

    ensureSpace(ctx, boxHeight + 2)

    doc.setFillColor(241, 245, 249)
    doc.roundedRect(MARGIN, ctx.y, CONTENT_WIDTH, boxHeight, 1.5, 1.5, 'F')

    doc.setFont(FONT, 'bold')
    doc.setFontSize(8.5)
    doc.setTextColor(100, 116, 139)
    doc.text(labelLines, MARGIN + 3.5, ctx.y + 5)

    doc.setFont(FONT, 'normal')
    doc.setFontSize(9)
    doc.setTextColor(15, 23, 42)
    doc.text(valueLines, MARGIN + labelWidth + 4, ctx.y + 5)

    ctx.y += boxHeight + 2
  })
}

function labelValue(ctx, label, value) {
  const { doc } = ctx
  if (value == null || String(value).trim() === '') return

  ensureSpace(ctx, 8)
  doc.setFont(FONT, 'bold')
  doc.setFontSize(8.5)
  doc.setTextColor(100, 116, 139)
  doc.text(label, MARGIN, ctx.y)

  doc.setFont(FONT, 'normal')
  doc.setFontSize(9.5)
  doc.setTextColor(51, 65, 85)
  const lines = doc.splitTextToSize(String(value), CONTENT_WIDTH - 48)
  doc.text(lines, MARGIN + 48, ctx.y)

  ctx.y += lines.length * 3.9 + 2.5
}

function bullets(ctx, items) {
  const { doc } = ctx
  toList(items).forEach((item) => {
    const lines = doc.splitTextToSize(String(item), CONTENT_WIDTH - 10)
    ensureSpace(ctx, lines.length * 3.9 + 1)

    doc.setFont(FONT, 'bold')
    doc.setFontSize(9.5)
    doc.setTextColor(5, 150, 105)
    doc.text('•', MARGIN + 2, ctx.y)

    doc.setFont(FONT, 'normal')
    doc.setTextColor(51, 65, 85)
    doc.text(lines, MARGIN + 6, ctx.y)

    ctx.y += lines.length * 3.9 + 1.6
  })
}

function paragraph(ctx, label, value) {
  const { doc } = ctx
  if (!value || String(value).trim() === '') return

  section(ctx, label)
  const lines = doc.splitTextToSize(String(value), CONTENT_WIDTH)
  ensureSpace(ctx, lines.length * 4.4 + 2)

  doc.setFont(FONT, 'normal')
  doc.setFontSize(9.5)
  doc.setTextColor(51, 65, 85)
  doc.text(lines, MARGIN, ctx.y, { lineHeightFactor: 1.5 })

  ctx.y += lines.length * 4.4 + 3
}

function detectImageFormat(src) {
  if (/^data:image\/jpeg/i.test(src)) return 'JPEG'
  if (/^data:image\/webp/i.test(src)) return 'WEBP'
  return 'PNG'
}

function placeholderBox(ctx, alt) {
  const { doc } = ctx
  ensureSpace(ctx, 28)

  doc.setDrawColor(203, 213, 225)
  doc.setFillColor(241, 245, 249)
  doc.roundedRect(MARGIN, ctx.y, CONTENT_WIDTH, 26, 2, 2, 'DF')
  doc.setTextColor(100, 116, 139)
  doc.setFont(FONT, 'normal')
  doc.setFontSize(9)
  doc.text(`${alt} — not available for export`, PAGE_WIDTH / 2, ctx.y + 13, {
    align: 'center',
  })

  ctx.y += 30
}

function image(ctx, source, alt = 'Uploaded image') {
  const { doc } = ctx
  if (!source) {
    placeholderBox(ctx, alt)
    return
  }

  let props = null
  try {
    props = doc.getImageProperties(source)
  } catch {
    props = null
  }

  const maxWidth = 78
  const maxHeight = 58
  let width = maxWidth
  let height = 40

  if (props) {
    const ratio = props.height / props.width
    width = maxWidth
    height = width * ratio
    if (height > maxHeight) {
      height = maxHeight
      width = height / ratio
    }
  }

  ensureSpace(ctx, height + 4)
  try {
    const x = MARGIN + (CONTENT_WIDTH - width) / 2
    doc.addImage(source, detectImageFormat(source), x, ctx.y, width, height)
    ctx.y += height + 4
  } catch {
    placeholderBox(ctx, alt)
  }
}

function disclaimer(ctx, extraText = null) {
  const { doc } = ctx
  const text = extraText
    ? `${DEFAULT_DISCLAIMER} ${String(extraText).trim()}`
    : DEFAULT_DISCLAIMER
  const lines = doc.splitTextToSize(text, CONTENT_WIDTH - 8)
  const height = lines.length * 3.8 + 13

  ensureSpace(ctx, height + 4)

  doc.setDrawColor(252, 211, 77)
  doc.setFillColor(255, 251, 235)
  doc.roundedRect(MARGIN, ctx.y, CONTENT_WIDTH, height, 2, 2, 'DF')

  doc.setTextColor(146, 64, 14)
  doc.setFont(FONT, 'bold')
  doc.setFontSize(8.5)
  doc.text('MEDICAL DISCLAIMER', MARGIN + 4, ctx.y + 6)

  doc.setFont(FONT, 'normal')
  doc.setFontSize(8)
  doc.text(lines, MARGIN + 4, ctx.y + 11)

  ctx.y += height + 6
}

function finalize(doc) {
  const pageCount = doc.getNumberOfPages()
  const stamp = `Generated by ${APP_NAME} · ${new Date().toLocaleString()}`
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i)
    doc.setFont(FONT, 'normal')
    doc.setFontSize(7.5)
    doc.setTextColor(148, 163, 184)
    doc.text(stamp, PAGE_WIDTH / 2, PAGE_HEIGHT - 6, { align: 'center' })
    doc.text(`Page ${i} of ${pageCount}`, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 6, {
      align: 'right',
    })
    doc.text('Educational use only', MARGIN, PAGE_HEIGHT - 6)
  }
  return doc
}

function remediesSection(ctx, remedies) {
  const list = Array.isArray(remedies) ? remedies : []
  if (!list.length) return

  section(ctx, 'Traditional Remedies')

  list.forEach((remedy, index) => {
    if (!remedy || typeof remedy !== 'object') return
    const title = remedy.name ?? `Remedy ${index + 1}`
    const ingredients = Array.isArray(remedy.ingredients)
      ? remedy.ingredients.join(', ')
      : remedy.ingredients
    medicineCard(ctx, `${index + 1}. ${title}`, [
      ['Ingredients', ingredients],
      ['Preparation', remedy.preparation],
      ['Traditional Use', remedy.traditionalUse],
      ['Precautions', remedy.precautions],
    ])
  })

  ensureSpace(ctx, 26)
  ctx.y += 2

  const { doc } = ctx
  const lines = doc.splitTextToSize(REMEDIES_DISCLAIMER, CONTENT_WIDTH - 8)
  const height = lines.length * 3.8 + 11

  ensureSpace(ctx, height + 4)
  doc.setDrawColor(252, 211, 77)
  doc.setFillColor(255, 251, 235)
  doc.roundedRect(MARGIN, ctx.y, CONTENT_WIDTH, height, 2, 2, 'DF')

  doc.setTextColor(146, 64, 14)
  doc.setFont(FONT, 'bold')
  doc.setFontSize(8)
  doc.text('TRADITIONAL REMEDIES', MARGIN + 4, ctx.y + 6)

  doc.setFont(FONT, 'normal')
  doc.setFontSize(8)
  doc.text(lines, MARGIN + 4, ctx.y + 11)

  ctx.y += height + 6
}

export function buildLeafReport({ plant = {}, result = {}, imageUrl, disclaimerText = null }) {
  const doc = new jsPDF({ unit: 'mm', format: 'a4' })
  const ctx = createCtx(doc)

  header(ctx, 'Medicinal Leaf Identification', 'Leaf Detection Report')

  metaGrid(ctx, [
    ['Detection Date/Time', formatDate(result.analyzedAt)],
    ['Confidence', formatConfidence(result.confidence)],
    ['Status', result.status],
    ['Model', result.model],
    ['Request ID', result.id],
  ])

  section(ctx, 'Uploaded Image')
  image(ctx, imageUrl, 'Uploaded leaf image')

  section(ctx, 'Identified Plant')
  labelValue(ctx, 'Plant Name', plant.name)
  labelValue(ctx, 'Scientific Name', plant.scientificName)
  labelValue(ctx, 'Family', plant.family)

  if (toList(plant.uses).length) {
    section(ctx, 'Medicinal Uses & Benefits')
    bullets(ctx, plant.uses)
  }

  paragraph(ctx, 'Description', plant.description)

  const plantFacts = [
    ['Native Region', plant.nativeRegion],
    ['Parts Used', plant.partsUsed],
  ].filter(([, value]) => value != null && String(value).trim() !== '')
  if (plantFacts.length) {
    section(ctx, 'Plant Information')
    plantFacts.forEach(([label, value]) => labelValue(ctx, label, value))
  }

  if (toList(plant.activeCompounds).length) {
    section(ctx, 'Active Compounds')
    bullets(ctx, plant.activeCompounds)
  }

  if (toList(plant.precautions).length) {
    section(ctx, 'Precautions')
    bullets(ctx, plant.precautions)
  }

  if (toList(plant.sideEffects).length) {
    section(ctx, 'Side Effects')
    bullets(ctx, plant.sideEffects)
  }

  paragraph(ctx, 'Storage', plant.storage)

  remediesSection(ctx, plant.remedies)

  disclaimer(ctx, disclaimerText)
  return finalize(doc)
}

export function buildTabletReport({ medicine = {}, result = {}, imageUrl, disclaimerText = null }) {
  const doc = new jsPDF({ unit: 'mm', format: 'a4' })
  const ctx = createCtx(doc)

  header(ctx, 'Pharmaceutical Tablet Identification', 'Tablet Detection Report')

  metaGrid(ctx, [
    ['Detection Date/Time', formatDate(result.analyzedAt)],
    ['Confidence', formatConfidence(result.confidence)],
    ['Status', result.status],
    ['Model', result.model],
    ['Request ID', result.id],
  ])

  section(ctx, 'Uploaded Tablet Image')
  image(ctx, imageUrl, 'Uploaded tablet image')

  section(ctx, 'Identified Medicine')
  labelValue(ctx, 'Medicine Name', medicine.name)
  labelValue(ctx, 'Generic Name', medicine.genericName)

  const medicineFacts = [
    ['Composition', medicine.composition],
    ['Manufacturer', medicine.manufacturer],
    ['Category', medicine.category],
    ['Strength', medicine.dosage],
  ].filter(([, value]) => value != null && String(value).trim() !== '')
  if (medicineFacts.length) {
    section(ctx, 'Medicine Information')
    medicineFacts.forEach(([label, value]) => labelValue(ctx, label, value))
  }

  if (toList(medicine.uses).length) {
    section(ctx, 'Uses')
    bullets(ctx, medicine.uses)
  }

  if (toList(medicine.precautions).length) {
    section(ctx, 'Precautions')
    bullets(ctx, medicine.precautions)
  }

  if (toList(medicine.sideEffects).length) {
    section(ctx, 'Side Effects')
    bullets(ctx, medicine.sideEffects)
  }

  paragraph(ctx, 'Storage', medicine.storage)
  paragraph(ctx, 'Description', medicine.description)

  disclaimer(ctx, disclaimerText)
  return finalize(doc)
}

function medicineCard(ctx, title, rows) {
  const { doc } = ctx
  const blocks = rows
    .map(([label, value]) => {
      if (value == null || String(value).trim() === '') return null
      const lineCount = doc.splitTextToSize(String(value), CONTENT_WIDTH - 58).length
      return { label, value, lineCount }
    })
    .filter(Boolean)
  const bodyHeight = blocks.reduce((acc, block) => acc + block.lineCount * 3.9 + 2, 0) + 12

  ensureSpace(ctx, bodyHeight + 2)
  doc.setFillColor(241, 245, 249)
  doc.setDrawColor(203, 213, 225)
  doc.roundedRect(MARGIN, ctx.y + 1, CONTENT_WIDTH, bodyHeight, 1.5, 1.5, 'DF')

  doc.setTextColor(15, 23, 42)
  doc.setFont(FONT, 'bold')
  doc.setFontSize(10)
  doc.text(title, MARGIN + 4, ctx.y + 7)

  let innerY = ctx.y + 13
  blocks.forEach((block) => {
    doc.setFont(FONT, 'bold')
    doc.setFontSize(8.5)
    doc.setTextColor(100, 116, 139)
    doc.text(block.label, MARGIN + 5, innerY)

    doc.setFont(FONT, 'normal')
    doc.setFontSize(9.5)
    doc.setTextColor(51, 65, 85)
    const lines = doc.splitTextToSize(String(block.value), CONTENT_WIDTH - 58)
    doc.text(lines, MARGIN + 30, innerY)

    innerY += lines.length * 3.9 + 2
  })

  ctx.y += bodyHeight + 4
}

function extractedTextBlock(ctx, text, label = 'Extracted OCR Text') {
  const { doc } = ctx
  if (!text || String(text).trim() === '') return

  section(ctx, label)
  const lines = doc.splitTextToSize(String(text), CONTENT_WIDTH - 8)
  const height = lines.length * 3.4 + 9

  ensureSpace(ctx, height + 2)
  doc.setFillColor(248, 250, 252)
  doc.setDrawColor(226, 232, 240)
  doc.roundedRect(MARGIN, ctx.y, CONTENT_WIDTH, height, 1.5, 1.5, 'DF')

  doc.setTextColor(51, 65, 85)
  doc.setFont('courier', 'normal')
  doc.setFontSize(8)
  doc.text(lines, MARGIN + 4, ctx.y + 6)

  ctx.y += height + 4
}

export function buildPrescriptionReport({ prescription = {}, imageUrl, disclaimerText = null }) {
  const doc = new jsPDF({ unit: 'mm', format: 'a4' })
  const ctx = createCtx(doc)

  header(ctx, 'Prescription OCR Extraction', 'Prescription Report')

  const patient = prescription.patientAge
    ? `${prescription.patientName} (${prescription.patientAge})`
    : prescription.patientName

  metaGrid(ctx, [
    ['Scan Date/Time', formatDate(prescription.issuedDate)],
    ['Prescription No.', prescription.prescriptionNumber],
    ['Patient', patient],
    ['Doctor', prescription.doctorName],
    ['Organization', prescription.organization],
    ['Status', prescription.status],
  ])

  section(ctx, 'Prescription Image')
  image(ctx, imageUrl, 'Uploaded prescription image')

  const medicines = Array.isArray(prescription.medicines) ? prescription.medicines : []
  if (medicines.length) {
    section(ctx, 'Medicine List')
    medicines.forEach((medicine, index) => {
      const name = medicine.medicineName ?? `Medicine ${index + 1}`
      medicineCard(ctx, `${index + 1}. ${name}`, [
        ['Tablet Name', medicine.medicineName ?? name],
        ['Dosage', medicine.dosage || 'As prescribed'],
        ['Usage', getMedicineUsage(medicine)],
        ['Duration', medicine.duration || 'Course duration'],
        ['Side Effects', getMedicineSideEffects(medicine)],
      ])
    })
  }

  disclaimer(ctx, prescription.disclaimer ?? disclaimerText)
  return finalize(doc)
}

export function buildHandwrittenPrescriptionReport({
  prescription = {},
  imageUrl,
  disclaimerText = null,
}) {
  const doc = new jsPDF({ unit: 'mm', format: 'a4' })
  const ctx = createCtx(doc)

  header(ctx, 'Handwritten Prescription', 'Handwritten Prescription Report')

  metaGrid(ctx, [
    ['Date', prescription.issuedDate ?? prescription.date],
    ['Prescription No.', prescription.prescriptionNumber],
    ['Patient Name', prescription.patientName],
    ['Doctor Name', prescription.doctorName],
    ['Organization', prescription.organization],
    ['Status', prescription.status],
  ])

  section(ctx, 'Prescription Image')
  image(ctx, imageUrl, 'Uploaded handwritten prescription image')

  const medicines = Array.isArray(prescription.medicines)
    ? prescription.medicines
    : []
  if (medicines.length) {
    section(ctx, 'Medicine List')
    medicines.forEach((medicine, index) => {
      const name = medicine.medicineName ?? `Medicine ${index + 1}`
      medicineCard(ctx, `${index + 1}. ${name}`, [
        ['Tablet Name', medicine.medicineName ?? name],
        ['Dosage', medicine.dosage || 'As prescribed'],
        ['Usage', getMedicineUsage(medicine)],
        ['Duration', medicine.duration || 'Course duration'],
        ['Side Effects', getMedicineSideEffects(medicine)],
      ])
    })
  }

  disclaimer(ctx, prescription.disclaimer ?? disclaimerText)
  return finalize(doc)
}

export default {
  buildLeafReport,
  buildTabletReport,
  buildPrescriptionReport,
  buildHandwrittenPrescriptionReport,
  LEAF_FILE_NAME,
  TABLET_FILE_NAME,
  PRESCRIPTION_FILE_NAME,
  HANDWRITTEN_PRESCRIPTION_FILE_NAME,
  APP_NAME,
}