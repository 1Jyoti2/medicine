/**
 * Plant Remedies Knowledge Helper.
 * Provides rich traditional herbal remedies fallback for medicinal plants.
 */

export const PLANT_REMEDIES_MAP = {
  'stephania japonica': [
    {
      name: 'Stephania Root Decoction (Joint Relief)',
      ingredients: ['Dried Stephania root / stem slices (3-5g)', 'Water (2 cups)', 'Licorice root (optional)'],
      preparation:
        'Simmer 3-5g of dried Stephania root in two cups of water for 15-20 minutes until reduced by half. Strain and drink warm once daily under traditional guidance.',
      traditionalUse:
        'Traditional herbal decoction used in Asian folk traditions for soothing joint stiffness and rheumatic aches.',
      precautions:
        'Contains active isoquinoline alkaloids. Avoid during pregnancy, lactation, or without consulting an herbal practitioner.',
    },
    {
      name: 'Stephania Leaf Warming Poultice',
      ingredients: ['Fresh Stephania leaves', 'A few drops of sesame oil'],
      preparation:
        'Crush fresh leaves into a poultice and gently warm with a few drops of sesame oil. Apply externally over affected joints or swelling with a clean cloth wrap for 15 minutes.',
      traditionalUse:
        'Traditional external poultice applied to reduce localized joint inflammation and discomfort.',
      precautions:
        'External use only. Test on a small patch of skin first to ensure no irritation.',
    },
  ],
  'centella asiatica': [
    {
      name: 'Gotu Kola Memory & Vitality Tonic',
      ingredients: ['Fresh Centella Asiatica leaves', 'Warm water or milk', 'Honey (optional)'],
      preparation:
        'Crush fresh leaves to extract 10-15 ml of pure juice. Mix with warm water or milk and honey. Consume in the morning.',
      traditionalUse:
        'Ayurvedic Medhya Rasayana beverage traditionally taken for memory retention, mental clarity, and nerve health.',
      precautions:
        'Avoid excessive intake. Discontinue if gastric discomfort occurs.',
    },
    {
      name: 'Gotu Kola Skin Soothing Paste',
      ingredients: ['Fresh Centella leaves', 'Rose water or clean water'],
      preparation:
        'Grind fresh leaves into a fine paste. Apply evenly to minor blemishes or irritated skin areas for 15-20 minutes, then rinse.',
      traditionalUse:
        'Traditional topical preparation used to promote skin revitalization and accelerate soothing.',
      precautions:
        'Do not apply to deep open wounds. Perform a skin patch test first.',
    },
  ],
  'coccinia grandis': [
    {
      name: 'Ivy Gourd Leaf Infusion for Blood Sugar',
      ingredients: ['Fresh Coccinia Grandis leaves', 'Water', 'Cumin seeds (optional)'],
      preparation:
        'Boil a handful of washed fresh leaves in two cups of water with a pinch of cumin seeds for 5 minutes. Strain and drink warm before meals.',
      traditionalUse:
        'Traditional Ayurvedic preparation consumed to support healthy glycemic balance and metabolic wellness.',
      precautions:
        'Monitor blood sugar levels regularly if taking antidiabetic medication to prevent hypoglycemia.',
    },
    {
      name: 'Cooling Coccinia Leaf Juice',
      ingredients: ['Fresh Coccinia leaves', 'Water', 'Pinch of black salt'],
      preparation:
        'Blend washed tender leaves with half a cup of water, strain, add a pinch of black salt, and drink fresh.',
      traditionalUse:
        'Traditional cooling tonic used to alleviate internal body heat and promote skin wellness.',
      precautions:
        'Consume freshly prepared; do not store overnight.',
    },
  ],
  'eclipta prostrata': [
    {
      name: 'Bhringraj Ayurvedic Hair Oil',
      ingredients: ['Fresh Eclipta Prostrata leaf juice', 'Pure virgin coconut oil or sesame oil'],
      preparation:
        'Simmer equal parts fresh leaf juice and coconut oil on low heat until moisture evaporates and dark green herbal oil remains. Cool and strain into a glass bottle.',
      traditionalUse:
        'Renowned Ayurvedic hair oil massaged into the scalp to strengthen roots, prevent premature greying, and stimulate hair vitality.',
      precautions:
        'For external scalp application only. Perform a skin patch test.',
    },
    {
      name: 'Bhringraj Leaf Liver Wellness Brew',
      ingredients: ['Dried Bhringraj herb', 'Water'],
      preparation:
        'Boil 3g of dried whole herb in a cup of water for 5 minutes. Strain and consume lukewarm.',
      traditionalUse:
        'Traditional herbal brew historically used for liver rejuvenation and natural detoxification.',
      precautions:
        'Consult an Ayurvedic practitioner before internal use.',
    },
  ],
  'mikania micrantha': [
    {
      name: 'Fresh Mikania Wound Poultice',
      ingredients: ['Fresh Mikania Micrantha leaves'],
      preparation:
        'Wash fresh tender leaves thoroughly. Crush between palms or with a pestle to release herbal juice. Apply directly onto minor cuts, scratches, or insect bites.',
      traditionalUse:
        'Traditional rapid styptic and antiseptic poultice used in rural areas to arrest minor bleeding and soothe wounds.',
      precautions:
        'Ensure leaves are thoroughly clean. Seek professional medical care for deep wounds.',
    },
    {
      name: 'Mikania Herbal Steam Inhalation',
      ingredients: ['Fresh Mikania leaves', 'Boiling water'],
      preparation:
        'Add a handful of leaves to a bowl of steaming water. Cover head with a towel and inhale herbal vapors for 5-10 minutes.',
      traditionalUse:
        'Traditional respiratory steam used for clearing nasal passages and soothing throat irritation.',
      precautions:
        'Keep a safe distance to avoid steam burns.',
    },
  ],
  'murraya koenigii': [
    {
      name: 'Curry Leaf Digestive Buttermilk',
      ingredients: ['Fresh curry leaves', 'Fresh buttermilk', 'Roasted cumin powder', 'Pinch of rock salt'],
      preparation:
        'Finely crush 8-10 fresh curry leaves and stir into a glass of spiced buttermilk. Drink after lunch.',
      traditionalUse:
        'Ayurvedic digestive drink supporting gut flora, appetite stimulation, and metabolism.',
      precautions:
        'Safe in standard dietary usage.',
    },
    {
      name: 'Curry Leaf & Fenugreek Hair Mask',
      ingredients: ['Fresh curry leaves', 'Soaked fenugreek seeds', 'Yogurt'],
      preparation:
        'Blend leaves and soaked fenugreek seeds into a smooth paste with yogurt. Apply to scalp for 25 minutes, then rinse.',
      traditionalUse:
        'Traditional hair care mask promoting follicular health and reducing dandruff.',
      precautions:
        'For external scalp use only.',
    },
  ],
}

export function getPlantRemedies(plant) {
  if (!plant) return []
  if (Array.isArray(plant.remedies) && plant.remedies.length > 0) {
    return plant.remedies
  }

  const rawName = (plant.name || '').toLowerCase().trim()
  const rawSciName = (plant.scientificName || '').toLowerCase().trim()

  for (const [key, remedies] of Object.entries(PLANT_REMEDIES_MAP)) {
    if (
      rawName.includes(key) ||
      key.includes(rawName) ||
      rawSciName.includes(key) ||
      key.includes(rawSciName)
    ) {
      return remedies
    }
  }

  return []
}
