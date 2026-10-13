/**
 * Medicine Knowledge Lookup Helper.
 * Provides standard Usage & Side Effects for detected and prescribed medications.
 */

export const MEDICINE_INFO_MAP = {
  levocetirizine: {
    usage: 'Allergy relief, Hay fever, Urticaria, Sneezing, Runny nose & Itching',
    sideEffects: 'Drowsiness, Dry mouth, Fatigue, Mild headache',
  },
  cetirizine: {
    usage: 'Allergy relief, Runny nose, Sneezing, Allergic rhinitis & Itching',
    sideEffects: 'Drowsiness, Dry mouth, Fatigue, Dizziness',
  },
  montelukast: {
    usage: 'Asthma maintenance, Prevention of bronchospasm, Allergic rhinitis',
    sideEffects: 'Headache, Abdominal pain, Dizziness, Fatigue',
  },
  calamine: {
    usage: 'Skin soothing, Insect bites, Sunburn, Itching & Eczema relief',
    sideEffects: 'Mild skin dryness or irritation (rare)',
  },
  paracetamol: {
    usage: 'Fever reduction, Mild to moderate pain relief, Headache',
    sideEffects: 'Nausea, Skin rash (rare)',
  },
  acetaminophen: {
    usage: 'Fever reduction, Pain relief, Body aches',
    sideEffects: 'Nausea, Skin rash (rare)',
  },
  ibuprofen: {
    usage: 'Anti-inflammatory pain relief, Fever reduction, Muscle aches',
    sideEffects: 'Stomach upset, Heartburn, Dizziness, Mild nausea',
  },
  amoxicillin: {
    usage: 'Bacterial infections, Respiratory, Ear/Nose/Throat & Skin infections',
    sideEffects: 'Diarrhea, Nausea, Skin rash, Vomiting',
  },
  augmentin: {
    usage: 'Resistant bacterial infections, Sinusitis, Respiratory tract infections',
    sideEffects: 'Diarrhea, Nausea, Skin rash, Stomach upset',
  },
  metformin: {
    usage: 'Type 2 diabetes blood sugar control, Insulin sensitivity support',
    sideEffects: 'Stomach upset, Metallic taste, Diarrhea, Nausea',
  },
  omeprazole: {
    usage: 'Acid reflux (GERD), Gastric & Duodenal ulcers, Heartburn relief',
    sideEffects: 'Headache, Abdominal pain, Nausea, Flatulence',
  },
  pantoprazole: {
    usage: 'Acidity, Acid reflux, GERD, Gastric ulcer management',
    sideEffects: 'Headache, Diarrhea, Stomach pain, Nausea',
  },
  rabeprazole: {
    usage: 'Gastric acid reduction, GERD, Peptic ulcer healing',
    sideEffects: 'Headache, Dizziness, Diarrhea, Mild nausea',
  },
  esomeprazole: {
    usage: 'Severe GERD, Erosive esophagitis, Acid suppression',
    sideEffects: 'Headache, Nausea, Flatulence, Abdominal pain',
  },
  ranitidine: {
    usage: 'Heartburn, Acid indigestion, Peptic ulcer management',
    sideEffects: 'Headache, Dizziness, Constipation',
  },
  domperidone: {
    usage: 'Nausea, Vomiting, Gastric motility improvement',
    sideEffects: 'Dry mouth, Headache, Mild cramps',
  },
  ondansetron: {
    usage: 'Prevention of nausea and vomiting',
    sideEffects: 'Constipation, Headache, Flushing, Fatigue',
  },
  amlodipine: {
    usage: 'High blood pressure (Hypertension), Angina / Chest pain management',
    sideEffects: 'Ankle swelling (edema), Flushing, Dizziness, Fatigue',
  },
  telmisartan: {
    usage: 'Hypertension management, Cardiovascular risk reduction',
    sideEffects: 'Dizziness, Sinus congestion, Back pain',
  },
  losartan: {
    usage: 'Hypertension, Diabetic nephropathy, Stroke risk reduction',
    sideEffects: 'Dizziness, Low blood pressure, Fatigue',
  },
  atorvastatin: {
    usage: 'Cholesterol & triglyceride reduction, Cardiovascular risk prevention',
    sideEffects: 'Mild muscle aches, Digestive changes, Fatigue',
  },
  rosuvastatin: {
    usage: 'High cholesterol reduction, Atherosclerosis prevention',
    sideEffects: 'Muscle aches, Headache, Abdominal pain',
  },
  glimepiride: {
    usage: 'Type 2 diabetes blood sugar management',
    sideEffects: 'Hypoglycemia (low blood sugar), Nausea, Dizziness',
  },
  azithromycin: {
    usage: 'Bacterial respiratory infections, Strep throat, Bronchitis',
    sideEffects: 'Diarrhea, Nausea, Abdominal pain, Headache',
  },
  ciprofloxacin: {
    usage: 'Urinary tract infections, Bacterial infections, Prostatitis',
    sideEffects: 'Nausea, Diarrhea, Headache, Tendon discomfort',
  },
  levofloxacin: {
    usage: 'Respiratory and urinary tract bacterial infections, Pneumonia',
    sideEffects: 'Nausea, Headache, Insomnia, Dizziness',
  },
  cefixime: {
    usage: 'Bacterial infections of ear, throat, urinary tract & lungs',
    sideEffects: 'Diarrhea, Loose stools, Abdominal pain, Nausea',
  },
  doxycycline: {
    usage: 'Bacterial infections, Acne vulgaris, Lyme disease, Malaria prophylaxis',
    sideEffects: 'Sun sensitivity, Nausea, Upset stomach',
  },
  metronidazole: {
    usage: 'Bacterial and protozoal infections, Dental infections',
    sideEffects: 'Metallic taste, Nausea, Dark urine, Headache',
  },
  fluconazole: {
    usage: 'Fungal infections, Candidiasis, Yeast infections',
    sideEffects: 'Headache, Nausea, Stomach pain, Rash',
  },
  clotrimazole: {
    usage: 'Topical fungal infections, Ringworm, Athlete\'s foot',
    sideEffects: 'Mild burning, Redness, Stinging at application site',
  },
  mupirocin: {
    usage: 'Bacterial skin infections, Impetigo, Folliculitis',
    sideEffects: 'Mild localized burning or stinging',
  },
  betamethasone: {
    usage: 'Severe skin inflammation, Eczema, Psoriasis relief',
    sideEffects: 'Skin thinning, Dryness, Burning with prolonged use',
  },
  salbutamol: {
    usage: 'Bronchospasm relief, Asthma, Chronic obstructive pulmonary disease',
    sideEffects: 'Tremor, Palpitations, Nervousness, Headache',
  },
  budesonide: {
    usage: 'Asthma maintenance, Airway inflammation control',
    sideEffects: 'Throat irritation, Hoarseness, Cough',
  },
  ambroxol: {
    usage: 'Productive wet cough, Mucus clearance, Bronchial congestion',
    sideEffects: 'Mild gastrointestinal discomfort, Nausea',
  },
  dextromethorphan: {
    usage: 'Dry non-productive cough suppression',
    sideEffects: 'Drowsiness, Dizziness, Nausea',
  },
  chlorpheniramine: {
    usage: 'Allergy relief, Cold symptoms, Sneezing, Itchy eyes',
    sideEffects: 'Drowsiness, Dry mouth, Blurred vision',
  },
  fexofenadine: {
    usage: 'Non-drowsy allergy relief, Hay fever, Urticaria',
    sideEffects: 'Headache, Drowsiness (rare), Nausea',
  },
  diclofenac: {
    usage: 'Joint pain, Arthritis, Post-injury inflammation & Pain relief',
    sideEffects: 'Stomach pain, Heartburn, Nausea, Dizziness',
  },
  aceclofenac: {
    usage: 'Musculoskeletal pain, Osteoarthritis, Rheumatoid arthritis',
    sideEffects: 'Indigestion, Abdominal pain, Dizziness',
  },
  tramadol: {
    usage: 'Moderate to severe pain relief',
    sideEffects: 'Dizziness, Nausea, Constipation, Drowsiness',
  },
  naproxen: {
    usage: 'Pain, Swelling, Joint stiffness, Menstrual cramps',
    sideEffects: 'Heartburn, Stomach pain, Dizziness',
  },
  mefenamic_acid: {
    usage: 'Menstrual cramps, Mild to moderate pain relief',
    sideEffects: 'Stomach pain, Nausea, Diarrhea',
  },
  aspirin: {
    usage: 'Pain relief, Fever reduction, Cardiovascular protection',
    sideEffects: 'Stomach irritation, Heartburn, Bleeding tendency',
  },
  vitamin_c: {
    usage: 'Immune support, Collagen synthesis, Iron absorption, Antioxidant',
    sideEffects: 'Mild stomach discomfort with large doses',
  },
  vitamin_d3: {
    usage: 'Bone health, Calcium absorption, Immune system support',
    sideEffects: 'Generally safe; nausea or hypercalcemia if severely overdosed',
  },
  vitamin_b_complex: {
    usage: 'Energy metabolism, Nerve health, Red blood cell formation',
    sideEffects: 'Bright yellow urine (harmless), Mild nausea',
  },
  calcium: {
    usage: 'Bone strength, Teeth maintenance, Osteoporosis prevention',
    sideEffects: 'Constipation, Bloating, Gas',
  },
  zinc: {
    usage: 'Immune defense, Wound healing, Skin repair',
    sideEffects: 'Nausea, Metallic taste if taken on empty stomach',
  },
  iron: {
    usage: 'Iron deficiency anemia, Hemoglobin production',
    sideEffects: 'Dark stools (normal), Constipation, Stomach upset',
  },
  folic_acid: {
    usage: 'Red blood cell production, Prenatal care, Neural tube defect prevention',
    sideEffects: 'Generally well-tolerated, rare bloating',
  },
}

