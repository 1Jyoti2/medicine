const medicinalPlants = [
  {
    id: 1,
    name: 'Tulsi',
    scientificName: 'Ocimum sanctum',
    family: 'Lamiaceae',
    nativeRegion: 'Southeast Asia',
    imageUrl: '/images/plants/tulsi.jpg',
    uses: ['Respiratory relief', 'Stress reduction', 'Immunity booster'],
    activeCompounds: ['Eugenol', 'Carvacrol', 'Ursolic acid'],
    partsUsed: 'Leaves and seeds',
    precautions: ['Avoid with blood-thinning medication'],
    sideEffects: ['Drowsiness', 'Upset stomach'],
    storage: 'Keep fresh leaves in a sealed container in the refrigerator. Dried leaves: store in an airtight jar away from sunlight.',
    description:
      'Holy basil, widely used in Ayurveda for its adaptogenic and antimicrobial properties.',
    remedies: [
      {
        name: 'Tulsi Tea',
        ingredients: ['Fresh Tulsi leaves', 'Water', 'Honey (optional)'],
        preparation:
          'Wash a handful of fresh Tulsi leaves. Boil one cup of water, add the leaves and steep for 5–7 minutes, then strain. Sweeten with honey if desired.',
        traditionalUse:
          'Traditional preparation consumed as a herbal beverage for general wellness.',
        precautions:
          'For traditional informational purposes only. Stop use if you feel unwell and avoid during pregnancy or while taking blood-thinning medication.',
      },
      {
        name: 'Tulsi and Ginger Decoction',
        ingredients: ['Fresh Tulsi leaves', 'Ginger slices', 'Water'],
        preparation:
          'Crush the Tulsi leaves and ginger together. Simmer in two cups of water until reduced by half, then strain and drink warm.',
        traditionalUse:
          'Traditional drink used in households as a comfort beverage during seasonal changes.',
        precautions:
          'For informational purposes only. Not a substitute for medical treatment.',
      },
      {
        name: 'Tulsi Leaf Paste',
        ingredients: ['Fresh Tulsi leaves', 'A few drops of water or coconut oil'],
        preparation:
          'Grind fresh Tulsi leaves into a smooth paste with water or coconut oil. Apply the paste to the skin and rinse off after a short while.',
        traditionalUse:
          'Traditional topical preparation reportedly used as a skin-soothing application.',
        precautions:
          'Do a small patch test first. For informational purposes only.',
      },
    ],
  },
  {
    id: 2,
    name: 'Neem',
    scientificName: 'Azadirachta indica',
    family: 'Meliaceae',
    nativeRegion: 'Indian subcontinent',
    imageUrl: '/images/plants/neem.jpg',
    uses: ['Antibacterial', 'Antifungal', 'Skin and dental care'],
    activeCompounds: ['Azadirachtin', 'Nimbin', 'Quercetin'],
    partsUsed: 'Leaves, bark and seeds',
    precautions: ['Not recommended during pregnancy'],
    sideEffects: ['Stomach irritation', 'Low blood sugar'],
    storage: 'Store dried leaves in a cool, dry, dark place in an airtight container.',
    description:
      'A versatile medicinal tree valued for its purifying and skin-healing properties.',
    remedies: [
      {
        name: 'Neem Leaf Bath Infusion',
        ingredients: ['Fresh or dried Neem leaves', 'Hot water'],
        preparation:
          'Boil a handful of Neem leaves in a large pot of water for 10 minutes. Let the water cool to a comfortable temperature and use it as a traditional bathing rinse.',
        traditionalUse:
          'Traditional preparation used as a soothing bathing rinse in some regions.',
        precautions:
          'For informational purposes only. Not recommended during pregnancy.',
      },
      {
        name: 'Neem Leaf Paste',
        ingredients: ['Fresh Neem leaves', 'Turmeric powder', 'Water'],
        preparation:
          'Grind fresh Neem leaves with a pinch of turmeric and enough water to form a paste. Apply to the skin, leave briefly, and rinse off.',
        traditionalUse:
          'Traditional topical preparation historically applied to the skin.',
        precautions:
          'Do a small patch test before use. For informational purposes only.',
      },
      {
        name: 'Neem Leaf Tea',
        ingredients: ['Fresh Neem leaves', 'Water'],
        preparation:
          'Simmer a few washed Neem leaves in a cup of water for 5 minutes. Strain and drink lukewarm.',
        traditionalUse:
          'Traditional herbal beverage prepared in some households as a general wellness drink.',
        precautions:
          'For informational purposes only. Consume in small amounts and stop if you experience stomach irritation.',
      },
    ],
  },
  {
    id: 3,
    name: 'Aloe Vera',
    scientificName: 'Aloe barbadensis miller',
    family: 'Asphodelaceae',
    nativeRegion: 'Arabian Peninsula',
    imageUrl: '/images/plants/aloe-vera.jpg',
    uses: ['Skin healing', 'Hydration', 'Digestion support'],
    activeCompounds: ['Aloin', 'Anthraquinones', 'Polysaccharides'],
    partsUsed: 'Leaf gel and latex',
    precautions: ['Remove the yellow latex layer before use'],
    sideEffects: ['Abdominal cramps', 'Diarrhoea'],
    storage: 'Keep cut leaves refrigerated below 25°C. Gel can be stored in an airtight container.',
    description:
      'Succulent plant whose gel soothes burns, hydrates the skin and aids digestion.',
    remedies: [
      {
        name: 'Fresh Aloe Gel Application',
        ingredients: ['Fresh Aloe Vera leaf', 'Clean spoon'],
        preparation:
          'Slice open a mature Aloe Vera leaf, scoop out the clear gel with a clean spoon, and apply it directly to the skin. Rinse after a short while.',
        traditionalUse:
          'Traditional topical preparation used as a cooling skin application.',
        precautions:
          'Remove the yellow latex layer before use. For informational purposes only.',
      },
      {
        name: 'Aloe and Honey Drink',
        ingredients: ['Fresh Aloe Vera gel', 'Honey', 'Water'],
        preparation:
          'Blend a small spoon of fresh aloe gel, one teaspoon of honey and a glass of water. Drink it fresh.',
        traditionalUse:
          'Traditional preparation consumed as a general wellness drink.',
        precautions:
          'For informational purposes only. Start with a small amount and avoid if you are pregnant or have digestive sensitivities.',
      },
    ],
  },
  {
    id: 4,
    name: 'Mint',
    scientificName: 'Mentha',
    family: 'Lamiaceae',
    nativeRegion: 'Europe and Asia',
    imageUrl: '/images/plants/mint.jpg',
    uses: ['Digestion aid', 'Nausea relief', 'Breath freshener'],
    activeCompounds: ['Menthol', 'Menthone', 'Rosmarinic acid'],
    partsUsed: 'Leaves and oil',
    precautions: ['May worsen acid reflux in sensitive people'],
    sideEffects: ['Heartburn', 'Allergic reaction (rare)'],
    storage: 'Store fresh sprigs in the refrigerator with stems in water. Dried leaves: keep in an airtight container.',
    description:
      'A fragrant herb used to calm the stomach, relieve nausea and freshen breath.',
    remedies: [
      {
        name: 'Mint Tea',
        ingredients: ['Fresh Mint leaves', 'Water'],
        preparation:
          'Wash a handful of fresh mint leaves and steep them in a cup of hot water for 5 minutes. Strain and drink warm.',
        traditionalUse:
          'Traditional herbal beverage enjoyed for its refreshing taste and soothing properties.',
        precautions:
          'For informational purposes only. May worsen acid reflux in sensitive people.',
      },
      {
        name: 'Mint and Lemon Infusion',
        ingredients: ['Fresh Mint leaves', 'Lemon slices', 'Water'],
        preparation:
          'Add fresh mint leaves and lemon slices to a cup of warm water. Let it infuse for 5 minutes and drink.',
        traditionalUse:
          'Traditional preparation consumed as a refreshing wellness drink.',
        precautions:
          'For informational purposes only. Not a substitute for medical advice.',
      },
    ],
  },
  {
    id: 5,
    name: 'Curry Leaves',
    scientificName: 'Murraya koenigii',
    family: 'Rutaceae',
    nativeRegion: 'India and Sri Lanka',
    imageUrl: '/images/plants/curry-leaves.jpg',
    uses: ['Digestion support', 'Blood sugar regulation', 'Hair care'],
    activeCompounds: ['Carbazole alkaloids', 'Limonene'],
    partsUsed: 'Leaves',
    precautions: ['Consult a doctor if pregnant'],
    sideEffects: ['Mild stomach upset'],
    storage: 'Store fresh leaves in the refrigerator. Dried leaves: keep in an airtight container away from moisture.',
    description:
      'Aromatic leaves common in South Asian cooking with well-known digestive benefits.',
    remedies: [
      {
        name: 'Curry Leaf Infusion',
        ingredients: ['Fresh Curry Leaves', 'Water'],
        preparation:
          'Simmer a handful of fresh curry leaves in a cup of water for 5 minutes. Strain and drink warm.',
        traditionalUse:
          'Traditional preparation consumed as a herbal beverage after meals.',
        precautions:
          'For informational purposes only. Consult a doctor if pregnant.',
      },
      {
        name: 'Curry Leaf and Buttermilk Drink',
        ingredients: ['Fresh Curry Leaves', 'Buttermilk'],
        preparation:
          'Blend a few fresh curry leaves with a glass of buttermilk and consume fresh.',
        traditionalUse:
          'Traditional preparation used as a digestive wellness drink in some regions.',
        precautions:
          'For informational purposes only. Stop if you experience mild stomach upset.',
      },
      {
        name: 'Curry Leaf Hair Paste',
        ingredients: ['Fresh Curry Leaves', 'Coconut oil'],
        preparation:
          'Grind fresh curry leaves into a paste and mix with a little coconut oil. Apply to the scalp and hair, leave for 20 minutes, then rinse with mild shampoo.',
        traditionalUse:
          'Traditional preparation used as a hair care application in some households.',
        precautions:
          'For informational purposes only. Do a small patch test before full application.',
      },
    ],
  },
  {
    id: 6,
    name: 'Betel Leaf',
    scientificName: 'Piper betle',
    family: 'Piperaceae',
    nativeRegion: 'South and Southeast Asia',
    imageUrl: '/images/plants/betel-leaf.jpg',
    uses: ['Antiseptic properties', 'Wound healing support', 'Oral care'],
    activeCompounds: ['Chavibetol', 'Allylpyrocatechol'],
    partsUsed: 'Leaves',
    precautions: ['Limited use in chewing preparations'],
    sideEffects: ['Mouth irritation', 'Drowsiness'],
    storage: 'Store fresh leaves wrapped and refrigerated; use within a few days.',
    description:
      'Widely used in traditional medicine for its antimicrobial and healing actions.',
    remedies: [
      {
        name: 'Betel Leaf Wash Rinse',
        ingredients: ['Fresh Betel Leaves', 'Water'],
        preparation:
          'Simmer a few fresh betel leaves in a cup of water for 5 minutes. Allow it to cool and use as a traditional mouthwash rinse.',
        traditionalUse:
          'Traditional preparation used as a mouth rinse for general oral care.',
        precautions:
          'Do not swallow the rinse. For informational purposes only.',
      },
      {
        name: 'Betel Leaf Paste',
        ingredients: ['Fresh Betel Leaves', 'Water'],
        preparation:
          'Grind fresh betel leaves with a little water to form a paste. Apply to the skin, let it sit briefly, then rinse off.',
        traditionalUse:
          'Traditional topical preparation historically applied to the skin.',
        precautions:
          'Limited use recommended. Do a patch test first and avoid prolonged contact, as it may cause mouth or skin irritation.',
      },
    ],
  },
  {
    id: 7,
    name: 'Ashwagandha',
    scientificName: 'Withania somnifera',
    family: 'Solanaceae',
    nativeRegion: 'India',
    imageUrl: '/images/plants/ashwagandha.jpg',
    uses: ['Stress relief', 'Energy and vitality', 'Improves sleep'],
    activeCompounds: ['Withanolides', 'Alkaloids'],
    partsUsed: 'Root and leaves',
    precautions: ['Avoid with thyroid medication'],
    sideEffects: ['Drowsiness', 'Upset stomach'],
    storage: 'Store powder in an airtight container away from moisture and direct sunlight.',
    description:
      'An adaptogenic herb traditionally used to reduce stress and boost overall vitality.',
    remedies: [
      {
        name: 'Ashwagandha Milk',
        ingredients: ['Ashwagandha root powder', 'Warm milk', 'Honey (optional)'],
        preparation:
          'Stir half a teaspoon of Ashwagandha root powder into a cup of warm milk. Sweeten with honey if desired and drink before sleeping.',
        traditionalUse:
          'Traditional preparation consumed as a calming night-time beverage.',
        precautions:
          'For informational purposes only. Avoid with thyroid medication and do not exceed the recommended amount.',
      },
      {
        name: 'Ashwagandha Decoction',
        ingredients: ['Ashwagandha root powder', 'Water'],
        preparation:
          'Boil half a teaspoon of Ashwagandha root powder in a cup of water for 5 minutes. Strain and drink warm.',
        traditionalUse:
          'Traditional preparation used as a general wellness drink in Ayurvedic practice.',
        precautions:
          'For informational purposes only. Avoid with thyroid medication and consult a healthcare professional before use.',
      },
    ],
  },
  {
    id: 8,
    name: 'Giloy',
    scientificName: 'Tinospora cordifolia',
    family: 'Menispermaceae',
    nativeRegion: 'India',
    imageUrl: '/images/plants/giloy.jpg',
    uses: ['Immunity support', 'Fever management', 'Detoxification'],
    activeCompounds: ['Tinosporin', 'Berberine', 'Polysaccharides'],
    partsUsed: 'Stem and leaves',
    precautions: ['Avoid before surgery'],
    sideEffects: ['Digestive upset'],
    storage: 'Store dried stem pieces in a cool, dry place in an airtight container.',
    description:
      'Known as the root of immortality in Ayurveda for its immune-boosting effects.',
    remedies: [
      {
        name: 'Giloy Stem Decoction',
        ingredients: ['Dried Giloy stem pieces', 'Water'],
        preparation:
          'Boil a few dried Giloy stem pieces in two cups of water until reduced by half. Strain and drink warm.',
        traditionalUse:
          'Traditional Ayurvedic preparation used as a general wellness beverage.',
        precautions:
          'For informational purposes only. Avoid before surgery and consult a healthcare professional before use.',
      },
      {
        name: 'Giloy Juice',
        ingredients: ['Fresh Giloy stem', 'Water'],
        preparation:
          'Wash the fresh stem, crush it and extract the juice. Mix with a little water and drink fresh.',
        traditionalUse:
          'Traditional preparation consumed as a fresh wellness drink in some households.',
        precautions:
          'For informational purposes only. Stop if you experience digestive upset.',
      },
      {
        name: 'Giloy and Tulsi Infusion',
        ingredients: ['Dried Giloy stem pieces', 'Fresh Tulsi leaves', 'Water'],
        preparation:
          'Simmer Giloy stem pieces and Tulsi leaves together in water for 5 minutes. Strain and drink warm.',
        traditionalUse:
          'Traditional herbal preparation combining two commonly used wellness herbs.',
        precautions:
          'For informational purposes only. Avoid before surgery and consult a healthcare professional before use.',
      },
    ],
  },
  {
    id: 9,
    name: 'Stephania Japonica',
    scientificName: 'Stephania japonica',
    family: 'Menispermaceae',
    nativeRegion: 'East and South Asia, Australasia',
    imageUrl: '/images/plants/stephania-japonica.jpg',
    uses: ['Joint pain relief', 'Anti-inflammatory', 'Anti-rheumatic', 'Fever management', 'Blood circulation improvement', 'Diuretic effects'],
    activeCompounds: ['Alkaloids (stephanine, cepharanthine)', 'Tetrandrine', 'Berbamine', 'Flavonoids', 'Phenolic compounds'],
    partsUsed: 'Root and tuber primarily, leaves occasionally',
    precautions: ['Contains potent alkaloids; strictly follow dosage guidelines', 'Avoid during pregnancy and breastfeeding', 'May interact with blood pressure medications'],
    sideEffects: ['Nausea or vomiting', 'Dizziness', 'Low blood pressure', 'Digestive discomfort'],
    storage: 'Store dried root and leaves in a cool, dark, dry place in an airtight glass container.',
    description:
      'Stephania japonica is a climbing vine traditionally used in Chinese and Japanese herbal medicine, particularly valued for its analgesic and anti-rheumatic properties.',
    remedies: [
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
  },
  {
    id: 10,
    name: 'Centella Asiatica',
    scientificName: 'Centella asiatica',
    family: 'Apiaceae',
    nativeRegion: 'Asia (India, Sri Lanka, China)',
    imageUrl: '/images/plants/centella-asiatica.jpg',
    uses: ['Cognitive enhancement', 'Wound healing', 'Skin repair', 'Anxiety & stress reduction'],
    activeCompounds: ['Asiaticoside', 'Madecassoside', 'Asiatic acid', 'Flavonoids'],
    partsUsed: 'Whole plant, leaves',
    precautions: ['Avoid in high doses during pregnancy', 'Consult doctor before surgery'],
    sideEffects: ['Mild stomach upset', 'Drowsiness'],
    storage: 'Store dried leaves in an airtight container away from light and moisture.',
    description:
      'Centella asiatica (Gotu Kola) is a renowned Ayurvedic herb for brain health, memory enhancement, and dermatological healing.',
    remedies: [
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
  },
  {
    id: 11,
    name: 'Coccinia Grandis',
    scientificName: 'Coccinia grandis',
    family: 'Cucurbitaceae',
    nativeRegion: 'Tropical Asia and Africa',
    imageUrl: '/images/plants/coccinia-grandis.jpg',
    uses: ['Blood sugar regulation', 'Anti-inflammatory', 'Antioxidant support', 'Liver protection'],
    activeCompounds: ['Cephalandrin', 'Beta-carotene', 'Flavonoids', 'Vitamin C'],
    partsUsed: 'Leaves and fruits',
    precautions: ['Monitor blood glucose if taking diabetes medication'],
    sideEffects: ['Hypoglycemia if combined with insulin'],
    storage: 'Keep fresh leaves refrigerated. Dried leaves: store in an airtight jar.',
    description:
      'Coccinia grandis (Ivy Gourd / Tindora) is traditionally used in Ayurvedic medicine for managing diabetes and metabolic health.',
    remedies: [
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
  },
  {
    id: 12,
    name: 'Eclipta Prostrata',
    scientificName: 'Eclipta prostrata',
    family: 'Asteraceae',
    nativeRegion: 'Tropical & Subtropical regions',
    imageUrl: '/images/plants/eclipta-prostrata.jpg',
    uses: ['Hair growth & vitality', 'Liver rejuvenation', 'Skin wellness', 'Antimicrobial'],
    activeCompounds: ['Wedelolactone', 'Demethylwedelolactone', 'Ecliptine', 'Flavonoids'],
    partsUsed: 'Leaves and whole herb',
    precautions: ['Avoid during pregnancy without medical consultation'],
    sideEffects: ['Mild chilliness in sensitive individuals'],
    storage: 'Store powder or dried herb in an airtight container away from heat.',
    description:
      'Eclipta prostrata (Bhringraj) is the "King of Herbs" for hair nourishment, liver detoxification, and vitality in Ayurveda.',
    remedies: [
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
  },
  {
    id: 13,
    name: 'Mikania Micrantha',
    scientificName: 'Mikania micrantha',
    family: 'Asteraceae',
    nativeRegion: 'Central and South America, naturalized in Asia',
    imageUrl: '/images/plants/mikania-micrantha.jpg',
    uses: ['Wound healing & clotting', 'Antibacterial', 'Fever reduction', 'Pain relief'],
    activeCompounds: ['Mikanolide', 'Dihydromikanolide', 'Sesquiterpene lactones'],
    partsUsed: 'Leaves',
    precautions: ['External application preferred; internal use only under guidance'],
    sideEffects: ['Skin dermatitis in rare allergic individuals'],
    storage: 'Use fresh leaves directly or dry in the shade.',
    description:
      'Mikania micrantha (Bitter Vine) is traditionally applied topically as a rapid coagulant and antiseptic on acute wounds.',
    remedies: [
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
  },
]

const pharmaceuticalMedicines = [
  {
    id: 1,
    name: 'Paracetamol',
    genericName: 'Acetaminophen',
    composition: 'Acetaminophen BP 500 mg',
    category: 'Analgesic / Antipyretic',
    dosage: '500 mg',
    imageUrl: '/images/tablets/paracetamol.jpg',
    uses: ['Fever reduction', 'Mild to moderate pain relief'],
    sideEffects: ['Nausea', 'Skin rash (rare)'],
    precautions: ['Do not exceed 4 g per day'],
    storage: 'Store below 25°C in a dry place',
    manufacturer: 'MedLeaf Pharma Ltd',
    description:
      'A widely used pain reliever and fever reducer suitable for adults and children.',
  },
  {
    id: 2,
    name: 'Ibuprofen',
    genericName: 'Ibuprofen',
    composition: 'Ibuprofen 200 mg',
    category: 'NSAID',
    dosage: '200 mg',
    imageUrl: '/images/tablets/ibuprofen.jpg',
    uses: ['Anti-inflammatory pain relief', 'Fever reduction'],
    sideEffects: ['Stomach upset', 'Dizziness'],
    precautions: ['Take with food', 'Avoid in stomach ulcers'],
    storage: 'Store below 25°C away from light',
    manufacturer: 'MedLeaf Pharma Ltd',
    description:
      'A non-steroidal anti-inflammatory drug for pain, fever and inflammation.',
  },
  {
    id: 3,
    name: 'Amoxicillin',
    genericName: 'Amoxicillin trihydrate',
    composition: 'Amoxicillin trihydrate 500 mg',
    category: 'Antibiotic',
    dosage: '500 mg',
    imageUrl: '/images/tablets/amoxicillin.jpg',
    uses: ['Bacterial infection treatment'],
    sideEffects: ['Diarrhoea', 'Nausea'],
    precautions: ['Complete the full course'],
    storage: 'Keep in a cool, dry place',
    manufacturer: 'MedLeaf Pharma Ltd',
    description:
      'A penicillin-type antibiotic effective against a wide range of bacterial infections.',
  },
  {
    id: 4,
    name: 'Metformin',
    genericName: 'Metformin hydrochloride',
    composition: 'Metformin hydrochloride 500 mg',
    category: 'Antidiabetic',
    dosage: '500 mg',
    imageUrl: '/images/tablets/metformin.jpg',
    uses: ['Type 2 diabetes management'],
    sideEffects: ['Stomach upset', 'Metallic taste'],
    precautions: ['Monitor kidney function'],
    storage: 'Store below 25°C',
    manufacturer: 'MedLeaf Pharma Ltd',
    description:
      'First-line medication to improve blood sugar control in type 2 diabetes.',
  },
  {
    id: 5,
    name: 'Cetirizine',
    genericName: 'Cetirizine hydrochloride',
    composition: 'Cetirizine hydrochloride 10 mg',
    category: 'Antihistamine',
    dosage: '10 mg',
    imageUrl: '/images/tablets/cetirizine.jpg',
    uses: ['Allergy relief', 'Sneezing and runny nose'],
    sideEffects: ['Drowsiness', 'Dry mouth'],
    precautions: ['Avoid alcohol'],
    storage: 'Store in a cool, dry place',
    manufacturer: 'MedLeaf Pharma Ltd',
    description:
      'A second-generation antihistamine used to treat allergy symptoms.',
  },
  {
    id: 6,
    name: 'Vitamin C',
    genericName: 'Ascorbic acid',
    composition: 'Ascorbic acid 500 mg',
    category: 'Supplement',
    dosage: '500 mg',
    imageUrl: '/images/tablets/vitamin-c.jpg',
    uses: ['Immune system support', 'Iron absorption'],
    sideEffects: ['Mild stomach discomfort'],
    precautions: ['Within recommended dosage'],
    storage: 'Store below 25°C away from light',
    manufacturer: 'MedLeaf Pharma Ltd',
    description:
      'An essential water-soluble vitamin commonly used as a daily supplement.',
  },
  {
    id: 7,
    name: 'Omeprazole',
    genericName: 'Omeprazole',
    composition: 'Omeprazole 20 mg',
    category: 'Proton Pump Inhibitor',
    dosage: '20 mg',
    imageUrl: '/images/tablets/omeprazole.jpg',
    uses: ['Acid reflux relief', 'Gastric ulcer treatment'],
    sideEffects: ['Headache', 'Abdominal pain'],
    precautions: ['Take before a meal'],
    storage: 'Store below 25°C',
    manufacturer: 'MedLeaf Pharma Ltd',
    description:
      'Reduces stomach acid production for heartburn and ulcer management.',
  },
  {
    id: 8,
    name: 'Amlodipine',
    genericName: 'Amlodipine besylate',
    composition: 'Amlodipine besylate 5 mg',
    category: 'Calcium Channel Blocker',
    dosage: '5 mg',
    imageUrl: '/images/tablets/amlodipine.jpg',
    uses: ['Blood pressure control', 'Angina relief'],
    sideEffects: ['Ankle swelling', 'Flushing'],
    precautions: ['Avoid grapefruit juice'],
    storage: 'Store below 30°C',
    manufacturer: 'MedLeaf Pharma Ltd',
    description:
      'Helps relax blood vessels to lower blood pressure and reduce chest pain.',
  },
]

const leafDetectionResults = [
  {
    id: 'leaf-001',
    plant: medicinalPlants[0],
    confidence: 94.6,
    imageUrl: '/images/uploads/tulsi-sample.jpg',
    analyzedAt: '2026-09-01T10:24:00Z',
    model: 'leafnet-v1',
    status: 'success',
  },
  {
    id: 'leaf-002',
    plant: medicinalPlants[1],
    confidence: 91.2,
    imageUrl: '/images/uploads/neem-sample.jpg',
    analyzedAt: '2026-09-01T09:10:00Z',
    model: 'leafnet-v1',
    status: 'success',
  },
  {
    id: 'leaf-003',
    plant: medicinalPlants[3],
    confidence: 88.5,
    imageUrl: '/images/uploads/mint-sample.jpg',
    analyzedAt: '2026-08-31T18:44:00Z',
    model: 'leafnet-v1',
    status: 'success',
  },
  {
    id: 'leaf-004',
    plant: medicinalPlants[6],
    confidence: 79.3,
    imageUrl: '/images/uploads/ashwagandha-sample.jpg',
    analyzedAt: '2026-08-30T14:02:00Z',
    model: 'leafnet-v1',
    status: 'low_confidence',
  },
  {
    id: 'leaf-005',
    plant: medicinalPlants[6],
    confidence: 52.1,
    imageUrl: '/images/uploads/unidentified-leaf.jpg',
    analyzedAt: '2026-08-28T11:37:00Z',
    model: 'leafnet-v1',
    status: 'uncertain',
  },
]

const tabletDetectionResults = [
  {
    id: 'tablet-001',
    medicine: pharmaceuticalMedicines[0],
    confidence: 96.2,
    imageUrl: '/images/uploads/paracetamol-sample.jpg',
    analyzedAt: '2026-09-01T10:30:00Z',
    model: 'tabletnet-v1',
    status: 'success',
  },
  {
    id: 'tablet-002',
    medicine: pharmaceuticalMedicines[2],
    confidence: 93.1,
    imageUrl: '/images/uploads/amoxicillin-sample.jpg',
    analyzedAt: '2026-09-01T08:55:00Z',
    model: 'tabletnet-v1',
    status: 'success',
  },
  {
    id: 'tablet-003',
    medicine: pharmaceuticalMedicines[4],
    confidence: 89.7,
    imageUrl: '/images/uploads/cetirizine-sample.jpg',
    analyzedAt: '2026-08-31T21:15:00Z',
    model: 'tabletnet-v1',
    status: 'success',
  },
  {
    id: 'tablet-004',
    medicine: pharmaceuticalMedicines[5],
    confidence: 74.8,
    imageUrl: '/images/uploads/vitamin-c-sample.jpg',
    analyzedAt: '2026-08-30T16:40:00Z',
    model: 'tabletnet-v1',
    status: 'low_confidence',
  },
  {
    id: 'tablet-005',
    medicine: pharmaceuticalMedicines[7],
    confidence: 58.3,
    imageUrl: '/images/uploads/unidentified-tablet.jpg',
    analyzedAt: '2026-08-27T12:05:00Z',
    model: 'tabletnet-v1',
    status: 'uncertain',
  },
]

const prescriptionResults = [
  {
    id: 'rx-001',
    prescriptionNumber: 'RX-2026-0042',
    patientName: 'Kasun Perera',
    patientAge: 34,
    doctorName: 'Dr. Nimali Fernando',
    organization: 'City General Hospital',
    issuedDate: '2026-09-01',
    extractedText: `CITY GENERAL HOSPITAL
Attn: Dr. Nimali Fernando
Patient: Kasun Perera, 34 years
Rx No: RX-2026-0042        Date: 2026-09-01

1. Paracetamol 500 mg  - Twice daily - 5 days - Take after food
2. Vitamin C 500 mg    - Once daily - 10 days - In the morning
                                             Dr. Nimali Fernando`,
    medicines: [
      {
        medicineName: 'Paracetamol',
        dosage: '500 mg',
        frequency: 'Twice daily',
        duration: '5 days',
        notes: 'Take after food',
      },
      {
        medicineName: 'Vitamin C',
        dosage: '500 mg',
        frequency: 'Once daily',
        duration: '10 days',
        notes: 'In the morning',
      },
    ],
    status: 'processed',
  },
  {
    id: 'rx-002',
    prescriptionNumber: 'RX-2026-0037',
    patientName: 'Nadeesha Silva',
    patientAge: 28,
    doctorName: 'Dr. Ruwan Jayasuriya',
    organization: 'Green Valley Clinic',
    issuedDate: '2026-08-29',
    extractedText: `GREEN VALLEY CLINIC
Attn: Dr. Ruwan Jayasuriya
Patient: Nadeesha Silva, 28 years
Rx No: RX-2026-0037        Date: 2026-08-29

1. Cetirizine 10 mg  - Once daily - 7 days - At night
2. Ibuprofen 200 mg  - As needed - 3 days - Max 3 tablets daily
                                            Dr. Ruwan Jayasuriya`,
    medicines: [
      {
        medicineName: 'Cetirizine',
        dosage: '10 mg',
        frequency: 'Once daily',
        duration: '7 days',
        notes: 'At night',
      },
      {
        medicineName: 'Ibuprofen',
        dosage: '200 mg',
        frequency: 'As needed',
        duration: '3 days',
        notes: 'Max 3 tablets daily',
      },
    ],
    status: 'processed',
  },
  {
    id: 'rx-003',
    prescriptionNumber: 'RX-2026-0031',
    patientName: 'Dilan Kumara',
    patientAge: 45,
    doctorName: 'Dr. Nimali Fernando',
    organization: 'City General Hospital',
    issuedDate: '2026-08-26',
    extractedText: `CITY GENERAL HOSPITAL
Attn: Dr. Nimali Fernando
Patient: Dilan Kumara, 45 years
Rx No: RX-2026-0031        Date: 2026-08-26

1. Metformin 500 mg  - Twice daily - 30 days - With meals
                                             Dr. Nimali Fernando`,
    medicines: [
      {
        medicineName: 'Metformin',
        dosage: '500 mg',
        frequency: 'Twice daily',
        duration: '30 days',
        notes: 'With meals',
      },
    ],
    status: 'reading',
  },
]

const detectionHistory = [
  {
    id: 'hist-001',
    name: 'Tulsi',
    type: 'Leaf',
    confidence: 94.6,
    date: '2026-09-01 10:24',
    status: 'success',
    resultId: 'leaf-001',
    imageUrl: '/images/uploads/tulsi-sample.jpg',
  },
  {
    id: 'hist-002',
    name: 'Paracetamol',
    type: 'Tablet',
    confidence: 96.2,
    date: '2026-09-01 10:30',
    status: 'success',
    resultId: 'tablet-001',
    imageUrl: '/images/uploads/paracetamol-sample.jpg',
  },
  {
    id: 'hist-003',
    name: 'Amoxicillin',
    type: 'Tablet',
    confidence: 93.1,
    date: '2026-09-01 08:55',
    status: 'success',
    resultId: 'tablet-002',
    imageUrl: '/images/uploads/amoxicillin-sample.jpg',
  },
  {
    id: 'hist-004',
    name: 'Neem',
    type: 'Leaf',
    confidence: 91.2,
    date: '2026-09-01 09:10',
    status: 'success',
    resultId: 'leaf-002',
    imageUrl: '/images/uploads/neem-sample.jpg',
  },
  {
    id: 'hist-005',
    name: 'Ashwagandha',
    type: 'Leaf',
    confidence: 79.3,
    date: '2026-08-30 14:02',
    status: 'pending',
    resultId: 'leaf-004',
    imageUrl: '/images/uploads/ashwagandha-sample.jpg',
  },
  {
    id: 'hist-006',
    name: 'RX-2026-0042',
    type: 'Prescription',
    confidence: null,
    date: '2026-09-01 10:45',
    status: 'success',
    resultId: 'rx-001',
    imageUrl: '/images/uploads/prescription-sample.jpg',
  },
  {
    id: 'hist-007',
    name: 'Unidentified tablet',
    type: 'Tablet',
    confidence: 58.3,
    date: '2026-08-27 12:05',
    status: 'failed',
    resultId: 'tablet-005',
    imageUrl: '/images/uploads/unidentified-tablet.jpg',
  },
]

function getPlantById(id) {
  return medicinalPlants.find((plant) => plant.id === id) ?? null
}

function getMedicineById(id) {
  return pharmaceuticalMedicines.find((medicine) => medicine.id === id) ?? null
}

function getLeafResultById(id) {
  return leafDetectionResults.find((result) => result.id === id) ?? null
}

function getTabletResultById(id) {
  return tabletDetectionResults.find((result) => result.id === id) ?? null
}

function getPrescriptionById(id) {
  return prescriptionResults.find((result) => result.id === id) ?? null
}

function getHistoryById(id) {
  return detectionHistory.find((entry) => entry.id === id) ?? null
}

const mockData = {
  medicinalPlants,
  pharmaceuticalMedicines,
  leafDetectionResults,
  tabletDetectionResults,
  prescriptionResults,
  detectionHistory,
}

export {
  medicinalPlants,
  pharmaceuticalMedicines,
  leafDetectionResults,
  tabletDetectionResults,
  prescriptionResults,
  detectionHistory,
  getPlantById,
  getMedicineById,
  getLeafResultById,
  getTabletResultById,
  getPrescriptionById,
  getHistoryById,
  medicinalPlants as medicinalLeaves,
  pharmaceuticalMedicines as pharmaceuticalTablets,
}

export default mockData