export function getMedicineUsage(medicine) {
  if (!medicine) return 'As prescribed by physician'
  if (medicine.usage && typeof medicine.usage === 'string' && medicine.usage.trim()) {
    return medicine.usage
  }
  if (medicine.uses && Array.isArray(medicine.uses) && medicine.uses.length > 0) {
    return medicine.uses.join(', ')
  }
  if (typeof medicine.uses === 'string' && medicine.uses.trim()) {
    return medicine.uses
  }

  const rawName = (medicine.medicineName || medicine.name || '').toLowerCase().replace(/[^a-z0-9]/g, ' ')
  for (const [key, info] of Object.entries(MEDICINE_INFO_MAP)) {
    const cleanKey = key.replace(/_/g, ' ')
    if (rawName.includes(cleanKey) || cleanKey.includes(rawName)) {
      return info.usage
    }
  }

  return 'Treatment as indicated by consulting physician'
}

export function getMedicineSideEffects(medicine) {
  if (!medicine) return 'None specifically reported; consult physician if symptoms occur'
  if (medicine.sideEffects && Array.isArray(medicine.sideEffects) && medicine.sideEffects.length > 0) {
    return medicine.sideEffects.join(', ')
  }
  if (typeof medicine.sideEffects === 'string' && medicine.sideEffects.trim()) {
    return medicine.sideEffects
  }
  if (medicine.side_effects && Array.isArray(medicine.side_effects) && medicine.side_effects.length > 0) {
    return medicine.side_effects.join(', ')
  }
  if (typeof medicine.side_effects === 'string' && medicine.side_effects.trim()) {
    return medicine.side_effects
  }

  const rawName = (medicine.medicineName || medicine.name || '').toLowerCase().replace(/[^a-z0-9]/g, ' ')
  for (const [key, info] of Object.entries(MEDICINE_INFO_MAP)) {
    const cleanKey = key.replace(/_/g, ' ')
    if (rawName.includes(cleanKey) || cleanKey.includes(rawName)) {
      return info.sideEffects
    }
  }

  return 'Mild drowsiness, nausea, or dizziness (consult physician if symptoms persist)'
}
