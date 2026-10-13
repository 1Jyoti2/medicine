const translations = {
  en: {
    // Navbar
    'nav.home': 'Home',
    'nav.leaf': 'Leaf Detection',
    'nav.tablet': 'Tablet Detection',
    'nav.prescription': 'Prescription',
    'nav.history': 'History',
    'nav.howItWorks': 'How It Works',
    'nav.about': 'About',
    'nav.signIn': 'Sign In',
    'nav.signUp': 'Sign Up',
    'nav.logOut': 'Log Out',

    // Common
    'common.back': 'Back',

    // Hero
    'hero.badge': 'Machine Learning · Healthcare AI',
    'hero.title.line1': 'Machine Learning Approach for Detecting',
    'hero.title.line2': 'the Medicinal Leaves',
    'hero.title.amp': '&',
    'hero.title.line3': 'Pharmaceutical Tablets',
    'hero.subtitle':
      'Identify medicinal plants, pharmaceutical tablets, and extract medicine information from prescriptions using intelligent image analysis.',
    'hero.ctaLeaf': 'Identify Medicinal Leaf',
    'hero.ctaTablet': 'Identify Tablet',
    'hero.ctaPrescription': 'Scan Prescription',
    'hero.visual.scanning': 'SCANNING',
    'hero.visual.leafDetected': 'Leaf detected',
    'hero.visual.tabletMatched': 'Tablet matched',
    'hero.visual.rxExtracted': 'Rx extracted',
    'hero.visual.aiActive': 'AI Model Active',
    'hero.visual.tablet': 'Tablet',
    'hero.visual.paracetamol': 'Paracetamol',
    'hero.visual.prescription': 'Prescription',
    'hero.visual.rx': 'Rx #0042',
    'hero.visual.confidence': 'Confidence 96.2%',

    // Features
    'features.eyebrow': 'Features',
    'features.title': 'Smart Detection for Everyday Healthcare',
    'features.subtitle':
      'Three powerful tools that turn images into accurate, understandable medicine information.',
    'features.leaf.title': 'Medicinal Leaf Detection',
    'features.leaf.desc':
      'Upload a photo of any leaf and the model instantly recognises medicinal species, uncovering their common uses and properties.',
    'features.leaf.cta': 'Identify Leaf',
    'features.tablet.title': 'Tablet Recognition',
    'features.tablet.desc':
      'Snap a pharmaceutical tablet and get its name, generic composition, dosage and usage details within seconds.',
    'features.tablet.cta': 'Identify Tablet',
    'features.rx.title': 'Prescription Scanner',
    'features.rx.desc':
      'Scan handwritten or printed prescriptions to automatically extract medicine information and medication history.',
    'features.rx.cta': 'Scan Prescription',

    // How it works (Home)
    'home.howItWorks.eyebrow': 'How It Works',
    'home.howItWorks.title': 'From Image to Answer in Four Steps',
    'home.howItWorks.subtitle':
      'A simple, transparent pipeline powered by a trained machine learning model.',
    'home.steps.upload.title': 'Upload Image',
    'home.steps.upload.desc':
      'Capture or upload a clear image of the leaf, tablet or prescription you want to identify.',
    'home.steps.analysis.title': 'Image Analysis',
    'home.steps.analysis.desc':
      'Our pipeline cleans the image, removes noise and prepares it for the recognition model.',
    'home.steps.prediction.title': 'AI Prediction',
    'home.steps.prediction.desc':
      'The trained model classifies the item and assigns a confidence score to the prediction.',
    'home.steps.display.title': 'Information Display',
    'home.steps.display.desc':
      'View the medicinal name, properties, dosage guidance and references in a clear report.',

    // CTA
    'cta.title': 'Start Detecting in Seconds',
    'cta.subtitle':
      'Upload an image and let the model reveal what the medicine is, what it treats, and how it is used.',
    'cta.button': 'Try It Now',

    // About page
    'about.eyebrow': 'About This Project',
    'about.title': 'MedScan AI',
    'about.subtitle':
      'A Machine Learning Approach for Detecting Medicinal Leaves and Pharmaceutical Tablets',
    'about.projectTitle': 'Final-Year Academic Project',
    'about.department': 'Department of Computer Science & Engineering',
    'about.para1':
      'MedScan AI is a final-year undergraduate project that explores the application of machine learning in the domain of pharmaceutical and botanical identification. The project aims to develop an intelligent system capable of identifying medicinal leaves, recognising pharmaceutical tablets and extracting information from prescription documents.',
    'about.para2':
      'The system is designed to serve as a practical, accessible tool for students, healthcare workers and the general public — providing fast, preliminary identification results while emphasising that findings should always be verified by a qualified medical professional.',
    'about.coreTitle': 'Core Capabilities',
    'about.coreSubtitle':
      'Three detection modules covering leaves, tablets and prescriptions.',
    'about.capabilities.leaf.title': 'Medicinal Leaf Detection',
    'about.capabilities.leaf.desc':
      'Identifies medicinal plant species from leaf images using trained deep-learning classification models.',
    'about.capabilities.tablet.title': 'Pharmaceutical Tablet Recognition',
    'about.capabilities.tablet.desc':
      'Recognises oral medication tablets based on visual features such as shape, colour and imprint patterns.',
    'about.capabilities.rx.title': 'Prescription Scanning',
    'about.capabilities.rx.desc':
      'Extracts readable medicine information from prescription documents using optical character recognition.',
    'about.capabilities.ai.title': 'AI-Assisted Identification',
    'about.capabilities.ai.desc':
      'Provides fast, preliminary identification results to assist users, while always recommending professional medical consultation.',
    'about.howItWorksTitle': 'How It Works',
    'about.howItWorksSubtitle': 'A high-level overview of the detection workflow.',
    'about.step1.title': '1. Upload',
    'about.step1.desc': 'Capture or select an image',
    'about.step2.title': '2. Analyse',
    'about.step2.desc': 'Preprocess and extract features',
    'about.step3.title': '3. Predict',
    'about.step3.desc': 'ML model classifies the image',
    'about.step4.title': '4. Display',
    'about.step4.desc': 'Results with confidence and details',
    'about.roadmapTitle': 'Future Integration Roadmap',
    'about.roadmapSubtitle':
      'Planned enhancements as the project matures toward a production-ready system.',
    'about.roadmap.ml.title': 'Trained ML Models',
    'about.roadmap.ml.desc':
      'Deploy custom convolutional neural networks trained on curated datasets of medicinal leaves and pharmaceutical tablets.',
    'about.roadmap.backend.title': 'FastAPI Backend',
    'about.roadmap.backend.desc':
      'Serve model predictions through a high-performance Python API built with FastAPI, enabling real-time inference.',
    'about.roadmap.eval.title': 'Model Evaluation',
    'about.roadmap.eval.desc':
      'Measure accuracy, precision, recall and F1 score across multiple classification categories to ensure reliable predictions.',
    'about.roadmap.improve.title': 'Continuous Improvement',
    'about.roadmap.improve.desc':
      'Retrain models with new data to improve accuracy and expand coverage of additional plant species and medications.',
    'about.disclaimerTitle': 'Important Disclaimer',
    'about.disclaimerDesc':
      'The current frontend application operates on mock data for demonstration purposes. It does not contain a working machine learning model or backend service. The ML classification pipeline, FastAPI server and trained model weights are planned for future integration and are not part of this release. All identification results shown are simulated and should not be used for medical diagnosis.',

    // HowItWorks page
    'hiw.eyebrow': 'Workflow',
    'hiw.title': 'How It Works',
    'hiw.subtitle':
      'A four-step overview of the MedScan AI detection pipeline — from image upload to detailed result.',
    'hiw.steps.upload.title': 'Upload Image',
    'hiw.steps.upload.desc':
      'Capture a photo using your device camera or upload an existing image of a medicinal leaf, pharmaceutical tablet, or prescription document.',
    'hiw.steps.analysis.title': 'Image Analysis',
    'hiw.steps.analysis.desc':
      'The uploaded image undergoes preprocessing — resizing, normalisation, and feature extraction — to prepare it for the machine learning model.',
    'hiw.steps.prediction.title': 'AI Prediction',
    'hiw.steps.prediction.desc':
      'A trained classification model analyses the preprocessed image and returns a prediction with a confidence score for the most likely match.',
    'hiw.steps.display.title': 'Information Display',
    'hiw.steps.display.desc':
      'Results are presented in a clear dashboard showing the identified name, confidence level, detailed properties, medicinal uses, precautions and storage information.',
    'hiw.cards.camera.title': 'Camera Capture',
    'hiw.cards.camera.desc':
      'Take a photo directly from your device camera for real-time detection.',
    'hiw.cards.ocr.title': 'Prescription OCR',
    'hiw.cards.ocr.desc':
      'Extract readable medicine information from prescription images using optical character recognition.',
    'hiw.cards.details.title': 'Rich Details',
    'hiw.cards.details.desc':
      'Access detailed profiles covering uses, active compounds, side effects, precautions and storage.',

    // Disclaimer
    'disclaimer':
      'This application provides AI-assisted identification for educational and informational purposes. It is not a substitute for professional medical advice.',

    // Footer
    'footer.desc':
      'A machine learning approach for detecting medicinal leaves and pharmaceutical tablets to support safe and informed healthcare.',
    'footer.explore': 'Explore',
    'footer.learnMore': 'Learn More',
    'footer.privacy': 'Privacy Policy',
    'footer.terms': 'Terms of Service',
    'footer.getInTouch': 'Get in Touch',
    'footer.address': 'University Campus, Faculty of Computing, Sri Lanka',
    'footer.allRights': 'MedScan AI. All rights reserved.',
    'footer.builtWithPrefix': 'Built with',
    'footer.and': 'and',
    'footer.builtWithSuffix': 'for better healthcare',

    // Detection pages
    'detect.uploadTitle': 'Upload Image',
    'detect.uploadHint': 'Drag & drop your image here, or browse files',
    'detect.uploadLabel': 'Upload an image',
    'detect.supportedFormats': 'Supported formats: JPG, JPEG, PNG',
    'detect.captureTitle': 'Capture with Camera',
    'detect.captureHint': 'Allow camera access to take a photo.',
    'detect.cameraPreview': 'Camera preview',
    'detect.analyze': 'Analyze',
    'detect.analyzing': 'Analyzing…',
    'detect.analyzeLeaf': 'Analyze Leaf',
    'detect.analyzeTablet': 'Analyze Tablet',
    'detect.analyzePrescription': 'Analyze Prescription',

    // Detection page headers
    'leafDetection.eyebrow': 'Leaf Detection',
    'leafDetection.title': 'Medicinal Leaf Detection',
    'leafDetection.subtitle':
      'Upload or capture an image of a medicinal leaf to identify the plant.',
    'tabletDetection.eyebrow': 'Tablet Detection',
    'tabletDetection.title': 'Pharmaceutical Tablet Recognition',
    'tabletDetection.subtitle':
      'Upload or capture an image of a pharmaceutical tablet to identify the medicine.',
    'rxScanner.eyebrow': 'Prescription Scanner',
    'rxScanner.title': 'Prescription Scanner',
    'rxScanner.subtitle':
      'Upload or capture a handwritten prescription image to extract the medicine information.',
    'rxScanner.uploadTitle': 'Upload Handwritten Prescription',
    'rxScanner.uploadLabel': 'Upload a handwritten prescription image',
    'rxScanner.uploadHint': 'Drag & drop the handwritten prescription here, or browse files',
    'rxScanner.changeImage': 'Change Image',
    'rxScanner.supportedFormats': 'Supported formats: JPG, JPEG, PNG, WEBP',
    'rxScanner.handwritten': 'Handwritten Prescription',
    'rxScanner.scanning': 'Scanning…',
    'rxScanner.scan': 'Scan Prescription',
    'rxScanner.process': 'Process Prescription',
    'rxScanner.processing': 'Processing Prescription…',
    'rxScanner.captureTitle': 'Capture Handwritten Prescription',
    'rxScanner.cameraHint':
      'Take a clear, well-lit photo of the handwritten prescription.',
    'rxScanner.overlayTitle': 'Reading Handwritten Prescription',
    'rxScanner.overlayDesc':
      'Simulating extraction of medicine details using demo data…',
    'rxScanner.resultEyebrow': 'Handwritten Prescription',
    'rxScanner.demoNotice':
      'Prescription information shown here is for demonstration purposes only. Handwritten prescriptions should be verified by a qualified healthcare professional before taking any medication.',
    'rxScanner.error':
      'Unable to scan the prescription. Please try again.',
    'rxScanner.genericError':
      'Something went wrong while scanning the prescription. Please try again.',

    // Camera
    'camera.starting': 'Starting camera…',
    'camera.requesting': 'Requesting camera permission…',
    'camera.opening': 'Opening camera…',
    'camera.ready': 'Live preview ready. Press again to capture the photo.',
    'camera.captured': 'Photo captured.',
    'camera.capture': 'Capture Photo',
    'camera.stop': 'Stop Camera',
    'camera.notReady':
      'The camera is not ready yet. Please wait for the preview to load before capturing.',
    'camera.captureFailed': 'Unable to capture the photo. Please try again.',
    'camera.streamError': 'The camera stream could not be displayed.',
    'camera.previewNotReady': 'The camera preview is not ready. Please try again.',
    'camera.notAllowed':
      'Camera access was denied. Please allow camera permission and try again.',
    'camera.notFound':
      'No camera was found on this device. Check that a camera is connected.',
    'camera.notReadable':
      'Your camera is currently in use by another application. Close it and try again.',
    'camera.security':
      'Camera access requires a secure (HTTPS) connection or localhost.',
    'camera.aborted': 'Opening the camera was aborted. Please try again.',
    'camera.generic':
      'Unable to access the camera. Check that it is connected and not in use.',
    'camera.unsupported':
      'Camera capture is not supported in this browser. You can still upload an image instead.',
    'camera.insecure':
      'Camera access requires a secure (HTTPS) connection or localhost. Serve the app over HTTPS or localhost to use the camera.',

    // Language
    'lang.en': 'English',
    'lang.kn': 'Kannada',
    'lang.hi': 'Hindi',
    'lang.ml': 'Malayalam',

    // Banner
    'banner.title':
      'Machine Learning Approach for Detecting the Medicinal Leaves & Pharmaceutical Tablets',
  },

  kn: {
    'nav.home': 'ಮನೆ',
    'nav.leaf': 'ಎಲೆ ಪತ್ತೆ',
    'nav.tablet': 'ಟ್ಯಾಬ್ಲೆಟ್ ಪತ್ತೆ',
    'nav.prescription': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್',
    'nav.history': 'ಇತಿಹಾಸ',
    'nav.howItWorks': 'ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ',
    'nav.about': 'ಕುರಿತು',
    'nav.signIn': 'ಸೈನ್ ಇನ್',
    'nav.signUp': 'ಸೈನ್ ಅಪ್',
    'nav.logOut': 'ಲಾಗ್ ಔಟ್',

    // Common
    'common.back': 'ಹಿಂದಕ್ಕೆ',

    'hero.badge': 'ಯಂತ್ರ ಕಲಿಕೆ · ಆರೋಗ್ಯ AI',
    'hero.title.line1': 'ಔಷಧೀಯ ಎಲೆಗಳು ಮತ್ತು ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್‌ಗಳನ್ನು ಪತ್ತೆಹಿಡಿಯಲು ಮೆಷಿನ್ ಲರ್ನಿಂಗ್ ವಿಧಾನ',
    'hero.title.line2': 'ಔಷಧೀಯ ಎಲೆಗಳು',
    'hero.title.amp': '&',
    'hero.title.line3': 'ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್‌ಗಳು',
    'hero.subtitle':
      'ಬುದ್ಧಿವಂತ ಚಿತ್ರ ವಿಶ್ಲೇಷಣೆಯ ಮೂಲಕ ಔಷಧೀಯ ಸಸ್ಯಗಳು, ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್‌ಗಳನ್ನು ಗುರುತಿಸಿ ಮತ್ತು ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ಗಳಿಂದ ಔಷಧ ಮಾಹಿತಿಯನ್ನು ಹೊರತೆಗೆಯಿರಿ.',
    'hero.ctaLeaf': 'ಔಷಧೀಯ ಎಲೆ ಗುರುತಿಸಿ',
    'hero.ctaTablet': 'ಟ್ಯಾಬ್ಲೆಟ್ ಗುರುತಿಸಿ',
    'hero.ctaPrescription': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ',
    'hero.visual.scanning': 'ಸ್ಕ್ಯಾನಿಂಗ್',
    'hero.visual.leafDetected': 'ಎಲೆ ಪತ್ತೆಯಾಗಿದೆ',
    'hero.visual.tabletMatched': 'ಟ್ಯಾಬ್ಲೆಟ್ ಹೊಂದಿಕೆಯಾಗಿದೆ',
    'hero.visual.rxExtracted': 'Rx ಹೊರತೆಗೆಯಲಾಗಿದೆ',
    'hero.visual.aiActive': 'AI ಮಾದರಿ ಸಕ್ರಿಯ',
    'hero.visual.tablet': 'ಟ್ಯಾಬ್ಲೆಟ್',
    'hero.visual.paracetamol': 'ಪಾರಾಸೆಟಮಾಲ್',
    'hero.visual.prescription': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್',
    'hero.visual.rx': 'Rx #0042',
    'hero.visual.confidence': 'ವಿಶ್ವಾಸಾರ್ಹತೆ 96.2%',

    'features.eyebrow': 'ವೈಶಿಷ್ಟ್ಯಗಳು',
    'features.title': 'ನಿತ್ಯ ಆರೋಗ್ಯಕ್ಕಾಗಿ ಸ್ಮಾರ್ಟ್ ಪತ್ತೆ',
    'features.subtitle':
      'ಚಿತ್ರಗಳನ್ನು ನಿಖರ, ಅರ್ಥವಾಗುವ ಔಷಧ ಮಾಹಿತಿಯಾಗಿ ಪರಿವರ್ತಿಸುವ ಮೂರು ಶಕ್ತಿಶಾಲಿ ಉಪಕರಣಗಳು.',
    'features.leaf.title': 'ಔಷಧೀಯ ಎಲೆ ಪತ್ತೆ',
    'features.leaf.desc':
      'ಯಾವುದೇ ಎಲೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ಮಾದರಿಯು ಕ್ಷಣಾರ್ಧದಲ್ಲಿ ಔಷಧೀಯ ಜಾತಿಗಳನ್ನು ಗುರುತಿಸುತ್ತದೆ, ಅವುಗಳ ಸಾಮಾನ್ಯ ಬಳಕೆಗಳು ಮತ್ತು ಗುಣಲಕ್ಷಣಗಳನ್ನು ಬಹಿರಂಗಪಡಿಸುತ್ತದೆ.',
    'features.leaf.cta': 'ಎಲೆ ಗುರುತಿಸಿ',
    'features.tablet.title': 'ಟ್ಯಾಬ್ಲೆಟ್ ಗುರುತಿಸುವಿಕೆ',
    'features.tablet.desc':
      'ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್ ಸೆರೆಹಿಡಿದು ಅದರ ಹೆಸರು, ಸಾಮಾನ್ಯ ಸಂಯೋಜನೆ, ಪ್ರಮಾಣ ಮತ್ತು ಬಳಕೆಯ ವಿವರಗಳನ್ನು ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಪಡೆಯಿರಿ.',
    'features.tablet.cta': 'ಟ್ಯಾಬ್ಲೆಟ್ ಗುರುತಿಸಿ',
    'features.rx.title': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಸ್ಕ್ಯಾನರ್',
    'features.rx.desc':
      'ಕೈಬರಹ ಅಥವಾ ಮುದ್ರಿತ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ಗಳನ್ನು ಸ್ಕ್ಯಾನ್ ಮಾಡಿ ಔಷಧ ಮಾಹಿತಿ ಮತ್ತು ಔಷಧ ಇತಿಹಾಸವನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಹೊರತೆಗೆಯಿರಿ.',
    'features.rx.cta': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ',

    'home.howItWorks.eyebrow': 'ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ',
    'home.howItWorks.title': 'ಚಿತ್ರದಿಂದ ಉತ್ತರಕ್ಕೆ ನಾಲ್ಕು ಹಂತಗಳು',
    'home.howItWorks.subtitle':
      'ತರಬೇತಿ ಪಡೆದ ಯಂತ್ರ ಕಲಿಕೆ ಮಾದರಿಯಿಂದ ಚಾಲಿತವಾದ ಸರಳ, ಪಾರದರ್ಶಕ ಪೈಪ್‌ಲೈನ್.',
    'home.steps.upload.title': 'ಚಿತ್ರ ಅಪ್‌ಲೋಡ್',
    'home.steps.upload.desc':
      'ನೀವು ಗುರುತಿಸಲು ಬಯಸುವ ಎಲೆ, ಟ್ಯಾಬ್ಲೆಟ್ ಅಥವಾ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ನ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿಯಿರಿ ಅಥವಾ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.',
    'home.steps.analysis.title': 'ಚಿತ್ರ ವಿಶ್ಲೇಷಣೆ',
    'home.steps.analysis.desc':
      'ನಮ್ಮ ಪೈಪ್‌ಲೈನ್ ಚಿತ್ರವನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸುತ್ತದೆ, ಶಬ್ದವನ್ನು ತೆಗೆದುಹಾಕುತ್ತದೆ ಮತ್ತು ಗುರುತಿಸುವ ಮಾದರಿಗೆ ಸಿದ್ಧಪಡಿಸುತ್ತದೆ.',
    'home.steps.prediction.title': 'AI ಮುನ್ಸೂಚನೆ',
    'home.steps.prediction.desc':
      'ತರಬೇತಿ ಪಡೆದ ಮಾದರಿಯು ಐಟಂ ಅನ್ನು ವರ್ಗೀಕರಿಸುತ್ತದೆ ಮತ್ತು ಮುನ್ಸೂಚನೆಗೆ ವಿಶ್ವಾಸಾರ್ಹತೆ ಸ್ಕೋರ್ ನೀಡುತ್ತದೆ.',
    'home.steps.display.title': 'ಮಾಹಿತಿ ಪ್ರದರ್ಶನ',
    'home.steps.display.desc':
      'ಔಷಧೀಯ ಹೆಸರು, ಗುಣಲಕ್ಷಣಗಳು, ಪ್ರಮಾಣ ಮಾರ್ಗದರ್ಶನ ಮತ್ತು ಉಲ್ಲೇಖಗಳನ್ನು ಸ್ಪಷ್ಟ ವರದಿಯಲ್ಲಿ ವೀಕ್ಷಿಸಿ.',

    'cta.title': 'ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಪತ್ತೆ ಮಾಡಲು ಪ್ರಾರಂಭಿಸಿ',
    'cta.subtitle':
      'ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ಮಾದರಿಯು ಔಷಧ ಏನು, ಅದು ಏನನ್ನು ಚಿಕಿತ್ಸೆ ಮಾಡುತ್ತದೆ ಮತ್ತು ಅದನ್ನು ಹೇಗೆ ಬಳಸಲಾಗುತ್ತದೆ ಎಂಬುದನ್ನು ಬಹಿರಂಗಪಡಿಸಲಿ.',
    'cta.button': 'ಈಗ ಪ್ರಯತ್ನಿಸಿ',

    'about.eyebrow': 'ಈ ಯೋಜನೆಯ ಕುರಿತು',
    'about.title': 'MedScan AI',
    'about.subtitle':
      'ಔಷಧೀಯ ಎಲೆಗಳು ಮತ್ತು ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್‌ಗಳನ್ನು ಪತ್ತೆಹಿಡಿಯುವ ಯಂತ್ರ ಕಲಿಕೆ ವಿಧಾನ',
    'about.projectTitle': 'ಅಂತಿಮ ವರ್ಷದ ಶೈಕ್ಷಣಿಕ ಯೋಜನೆ',
    'about.department': 'ಕಂಪ್ಯೂಟರ್ ವಿಜ್ಞಾನ ಮತ್ತು ಎಂಜಿನಿಯರಿಂಗ್ ವಿಭಾಗ',
    'about.para1':
      'MedScan AI ಔಷಧ ಮತ್ತು ಸಸ್ಯಶಾಸ್ತ್ರೀಯ ಗುರುತಿಸುವಿಕೆಯ ಕ್ಷೇತ್ರದಲ್ಲಿ ಯಂತ್ರ ಕಲಿಕೆಯ ಅನ್ವಯವನ್ನು ಅನ್ವೇಷಿಸುವ ಅಂತಿಮ ವರ್ಷದ ಪದವಿ ಯೋಜನೆಯಾಗಿದೆ.',
    'about.para2':
      'ಈ ವ್ಯವಸ್ಥೆಯು ವಿದ್ಯಾರ್ಥಿಗಳು, ಆರೋಗ್ಯ ಕಾರ್ಯಕರ್ತರು ಮತ್ತು ಸಾರ್ವಜನಿಕರಿಗಾಗಿ ಪ್ರಾಯೋಗಿಕ, ಪ್ರವೇಶಿಸಬಹುದಾದ ಸಾಧನವಾಗಿ ಕೆಲಸ ಮಾಡಲು ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ.',
    'about.coreTitle': 'ಮೂಲ ಸಾಮರ್ಥ್ಯಗಳು',
    'about.coreSubtitle':
      'ಎಲೆಗಳು, ಟ್ಯಾಬ್ಲೆಟ್‌ಗಳು ಮತ್ತು ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ಗಳನ್ನು ಒಳಗೊಂಡಿರುವ ಮೂರು ಪತ್ತೆ ಘಟಕಗಳು.',
    'about.capabilities.leaf.title': 'ಔಷಧೀಯ ಎಲೆ ಪತ್ತೆ',
    'about.capabilities.leaf.desc':
      'ತರಬೇತಿ ಪಡೆದ ಆಳವಾದ ಕಲಿಕೆ ವರ್ಗೀಕರಣ ಮಾದರಿಗಳನ್ನು ಬಳಸಿಕೊಂಡು ಎಲೆ ಚಿತ್ರಗಳಿಂದ ಔಷಧೀಯ ಸಸ್ಯ ಜಾತಿಗಳನ್ನು ಗುರುತಿಸುತ್ತದೆ.',
    'about.capabilities.tablet.title': 'ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್ ಗುರುತಿಸುವಿಕೆ',
    'about.capabilities.tablet.desc':
      'ಆಕಾರ, ಬಣ್ಣ ಮತ್ತು ಮುದ್ರಣ ಮಾದರಿಗಳಂತಹ ದೃಶ್ಯ ಲಕ್ಷಣಗಳ ಆಧಾರದ ಮೇಲೆ ಮೌಖಿಕ ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್‌ಗಳನ್ನು ಗುರುತಿಸುತ್ತದೆ.',
    'about.capabilities.rx.title': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಸ್ಕ್ಯಾನಿಂಗ್',
    'about.capabilities.rx.desc':
      'ಆಪ್ಟಿಕಲ್ ಕ್ಯಾರೆಕ್ಟರ್ ರೆಕಗ್ನಿಷನ್ ಬಳಸಿಕೊಂಡು ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಡಾಕ್ಯುಮೆಂಟ್‌ಗಳಿಂದ ಓದಬಹುದಾದ ಔಷಧ ಮಾಹಿತಿಯನ್ನು ಹೊರತೆಗೆಯುತ್ತದೆ.',
    'about.capabilities.ai.title': 'AI-ಸಹಾಯಕ ಗುರುತಿಸುವಿಕೆ',
    'about.capabilities.ai.desc':
      'ಬಳಕೆದಾರರಿಗೆ ಸಹಾಯ ಮಾಡಲು ವೇಗವಾದ, ಪ್ರಾಥಮಿಕ ಗುರುತಿಸುವಿಕೆ ಫಲಿತಾಂಶಗಳನ್ನು ಒದಗಿಸುತ್ತದೆ.',
    'about.howItWorksTitle': 'ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ',
    'about.howItWorksSubtitle': 'ಪತ್ತೆ ಕಾರ್ಯಪ್ರವಾಹದ ಉನ್ನತ-ಮಟ್ಟದ ಅವಲೋಕನ.',
    'about.step1.title': '1. ಅಪ್‌ಲೋಡ್',
    'about.step1.desc': 'ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿಯಿರಿ ಅಥವಾ ಆಯ್ಕೆಮಾಡಿ',
    'about.step2.title': '2. ವಿಶ್ಲೇಷಿಸಿ',
    'about.step2.desc': 'ಮುಂಚಿತ ಸಂಸ್ಕರಣೆ ಮತ್ತು ವೈಶಿಷ್ಟ್ಯಗಳನ್ನು ಹೊರತೆಗೆಯಿರಿ',
    'about.step3.title': '3. ಮುನ್ಸೂಚನೆ',
    'about.step3.desc': 'ML ಮಾದರಿಯು ಚಿತ್ರವನ್ನು ವರ್ಗೀಕರಿಸುತ್ತದೆ',
    'about.step4.title': '4. ಪ್ರದರ್ಶನ',
    'about.step4.desc': 'ವಿಶ್ವಾಸಾರ್ಹತೆ ಮತ್ತು ವಿವರಗಳೊಂದಿಗೆ ಫಲಿತಾಂಶಗಳು',
    'about.roadmapTitle': 'ಭವಿಷ್ಯದ ಏಕೀಕರಣ ರೋಡ್‌ಮ್ಯಾಪ್',
    'about.roadmapSubtitle':
      'ಉತ್ಪಾದನೆ-ಸಿದ್ಧ ವ್ಯವಸ್ಥೆಯತ್ತ ಯೋಜನೆಯು ಪಕ್ವವಾಗುತ್ತಿರುವಾಗ ಯೋಜಿಸಿದ ಸುಧಾರಣೆಗಳು.',
    'about.roadmap.ml.title': 'ತರಬೇತಿ ಪಡೆದ ML ಮಾದರಿಗಳು',
    'about.roadmap.ml.desc':
      'ಔಷಧೀಯ ಎಲೆಗಳು ಮತ್ತು ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್‌ಗಳ ಸಂಗ್ರಹಿತ ಡೇಟಾಸೆಟ್‌ಗಳಲ್ಲಿ ತರಬೇತಿ ಪಡೆದ ಕಸ್ಟಮ್ ಕನ್ವೊಲ್ಯೂಷನ್ ನ್ಯೂರಲ್ ನೆಟ್‌ವರ್ಕ್‌ಗಳನ್ನು ನಿಯೋಜಿಸಿ.',
    'about.roadmap.backend.title': 'FastAPI ಬ್ಯಾಕ್‌ಎಂಡ್',
    'about.roadmap.backend.desc':
      'FastAPI ನೊಂದಿಗೆ ನಿರ್ಮಿಸಲಾದ ಉನ್ನತ-ಕಾರ್ಯಕ್ಷಮತೆಯ Python API ಮೂಲಕ ಮಾದರಿ ಮುನ್ಸೂಚನೆಗಳನ್ನು ಸೇವಿಸಿ.',
    'about.roadmap.eval.title': 'ಮಾದರಿ ಮೌಲ್ಯಮಾಪನ',
    'about.roadmap.eval.desc':
      'ನಿಖರ ಮುನ್ಸೂಚನೆಗಳನ್ನು ಖಾತ್ರಿಪಡಿಸಲು ಬಹು ವರ್ಗೀಕರಣ ವರ್ಗಗಳಲ್ಲಿ ನಿಖರತೆ, ನಿಖರತೆ, ಮರುಪಡೆಯುವಿಕೆ ಮತ್ತು F1 ಸ್ಕೋರ್ ಅನ್ನು ಅಳತೆ ಮಾಡಿ.',
    'about.roadmap.improve.title': 'ನಿರಂತರ ಸುಧಾರಣೆ',
    'about.roadmap.improve.desc':
      'ಹೊಸ ಡೇಟಾದೊಂದಿಗೆ ಮಾದರಿಗಳನ್ನು ಮರುತರಬೇತಿ ನೀಡಿ ನಿಖರತೆಯನ್ನು ಸುಧಾರಿಸಿ.',
    'about.disclaimerTitle': 'ಮಹತ್ವದ ಅಸ್ವೀಕರಣ',
    'about.disclaimerDesc':
      'ಪ್ರಸ್ತುತ ಫ್ರಂಟ್‌ಎಂಡ್ ಅಪ್ಲಿಕೇಶನ್ ಪ್ರದರ್ಶನ ಉದ್ದೇಶಗಳಿಗಾಗಿ ಮಾಕ್ ಡೇಟಾದಲ್ಲಿ ಕೆಲಸ ಮಾಡುತ್ತದೆ.',

    'hiw.eyebrow': 'ಕಾರ್ಯಪ್ರವಾಹ',
    'hiw.title': 'ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ',
    'hiw.subtitle':
      'MedScan AI ಪತ್ತೆ ಪೈಪ್‌ಲೈನ್‌ನ ನಾಲ್ಕು ಹಂತಗಳ ಅವಲೋಕನ — ಚಿತ್ರ ಅಪ್‌ಲೋಡ್‌ನಿಂದ ವಿವರವಾದ ಫಲಿತಾಂಶದವರೆಗೆ.',
    'hiw.steps.upload.title': 'ಚಿತ್ರ ಅಪ್‌ಲೋಡ್',
    'hiw.steps.upload.desc':
      'ನಿಮ್ಮ ಸಾಧನ ಕ್ಯಾಮೆರಾ ಬಳಸಿ ಫೋಟೋ ಸೆರೆಹಿಡಿಯಿರಿ ಅಥವಾ ಔಷಧೀಯ ಎಲೆ, ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್, ಅಥವಾ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಡಾಕ್ಯುಮೆಂಟ್‌ನ ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.',
    'hiw.steps.analysis.title': 'ಚಿತ್ರ ವಿಶ್ಲೇಷಣೆ',
    'hiw.steps.analysis.desc':
      'ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರವು ಮುಂಚಿತ ಸಂಸ್ಕರಣೆಗೆ ಒಳಗಾಗುತ್ತದೆ — ಗಾತ್ರ ಬದಲಾಯಿಸುವಿಕೆ, ನಾರ್ಮಲೈಸೇಶನ್, ಮತ್ತು ವೈಶಿಷ್ಟ್ಯ ಹೊರತೆಗೆಯುವಿಕೆ.',
    'hiw.steps.prediction.title': 'AI ಮುನ್ಸೂಚನೆ',
    'hiw.steps.prediction.desc':
      'ತರಬೇತಿ ಪಡೆದ ವರ್ಗೀಕರಣ ಮಾದರಿಯು ಮುಂಚಿತ ಸಂಸ್ಕರಿತ ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ.',
    'hiw.steps.display.title': 'ಮಾಹಿತಿ ಪ್ರದರ್ಶನ',
    'hiw.steps.display.desc':
      'ಫಲಿತಾಂಶಗಳನ್ನು ಸ್ಪಷ್ಟ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ ಪ್ರಸ್ತುತಪಡಿಸಲಾಗಿದೆ.',
    'hiw.cards.camera.title': 'ಕ್ಯಾಮೆರಾ ಸೆರೆಹಿಡಿಯುವಿಕೆ',
    'hiw.cards.camera.desc':
      'ರಿಯಲ್-ಟೈಮ್ ಪತ್ತೆಗಾಗಿ ನಿಮ್ಮ ಸಾಧನ ಕ್ಯಾಮೆರಾದಿಂದ ನೇರವಾಗಿ ಫೋಟೋ ತೆಗೆಯಿರಿ.',
    'hiw.cards.ocr.title': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ OCR',
    'hiw.cards.ocr.desc':
      'ಆಪ್ಟಿಕಲ್ ಕ್ಯಾರೆಕ್ಟರ್ ರೆಕಗ್ನಿಷನ್ ಬಳಸಿಕೊಂಡು ಓದಬಹುದಾದ ಔಷಧ ಮಾಹಿತಿಯನ್ನು ಹೊರತೆಗೆಯಿರಿ.',
    'hiw.cards.details.title': 'ಸಮೃದ್ಧ ವಿವರಗಳು',
    'hiw.cards.details.desc':
      'ಬಳಕೆಗಳು, ಸಕ್ರಿಯ ಸಂಯುಕ್ತಗಳು, ಅಡ್ಡ ಪರಿಣಾಮಗಳು, ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು ಮತ್ತು ಸಂಗ್ರಹಣೆಯನ್ನು ಒಳಗೊಂಡಿರುವ ವಿವರವಾದ ಪ್ರೊಫೈಲ್‌ಗಳನ್ನು ಪ್ರವೇಶಿಸಿ.',

    'disclaimer':
      'ಈ ಅಪ್ಲಿಕೇಶನ್ ಶೈಕ್ಷಣಿಕ ಮತ್ತು ಮಾಹಿತಿ ಉದ್ದೇಶಗಳಿಗಾಗಿ AI-ಸಹಾಯಕ ಗುರುತಿಸುವಿಕೆಯನ್ನು ಒದಗಿಸುತ್ತದೆ. ಇದು ವೃತ್ತಿಪರ ವೈದ್ಯಕೀಯ ಸಲಹೆಯ ಪರ್ಯಾಯವಲ್ಲ.',

    'footer.desc':
      'ಸುರಕ್ಷಿತ ಮತ್ತು ಅರಿವುಳ್ಳ ಆರೋಗ್ಯ ಸೇವೆಯನ್ನು ಬೆಂಬಲಿಸಲು ಔಷಧೀಯ ಎಲೆಗಳು ಮತ್ತು ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್‌ಗಳನ್ನು ಪತ್ತೆಹಿಡಿಯುವ ಯಂತ್ರ ಕಲಿಕೆ ವಿಧಾನ.',
    'footer.explore': 'ಅನ್ವೇಷಿಸಿ',
    'footer.learnMore': 'ಇನ್ನಷ್ಟು ಕಲಿಯಿರಿ',
    'footer.privacy': 'ಗೌಪ್ಯತಾ ನೀತಿ',
    'footer.terms': 'ಸೇವಾ ನಿಯಮಗಳು',
    'footer.getInTouch': 'ಸಂಪರ್ಕಿಸಿ',
    'footer.address': 'ವಿಶ್ವವಿದ್ಯಾಲಯ ಕ್ಯಾಂಪಸ್, ಕಂಪ್ಯೂಟಿಂಗ್ ಘಟಕ, ಶ್ರೀಲಂಕಾ',
    'footer.allRights': 'MedScan AI. ಎಲ್ಲ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ.',
    'footer.builtWithPrefix': 'ಇದರೊಂದಿಗೆ ನಿರ್ಮಿಸಲಾಗಿದೆ',
    'footer.and': 'ಮತ್ತು',
    'footer.builtWithSuffix': 'ಉತ್ತಮ ಆರೋಗ್ಯಕ್ಕಾಗಿ',

    'detect.uploadTitle': 'ಚಿತ್ರ ಅಪ್‌ಲೋಡ್',
    'detect.uploadHint': 'ನಿಮ್ಮ ಚಿತ್ರವನ್ನು ಇಲ್ಲಿ ಎಳೆದು ಬಿಡಿ ಅಥವಾ ಫೈಲ್‌ಗಳನ್ನು ಬ್ರೌಸ್ ಮಾಡಿ',
    'detect.uploadLabel': 'ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
    'detect.supportedFormats': 'ಬೆಂಬಲಿತ ಸ್ವರೂಪಗಳು: JPG, JPEG, PNG',
    'detect.captureTitle': 'ಕ್ಯಾಮೆರಾದೊಂದಿಗೆ ಸೆರೆಹಿಡಿಯಿರಿ',
    'detect.captureHint': 'ಫೋಟೋ ತೆಗೆಯಲು ಕ್ಯಾಮೆರಾ ಪ್ರವೇಶವನ್ನು ಅನುಮತಿಸಿ.',
    'detect.cameraPreview': 'ಕ್ಯಾಮೆರಾ ಮುನ್ನೋಟ',
    'detect.analyze': 'ವಿಶ್ಲೇಷಿಸಿ',
    'detect.analyzing': 'ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ…',
    'detect.analyzeLeaf': 'ಎಲೆ ವಿಶ್ಲೇಷಿಸಿ',
    'detect.analyzeTablet': 'ಟ್ಯಾಬ್ಲೆಟ್ ವಿಶ್ಲೇಷಿಸಿ',
    'detect.analyzePrescription': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ವಿಶ್ಲೇಷಿಸಿ',

    'leafDetection.eyebrow': 'ಎಲೆ ಪತ್ತೆ',
    'leafDetection.title': 'ಔಷಧೀಯ ಎಲೆ ಪತ್ತೆ',
    'leafDetection.subtitle':
      'ಸಸ್ಯವನ್ನು ಗುರುತಿಸಲು ಔಷಧೀಯ ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಸೆರೆಹಿಡಿಯಿರಿ.',
    'tabletDetection.eyebrow': 'ಟ್ಯಾಬ್ಲೆಟ್ ಪತ್ತೆ',
    'tabletDetection.title': 'ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್ ಗುರುತಿಸುವಿಕೆ',
    'tabletDetection.subtitle':
      'ಔಷಧವನ್ನು ಗುರುತಿಸಲು ಔಷಧ ಟ್ಯಾಬ್ಲೆಟ್‌ನ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಸೆರೆಹಿಡಿಯಿರಿ.',
    'rxScanner.eyebrow': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಸ್ಕ್ಯಾನರ್',
    'rxScanner.title': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಸ್ಕ್ಯಾನರ್',
    'rxScanner.subtitle':
      'ಓದಬಹುದಾದ ಔಷಧ ಮಾಹಿತಿಯನ್ನು ಹೊರತೆಗೆಯಲು ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.',
    'rxScanner.uploadTitle': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಅಪ್‌ಲೋಡ್',
    'rxScanner.uploadLabel': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
    'rxScanner.uploadHint': 'ನಿಮ್ಮ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ನ್ ಇಲ್ಲಿ ಎಳೆದು ಬಿಡಿ ಅಥವಾ ಫೈಲ್‌ಗಳನ್ನು ಬ್ರೌಸ್ ಮಾಡಿ',
    'rxScanner.changeImage': 'ಚಿತ್ರ ಬದಲಾಯಿಸಿ',
    'rxScanner.supportedFormats': 'ಬೆಂಬಲಿತ ಸ್ವರೂಪಗಳು: JPG, JPEG, PNG, WEBP',
    'rxScanner.handwritten': 'ಕೈಬರಹದ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್',
    'rxScanner.overlayTitle': 'ಕೈಬರಹದ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಓದಲಾಗುತ್ತಿದೆ',
    'rxScanner.overlayDesc':
      'ಡೆಮೊ ಡೇಟಾ ಬಳಸಿ ಔಷಧ ವಿವರಗಳ ಹೊರತೆಗೆಯುವಿಕೆಯನ್ನು ಅನುಕರಿಸಲಾಗುತ್ತಿದೆ…',
    'rxScanner.scanning': 'ಸ್ಕ್ಯಾನ್ ಆಗುತ್ತಿದೆ…',
    'rxScanner.scan': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ',
    'rxScanner.ocrTitle': 'OCR ಸ್ಕ್ಯಾನಿಂಗ್',
    'rxScanner.ocrDesc': 'ಓದಬಹುದಾದ ಔಷಧ ಮಾಹಿತಿಯನ್ನು ಹೊರತೆಗೆಯಲಾಗುತ್ತಿದೆ…',
    'rxScanner.error': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಸ್ಕ್ಯಾನ್ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
    'rxScanner.genericError': 'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಸ್ಕ್ಯಾನ್ ಮಾಡುವಾಗ ಏನೋ ತಪ್ಪಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',

    'camera.starting': 'ಕ್ಯಾಮೆರಾ ಪ್ರಾರಂಭವಾಗುತ್ತಿದೆ…',
    'camera.requesting': 'ಕ್ಯಾಮೆರಾ ಅನುಮತಿ ಕೇಳಲಾಗುತ್ತಿದೆ…',
    'camera.opening': 'ಕ್ಯಾಮೆರಾ ತೆರೆಯಲಾಗುತ್ತಿದೆ…',
    'camera.ready': 'ಲೈವ್ ಮುನ್ನೋಟ ಸಿದ್ಧವಾಗಿದೆ. ಫೋಟೋ ಸೆರೆಹಿಡಿಯಲು ಮತ್ತೆ ಒತ್ತಿರಿ.',
    'camera.captured': 'ಫೋಟೋ ಸೆರೆಹಿಡಿಯಲಾಗಿದೆ.',
    'camera.capture': 'ಫೋಟೋ ಸೆರೆಹಿಡಿಯಿರಿ',
    'camera.stop': 'ಕ್ಯಾಮೆರಾ ನಿಲ್ಲಿಸಿ',
    'camera.notReady': 'ಕ್ಯಾಮೆರಾ ಇನ್ನೂ ಸಿದ್ಧವಾಗಿಲ್ಲ. ಸೆರೆಹಿಡಿಯುವ ಮೊದಲು ಮುನ್ನೋಟ ಲೋಡ್ ಆಗಲು ಕಾಯಿರಿ.',
    'camera.captureFailed': 'ಫೋಟೋ ಸೆರೆಹಿಡಿಯಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
    'camera.streamError': 'ಕ್ಯಾಮೆರಾ ಸ್ಟ್ರೀಮ್ ಅನ್ನು ಪ್ರದರ್ಶಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.',
    'camera.previewNotReady': 'ಕ್ಯಾಮೆರಾ ಮುನ್ನೋಟ ಸಿದ್ಧವಾಗಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
    'camera.notAllowed': 'ಕ್ಯಾಮೆರಾ ಪ್ರವೇಶ ನಿರಾಕರಿಸಲಾಗಿದೆ. ದಯವಿಟ್ಟು ಕ್ಯಾಮೆರಾ ಅನುಮತಿ ನೀಡಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
    'camera.notFound': 'ಈ ಸಾಧನದಲ್ಲಿ ಕ್ಯಾಮೆರಾ ಕಂಡುಬಂದಿಲ್ಲ. ಕ್ಯಾಮೆರಾ ಸಂಪರ್ಕಗೊಂಡಿದೆ ಎಂದು ಪರಿಶೀಲಿಸಿ.',
    'camera.notReadable': 'ನಿಮ್ಮ ಕ್ಯಾಮೆರಾವನ್ನು ಮತ್ತೊಂದು ಅಪ್ಲಿಕೇಶನ್ ಬಳಸುತ್ತಿರಬಹುದು. ಅದನ್ನು ಮುಚ್ಚಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
    'camera.security': 'ಕ್ಯಾಮೆರಾ ಪ್ರವೇಶಕ್ಕೆ ಸುರಕ್ಷಿತ (HTTPS) ಸಂಪರ್ಕ ಅಥವಾ localhost ಅಗತ್ಯವಿದೆ.',
    'camera.aborted': 'ಕ್ಯಾಮೆರಾ ತೆರೆಯುವಿಕೆ ರದ್ದಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
    'camera.generic': 'ಕ್ಯಾಮೆರಾವನ್ನು ಪ್ರವೇಶಿಸಲು ಸಾಧ್ಯವಾಗಿಲ್ಲ. ಅದು ಸಂಪರ್ಕಗೊಂಡಿದೆ ಮತ್ತು ಬಳಕೆಯಲ್ಲಿಲ್ಲ ಎಂದು ಪರಿಶೀಲಿಸಿ.',
    'camera.unsupported': 'ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಕ್ಯಾಮೆರಾ ಸೆರೆಹಿಡಿಯುವಿಕೆ ಬೆಂಬಲಿತವಾಗಿಲ್ಲ. ನೀವು ಇನ್ನೂ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಬಹುದು.',
    'camera.insecure': 'ಕ್ಯಾಮೆರಾ ಪ್ರವೇಶಕ್ಕೆ ಸುರಕ್ಷಿತ (HTTPS) ಸಂಪರ್ಕ ಅಥವಾ localhost ಅಗತ್ಯವಿದೆ.',

    'lang.en': 'English',
    'lang.kn': 'Kannada',
    'lang.hi': 'Hindi',
    'lang.ml': 'Malayalam',
  },

  hi: {
    'nav.home': 'होम',
    'nav.leaf': 'पत्ता पहचान',
    'nav.tablet': 'टैबलेट पहचान',
    'nav.prescription': 'प्रिस्क्रिप्शन',
    'nav.history': 'इतिहास',
    'nav.howItWorks': 'यह कैसे काम करता है',
    'nav.about': 'के बारे में',
    'nav.signIn': 'साइन इन',
    'nav.signUp': 'साइन अप',
    'nav.logOut': 'लॉग आउट',

    // Common
    'common.back': 'पीछे',

    'hero.badge': 'मशीन लर्निंग · हेल्थकेयर AI',
    'hero.title.line1': 'औषधीय पत्तियों और फार्मास्युटिकल टैबलेट का पता लगाने के लिए मशीन लर्निंग विधि',
    'hero.title.line2': 'औषधीय पत्तियां',
    'hero.title.amp': '&',
    'hero.title.line3': 'फार्मास्युटिकल टैबलेट',
    'hero.subtitle':
      'बुद्धिमान छवि विश्लेषण का उपयोग करके औषधीय पौधों, फार्मास्यूटिकल टैबलेट की पहचान करें और प्रिस्क्रिप्शन से दवा की जानकारी निकालें।',
    'hero.ctaLeaf': 'औषधीय पत्ता पहचानें',
    'hero.ctaTablet': 'टैबलेट पहचानें',
    'hero.ctaPrescription': 'प्रिस्क्रिप्शन स्कैन करें',
    'hero.visual.scanning': 'स्कैनिंग',
    'hero.visual.leafDetected': 'पत्ता पहचाना गया',
    'hero.visual.tabletMatched': 'टैबलेट मैच हुआ',
    'hero.visual.rxExtracted': 'Rx निकाला गया',
    'hero.visual.aiActive': 'AI मॉडल सक्रिय',
    'hero.visual.tablet': 'टैबलेट',
    'hero.visual.paracetamol': 'पैरासिटामोल',
    'hero.visual.prescription': 'प्रिस्क्रिप्शन',
    'hero.visual.rx': 'Rx #0042',
    'hero.visual.confidence': 'विश्वास 96.2%',

    'features.eyebrow': 'विशेषताएँ',
    'features.title': 'रोज़मर्रा की स्वास्थ्य सेवा के लिए स्मार्ट पहचान',
    'features.subtitle':
      'तीन शक्तिशाली उपकरण जो छवियों को सटीक, समझने योग्य दवा जानकारी में बदलते हैं।',
    'features.leaf.title': 'औषधीय पत्ता पहचान',
    'features.leaf.desc':
      'किसी भी पत्ते की फोटो अपलोड करें और मॉडल तुरंत औषधीय प्रजातियों को पहचानता है।',
    'features.leaf.cta': 'पत्ता पहचानें',
    'features.tablet.title': 'टैबलेट पहचान',
    'features.tablet.desc':
      'फार्मास्यूटिकल टैबलेट को स्नैप करें और सेकंडों में इसका नाम, संरचना, खुराक और उपयोग विवरण प्राप्त करें।',
    'features.tablet.cta': 'टैबलेट पहचानें',
    'features.rx.title': 'प्रिस्क्रिप्शन स्कैनर',
    'features.rx.desc':
      'हस्तलिखित या मुद्रित प्रिस्क्रिप्शन को स्कैन करें और दवा की जानकारी स्वचालित रूप से निकालें।',
    'features.rx.cta': 'प्रिस्क्रिप्शन स्कैन करें',

    'home.howItWorks.eyebrow': 'यह कैसे काम करता है',
    'home.howItWorks.title': 'छवि से उत्तर तक चार चरण',
    'home.howItWorks.subtitle':
      'एक प्रशिक्षित मशीन लर्निंग मॉडल द्वारा संचालित एक सरल, पारदर्शी पाइपलाइन।',
    'home.steps.upload.title': 'छवि अपलोड करें',
    'home.steps.upload.desc':
      'पत्ता, टैबलेट या प्रिस्क्रिप्शन की स्पष्ट छवि कैप्चर या अपलोड करें।',
    'home.steps.analysis.title': 'छवि विश्लेषण',
    'home.steps.analysis.desc':
      'हमारी पाइपलाइन छवि को साफ करती है, शोर हटाती है और मॉडल के लिए तैयार करती है।',
    'home.steps.prediction.title': 'AI भविष्यवाणी',
    'home.steps.prediction.desc':
      'प्रशिक्षित मॉडल आइटम को वर्गीकृत करता है और भविष्यवाणी को विश्वास स्कोर देता है।',
    'home.steps.display.title': 'जानकारी प्रदर्शन',
    'home.steps.display.desc':
      'औषधीय नाम, गुण, खुराक मार्गदर्शन और संदर्भों को स्पष्ट रिपोर्ट में देखें।',

    'cta.title': 'सेकंडों में पहचान शुरू करें',
    'cta.subtitle':
      'छवि अपलोड करें और मॉडल को बताएं कि दवा क्या है, यह क्या इलाज करती है, और इसका उपयोग कैसे किया जाता है।',
    'cta.button': 'अभी आज़माएं',

    'about.eyebrow': 'इस प्रोजेक्ट के बारे में',
    'about.title': 'MedScan AI',
    'about.subtitle':
      'औषधीय पत्तों और फार्मास्यूटिकल टैबलेट का पता लगाने के लिए मशीन लर्निंग दृष्टिकोण',
    'about.projectTitle': 'अंतिम वर्ष का शैक्षणिक प्रोजेक्ट',
    'about.department': 'कंप्यूटर विज्ञान और इंजीनियरिंग विभाग',
    'about.para1':
      'MedScan AI एक अंतिम वर्ष की परियोजना है जो फार्मास्यूटिकल और वनस्पति पहचान के क्षेत्र में मशीन लर्निंग के अनुप्रयोग का पता लगाती है।',
    'about.para2':
      'यह प्रणाली छात्रों, स्वास्थ्यकर्मियों और आम जनता के लिए एक व्यावहारिक, सुलभ उपकरण के रूप में काम करने के लिए डिज़ाइन की गई है।',
    'about.coreTitle': 'मूल क्षमताएं',
    'about.coreSubtitle':
      'पत्तों, टैबलेट और प्रिस्क्रिप्शन को कवर करने वाले तीन पहचान मॉड्यूल।',
    'about.capabilities.leaf.title': 'औषधीय पत्ता पहचान',
    'about.capabilities.leaf.desc':
      'प्रशिक्षित डीप-लर्निंग वर्गीकरण मॉडल का उपयोग करके पत्ता छवियों से औषधीय पौधों की प्रजातियों की पहचान करता है।',
    'about.capabilities.tablet.title': 'फार्मास्यूटिकल टैबलेट पहचान',
    'about.capabilities.tablet.desc':
      'आकार, रंग और छपाई पैटर्न जैसी दृश्य विशेषताओं के आधार पर ओरल मेडिकेशन टैबलेट को पहचानता है।',
    'about.capabilities.rx.title': 'प्रिस्क्रिप्शन स्कैनिंग',
    'about.capabilities.rx.desc':
      'ऑप्टिकल कैरेक्टर रिकग्निशन का उपयोग करके प्रिस्क्रिप्शन दस्तावेजों से पठनीय दवा जानकारी निकालता है।',
    'about.capabilities.ai.title': 'AI-सहायता प्राप्त पहचान',
    'about.capabilities.ai.desc':
      'उपयोगकर्ताओं की सहायता के लिए तेज़, प्रारंभिक पहचान परिणाम प्रदान करता है।',
    'about.howItWorksTitle': 'यह कैसे काम करता है',
    'about.howItWorksSubtitle': 'पहचान कार्यप्रवाह का उच्च-स्तरीय अवलोकन।',
    'about.step1.title': '1. अपलोड',
    'about.step1.desc': 'छवि कैप्चर या चुनें',
    'about.step2.title': '2. विश्लेषण',
    'about.step2.desc': 'प्रीप्रोसेस और विशेषताएं निकालें',
    'about.step3.title': '3. भविष्यवाणी',
    'about.step3.desc': 'ML मॉडल छवि को वर्गीकृत करता है',
    'about.step4.title': '4. प्रदर्शन',
    'about.step4.desc': 'विश्वास और विवरण के साथ परिणाम',
    'about.roadmapTitle': 'भविष्य एकीकरण रोडमैप',
    'about.roadmapSubtitle':
      'प्रोडक्शन-रेडी सिस्टम की ओर परियोजना परिपक्व होने पर नियोजित संवर्द्धन।',
    'about.roadmap.ml.title': 'प्रशिक्षित ML मॉडल',
    'about.roadmap.ml.desc':
      'औषधीय पत्तों और फार्मास्यूटिकल टैबलेट के डेटासेट पर प्रशिक्षित कस्टम कन्वोल्यूशनल न्यूरल नेटवर्क तैनात करें।',
    'about.roadmap.backend.title': 'FastAPI बैकएंड',
    'about.roadmap.backend.desc':
      'FastAPI के साथ बनाए गए उच्च-प्रदर्शन Python API के माध्यम से मॉडल भविष्यवाणियां प्रदान करें।',
    'about.roadmap.eval.title': 'मॉडल मूल्यांकन',
    'about.roadmap.eval.desc':
      'विश्वसनीय भविष्यवाणियों को सुनिश्चित करने के लिए सटीकता, परिशुद्धता, रिकॉल और F1 स्कोर मापें।',
    'about.roadmap.improve.title': 'निरंतर सुधार',
    'about.roadmap.improve.desc':
      'नए डेटा के साथ मॉडल को फिर से प्रशिक्षित करके सटीकता में सुधार करें।',
    'about.disclaimerTitle': 'महत्वपूर्ण अस्वीकरण',
    'about.disclaimerDesc':
      'वर्तमान फ्रंटएंड एप्लिकेशन प्रदर्शन उद्देश्यों के लिए मॉक डेटा पर काम करता है।',

    'hiw.eyebrow': 'कार्यप्रवाह',
    'hiw.title': 'यह कैसे काम करता है',
    'hiw.subtitle':
      'MedScan AI पहचान पाइपलाइन का चार चरणों का अवलोकन — छवि अपलोड से विस्तृत परिणाम तक।',
    'hiw.steps.upload.title': 'छवि अपलोड करें',
    'hiw.steps.upload.desc':
      'अपने डिवाइस कैमरे का उपयोग करके फोटो कैप्चर करें या औषधीय पत्ता, टैबलेट, या प्रिस्क्रिप्शन दस्तावेज़ की छवि अपलोड करें।',
    'hiw.steps.analysis.title': 'छवि विश्लेषण',
    'hiw.steps.analysis.desc':
      'अपलोड की गई छवि प्रीप्रोसेसिंग से गुजरती है — आकार बदलना, सामान्यीकरण, और विशेषता निकालना।',
    'hiw.steps.prediction.title': 'AI भविष्यवाणी',
    'hiw.steps.prediction.desc':
      'एक प्रशिक्षित वर्गीकरण मॉडल प्रीप्रोसेस की गई छवि का विश्लेषण करता है।',
    'hiw.steps.display.title': 'जानकारी प्रदर्शन',
    'hiw.steps.display.desc':
      'परिणाम एक स्पष्ट डैशबोर्ड में प्रस्तुत किए जाते हैं।',
    'hiw.cards.camera.title': 'कैमरा कैप्चर',
    'hiw.cards.camera.desc':
      'रीयल-टाइम पहचान के लिए अपने डिवाइस कैमरे से सीधे फोटो लें।',
    'hiw.cards.ocr.title': 'प्रिस्क्रिप्शन OCR',
    'hiw.cards.ocr.desc':
      'ऑप्टिकल कैरेक्टर रिकग्निशन का उपयोग करके पठनीय दवा जानकारी निकालें।',
    'hiw.cards.details.title': 'विस्तृत विवरण',
    'hiw.cards.details.desc':
      'उपयोग, सक्रिय यौगिकों, साइड इफेक्ट्स, सावधानियों और भंडारण को कवर करने वाली विस्तृत प्रोफाइल तक पहुंचें।',

    'disclaimer':
      'यह अनुप्रयोग शैक्षणिक और सूचनात्मक उद्देश्यों के लिए AI-सहायता प्राप्त पहचान प्रदान करता है। यह पेशेवर चिकित्सा सलाह का विकल्प नहीं है।',

    'footer.desc':
      'सुरक्षित और सूचित स्वास्थ्य सेवा का समर्थन करने के लिए औषधीय पत्तों और फार्मास्यूटिकल टैबलेट का पता लगाने के लिए मशीन लर्निंग दृष्टिकोण।',
    'footer.explore': 'अन्वेषण',
    'footer.learnMore': 'और जानें',
    'footer.privacy': 'गोपनीयता नीति',
    'footer.terms': 'सेवा की शर्तें',
    'footer.getInTouch': 'संपर्क में रहें',
    'footer.address': 'विश्वविद्यालय परिसर, कंप्यूटिंग संकाय, श्रीलंका',
    'footer.allRights': 'MedScan AI. सर्वाधिकार सुरक्षित।',
    'footer.builtWithPrefix': 'इसके साथ निर्मित',
    'footer.and': 'और',
    'footer.builtWithSuffix': 'बेहतर स्वास्थ्य के लिए',

    'detect.uploadTitle': 'छवि अपलोड करें',
    'detect.uploadHint': 'अपनी छवि यहां खींचें या फ़ाइलें ब्राउज़ करें',
    'detect.uploadLabel': 'छवि अपलोड करें',
    'detect.supportedFormats': 'समर्थित प्रारूप: JPG, JPEG, PNG',
    'detect.captureTitle': 'कैमरा से कैप्चर करें',
    'detect.captureHint': 'फ़ोटो लेने के लिए कैमरा अनुमति दें।',
    'detect.cameraPreview': 'कैमरा पूर्वावलोकन',
    'detect.analyze': 'विश्लेषण',
    'detect.analyzing': 'विश्लेषण हो रहा है…',
    'detect.analyzeLeaf': 'पत्ता विश्लेषण',
    'detect.analyzeTablet': 'टैबलेट विश्लेषण',
    'detect.analyzePrescription': 'प्रिस्क्रिप्शन विश्लेषण',

    'leafDetection.eyebrow': 'पत्ता पहचान',
    'leafDetection.title': 'औषधीय पत्ता पहचान',
    'leafDetection.subtitle':
      'पौधे की पहचान करने के लिए औषधीय पत्ते की छवि अपलोड करें या कैप्चर करें।',
    'tabletDetection.eyebrow': 'टैबलेट पहचान',
    'tabletDetection.title': 'फार्मास्यूटिकल टैबलेट पहचान',
    'tabletDetection.subtitle':
      'दवा की पहचान करने के लिए फार्मास्यूटिकल टैबलेट की छवि अपलोड करें या कैप्चर करें।',
    'rxScanner.eyebrow': 'प्रिस्क्रिप्शन स्कैनर',
    'rxScanner.title': 'प्रिस्क्रिप्शन स्कैनर',
    'rxScanner.subtitle':
      'पठनीय दवा जानकारी निकालने के लिए प्रिस्क्रिप्शन छवि अपलोड करें।',
    'rxScanner.uploadTitle': 'प्रिस्क्रिप्शन अपलोड करें',
    'rxScanner.uploadLabel': 'प्रिस्क्रिप्शन छवि अपलोड करें',
    'rxScanner.uploadHint': 'अपना प्रिस्क्रिप्शन यहां खींचें या फ़ाइलें ब्राउज़ करें',
    'rxScanner.changeImage': 'छवि बदलें',
    'rxScanner.supportedFormats': 'समर्थित प्रारूप: JPG, JPEG, PNG, WEBP',
    'rxScanner.handwritten': 'हस्तलिखित प्रिस्क्रिप्शन',
    'rxScanner.overlayTitle': 'हस्तलिखित प्रिस्क्रिप्शन पढ़ा जा रहा है',
    'rxScanner.overlayDesc':
      'डेमो डेटा का उपयोग करके दवा विवरण निकालने का अनुकरण किया जा रहा है…',
    'rxScanner.scanning': 'स्कैन हो रहा है…',
    'rxScanner.scan': 'प्रिस्क्रिप्शन स्कैन करें',
    'rxScanner.ocrTitle': 'OCR स्कैनिंग',
    'rxScanner.ocrDesc': 'पठनीय दवा जानकारी निकाली जा रही है…',
    'rxScanner.error': 'प्रिस्क्रिप्शन स्कैन करने में असमर्थ। कृपया पुनः प्रयास करें।',
    'rxScanner.genericError': 'प्रिस्क्रिप्शन स्कैन करते समय कुछ गलत हो गया। कृपया पुनः प्रयास करें।',

    'camera.starting': 'कैमरा शुरू हो रहा है…',
    'camera.requesting': 'कैमरा अनुमति मांगी जा रही है…',
    'camera.opening': 'कैमरा खोला जा रहा है…',
    'camera.ready': 'लाइव पूर्वावलोकन तैयार है। फोटो लेने के लिए फिर से दबाएं।',
    'camera.captured': 'फोटो कैप्चर हो गया।',
    'camera.capture': 'फोटो कैप्चर करें',
    'camera.stop': 'कैमरा बंद करें',
    'camera.notReady': 'कैमरा अभी तैयार नहीं है। कैप्चर करने से पहले पूर्वावलोकन लोड होने तक प्रतीक्षा करें।',
    'camera.captureFailed': 'फोटो कैप्चर करने में असमर्थ। कृपया पुनः प्रयास करें।',
    'camera.streamError': 'कैमरा स्ट्रीम प्रदर्शित नहीं हो सकी।',
    'camera.previewNotReady': 'कैमरा पूर्वावलोकन तैयार नहीं है। कृपया पुनः प्रयास करें।',
    'camera.notAllowed': 'कैमरा अनुमति अस्वीकृत कर दी गई। कृपया कैमरा अनुमति दें और पुनः प्रयास करें।',
    'camera.notFound': 'इस डिवाइस पर कोई कैमरा नहीं मिला। जांचें कि कैमरा जुड़ा है।',
    'camera.notReadable': 'आपका कैमरा किसी अन्य एप्लिकेशन द्वारा उपयोग में है। इसे बंद करके पुनः प्रयास करें।',
    'camera.security': 'कैमरा एक्सेस के लिए सुरक्षित (HTTPS) कनेक्शन या localhost आवश्यक है।',
    'camera.aborted': 'कैमरा खोलना रद्द कर दिया गया। कृपया पुनः प्रयास करें।',
    'camera.generic': 'कैमरा एक्सेस करने में असमर्थ। जांचें कि यह जुड़ा है और उपयोग में नहीं है।',
    'camera.unsupported': 'इस ब्राउज़र में कैमरा कैप्चर समर्थित नहीं है। आप अभी भी एक छवि अपलोड कर सकते हैं।',
    'camera.insecure': 'कैमरा एक्सेस के लिए सुरक्षित (HTTPS) कनेक्शन या localhost आवश्यक है।',

    'lang.en': 'English',
    'lang.kn': 'Kannada',
    'lang.hi': 'Hindi',
    'lang.ml': 'Malayalam',
  },

  ml: {
    'nav.home': 'ഹോം',
    'nav.leaf': 'ഇല തിരിച്ചറിയൽ',
    'nav.tablet': 'ടാബ്ലറ്റ് തിരിച്ചറിയൽ',
    'nav.prescription': 'പ്രെസ്ക്രിപ്ഷൻ',
    'nav.history': 'ചരിത്രം',
    'nav.howItWorks': 'എങ്ങനെ പ്രവർത്തിക്കുന്നു',
    'nav.about': 'കുറിച്ച്',
    'nav.signIn': 'സൈൻ ഇൻ',
    'nav.signUp': 'സൈൻ അപ്',
    'nav.logOut': 'ലോഗ് ഔട്ട്',

    // Common
    'common.back': 'പിന്നിലേക്ക്',

    'hero.badge': 'മെഷീൻ ലേണിംഗ് · ഹെൽത്ത്കെയർ AI',
    'hero.title.line1': 'ഔഷധ ഇലകളും ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റുകളും കണ്ടെത്തുന്നതിനുള്ള മെഷീൻ ലേണിംഗ് സമീപനം',
    'hero.title.line2': 'ഔഷധ ഇലകൾ',
    'hero.title.amp': '&',
    'hero.title.line3': 'ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റുകൾ',
    'hero.subtitle':
      'ഇന്റലിജന്റ് ഇമേജ് വിശകലനം ഉപയോഗിച്ച് ഔഷധ സസ്യങ്ങൾ, ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റുകൾ തിരിച്ചറിയുകയും പ്രെസ്ക്രിപ്ഷനുകളിൽ നിന്ന് മരുന്ന് വിവരങ്ങൾ എക്സ്ട്രാക്റ്റ് ചെയ്യുകയും ചെയ്യുക.',
    'hero.ctaLeaf': 'ഔഷധ ഇല തിരിച്ചറിയുക',
    'hero.ctaTablet': 'ടാബ്ലറ്റ് തിരിച്ചറിയുക',
    'hero.ctaPrescription': 'പ്രെസ്ക്രിപ്ഷൻ സ്കാൻ ചെയ്യുക',
    'hero.visual.scanning': 'സ്കാനിംഗ്',
    'hero.visual.leafDetected': 'ഇല കണ്ടെത്തി',
    'hero.visual.tabletMatched': 'ടാബ്ലറ്റ് പൊരുത്തപ്പെട്ടു',
    'hero.visual.rxExtracted': 'Rx എക്സ്ട്രാക്റ്റ് ചെയ്തു',
    'hero.visual.aiActive': 'AI മോഡൽ സജീവം',
    'hero.visual.tablet': 'ടാബ്ലറ്റ്',
    'hero.visual.paracetamol': 'പാരാസെറ്റമോൾ',
    'hero.visual.prescription': 'പ്രെസ്ക്രിപ്ഷൻ',
    'hero.visual.rx': 'Rx #0042',
    'hero.visual.confidence': 'വിശ്വാസം 96.2%',

    'features.eyebrow': 'സവിശേഷതകൾ',
    'features.title': 'എല്ലാ ദിവസത്തെ ആരോഗ്യ സംരക്ഷണത്തിനായി സ്മാർട്ട് തിരിച്ചറിയൽ',
    'features.subtitle':
      'ചിത്രങ്ങളെ കൃത്യവും മനസ്സിലാക്കാവുന്നതുമായ മരുന്ന് വിവരങ്ങളാക്കി മാറ്റുന്ന മൂന്ന് ശക്തിയുള്ള ഉപകരണങ്ങൾ.',
    'features.leaf.title': 'ഔഷധ ഇല തിരിച്ചറിയൽ',
    'features.leaf.desc':
      'ഏതെങ്കിലും ഇലയുടെ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക, മോഡൽ തത്ക്ഷണം ഔഷധ ഇനങ്ങളെ തിരിച്ചറിയുന്നു.',
    'features.leaf.cta': 'ഇല തിരിച്ചറിയുക',
    'features.tablet.title': 'ടാബ്ലറ്റ് തിരിച്ചറിയൽ',
    'features.tablet.desc':
      'ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റ് സ്നാപ്പ് ചെയ്ത് സെക്കൻഡുകൾക്കുള്ളിൽ അതിന്റെ പേര്, ഘടന, ഡോസ് വിവരങ്ങൾ നേടുക.',
    'features.tablet.cta': 'ടാബ്ലറ്റ് തിരിച്ചറിയുക',
    'features.rx.title': 'പ്രെസ്ക്രിപ്ഷൻ സ്കാനർ',
    'features.rx.desc':
      'കൈയെഴുത്തോ പ്രിന്റ് ചെയ്തതോ ആയ പ്രെസ്ക്രിപ്ഷനുകൾ സ്കാൻ ചെയ്ത് മരുന്ന് വിവരങ്ങൾ ഓട്ടോമാറ്റിക്കായി എക്സ്ട്രാക്റ്റ് ചെയ്യുക.',
    'features.rx.cta': 'പ്രെസ്ക്രിപ്ഷൻ സ്കാൻ ചെയ്യുക',

    'home.howItWorks.eyebrow': 'എങ്ങനെ പ്രവർത്തിക്കുന്നു',
    'home.howItWorks.title': 'ചിത്രത്തിൽ നിന്ന് ഉത്തരത്തിലേക്ക് നാല് ഘട്ടങ്ങൾ',
    'home.howItWorks.subtitle':
      'പരിശീലിപ്പിച്ച മെഷീൻ ലേണിംഗ് മോഡൽ നയിക്കുന്ന ലളിതവും സുതാര്യവുമായ പൈപ്പ്‌ലൈൻ.',
    'home.steps.upload.title': 'ചിത്രം അപ്‌ലോഡ് ചെയ്യുക',
    'home.steps.upload.desc':
      'നിങ്ങൾ തിരിച്ചറിയാൻ ആഗ്രഹിക്കുന്ന ഇല, ടാബ്ലറ്റ് അല്ലെങ്കിൽ പ്രെസ്ക്രിപ്ഷന്റെ വ്യക്തമായ ചിത്രം എടുക്കുകയോ അപ്‌ലോഡ് ചെയ്യുകയോ ചെയ്യുക.',
    'home.steps.analysis.title': 'ചിത്ര വിശകലനം',
    'home.steps.analysis.desc':
      'ഞങ്ങളുടെ പൈപ്പ്‌ലൈൻ ചിത്രം വൃത്തിയാക്കുന്നു, ശബ്ദം നീക്കുന്നു, തിരിച്ചറിയൽ മോഡലിനായി തയ്യാറാക്കുന്നു.',
    'home.steps.prediction.title': 'AI പ്രവചനം',
    'home.steps.prediction.desc':
      'പരിശീലിപ്പിച്ച മോഡൽ ഇനത്തെ വർഗ്ഗീകരിക്കുകയും പ്രവചനത്തിന് വിശ്വാസ സ്കോർ നൽകുകയും ചെയ്യുന്നു.',
    'home.steps.display.title': 'വിവര പ്രദർശനം',
    'home.steps.display.desc':
      'ഔഷധ നാമം, ഗുണങ്ങൾ, ഡോസ് മാർഗ്ഗനിർദ്ദേശം എന്നിവ വ്യക്തമായ റിപ്പോർട്ടിൽ കാണുക.',

    'cta.title': 'സെക്കൻഡുകൾക്കുള്ളിൽ തിരിച്ചറിയൽ ആരംഭിക്കുക',
    'cta.subtitle':
      'ഒരു ചിത്രം അപ്‌ലോഡ് ചെയ്യുക, മരുന്ന് എന്താണ്, എന്താണ് ചികിത്സിക്കുന്നത്, എങ്ങനെ ഉപയോഗിക്കുന്നു എന്ന് മോഡൽ വെളിപ്പെടുത്തട്ടെ.',
    'cta.button': 'ഇപ്പോൾ പരീക്ഷിക്കുക',

    'about.eyebrow': 'ഈ പ്രോജക്റ്റിനെ കുറിച്ച്',
    'about.title': 'MedScan AI',
    'about.subtitle':
      'ഔഷധ ഇലകളും ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റുകളും തിരിച്ചറിയുന്നതിനുള്ള മെഷീൻ ലേണിംഗ് സമീപനം',
    'about.projectTitle': 'അവസാന വർഷത്തെ അക്കാദമിക് പ്രോജക്റ്റ്',
    'about.department': 'കംപ്യൂട്ടർ സയൻസ് & എഞ്ചിനീയറിംഗ് വകുപ്പ്',
    'about.para1':
      'MedScan AI ഫാർമസ്യൂട്ടിക്കൽ, ബോട്ടാണിക്കൽ തിരിച്ചറിയലിന്റെ മേഖലയിൽ മെഷീൻ ലേണിംഗ് പ്രയോഗം പര്യവേക്ഷണം ചെയ്യുന്ന അവസാന വർഷ പദ്ധതിയാണ്.',
    'about.para2':
      'ഈ സംവിധാനം വിദ്യാർത്ഥികൾക്കും ആരോഗ്യ പ്രവർത്തകർക്കും പൊതുജനങ്ങൾക്കും പ്രായോഗികവും ആക്സസ് ചെയ്യാവുന്നതുമായ ഉപകരണമായി പ്രവർത്തിക്കാൻ രൂപകൽപ്പന ചെയ്തിരിക്കുന്നു.',
    'about.coreTitle': 'അടിസ്ഥാന കഴിവുകൾ',
    'about.coreSubtitle':
      'ഇലകൾ, ടാബ്ലറ്റുകൾ, പ്രെസ്ക്രിപ്ഷനുകൾ എന്നിവ ഉൾക്കൊള്ളുന്ന മൂന്ന് തിരിച്ചറിയൽ മൊഡ്യൂളുകൾ.',
    'about.capabilities.leaf.title': 'ഔഷധ ഇല തിരിച്ചറിയൽ',
    'about.capabilities.leaf.desc':
      'പരിശീലിപ്പിച്ച ഡീപ്-ലേണിംഗ് ക്ലാസിഫിക്കേഷൻ മോഡലുകൾ ഉപയോഗിച്ച് ഇല ചിത്രങ്ങളിൽ നിന്ന് ഔഷധ സസ്യ ഇനങ്ങളെ തിരിച്ചറിയുന്നു.',
    'about.capabilities.tablet.title': 'ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റ് തിരിച്ചറിയൽ',
    'about.capabilities.tablet.desc':
      'രൂപം, നിറം, മുദ്രണ പാറ്റേണുകൾ തുടങ്ങിയ ദൃശ്യ സവിശേഷതകളെ അടിസ്ഥാനമാക്കി ഓറൽ മെഡിക്കേഷൻ ടാബ്ലറ്റുകളെ തിരിച്ചറിയുന്നു.',
    'about.capabilities.rx.title': 'പ്രെസ്ക്രിപ്ഷൻ സ്കാനിംഗ്',
    'about.capabilities.rx.desc':
      'ഒപ്റ്റിക്കൽ കാരക്ടർ റെക്കഗ്നിഷൻ ഉപയോഗിച്ച് പ്രെസ്ക്രിപ്ഷൻ ഡോക്യുമെന്റുകളിൽ നിന്ന് വായിക്കാവുന്ന മരുന്ന് വിവരങ്ങൾ എക്സ്ട്രാക്റ്റ് ചെയ്യുന്നു.',
    'about.capabilities.ai.title': 'AI-സഹായ തിരിച്ചറിയൽ',
    'about.capabilities.ai.desc':
      'ഉപയോക്താക്കളെ സഹായിക്കാൻ വേഗത്തിലുള്ള പ്രാരംഭ തിരിച്ചറിയൽ ഫലങ്ങൾ നൽകുന്നു.',
    'about.howItWorksTitle': 'എങ്ങനെ പ്രവർത്തിക്കുന്നു',
    'about.howItWorksSubtitle': 'തിരിച്ചറിയൽ വർക്ക്‌ഫ്ലോയുടെ ഹൈ-ലെവൽ അവലോകനം.',
    'about.step1.title': '1. അപ്‌ലോഡ്',
    'about.step1.desc': 'ചിത്രം എടുക്കുക അല്ലെങ്കിൽ തിരഞ്ഞെടുക്കുക',
    'about.step2.title': '2. വിശകലനം',
    'about.step2.desc': 'പ്രീപ്രോസസ്സ് ചെയ്ത് സവിശേഷതകൾ എക്സ്ട്രാക്റ്റ് ചെയ്യുക',
    'about.step3.title': '3. പ്രവചനം',
    'about.step3.desc': 'ML മോഡൽ ചിത്രം വർഗ്ഗീകരിക്കുന്നു',
    'about.step4.title': '4. പ്രദർശനം',
    'about.step4.desc': 'വിശ്വാസവും വിശദാംശങ്ങളുമായി ഫലങ്ങൾ',
    'about.roadmapTitle': 'ഭാവി ഇന്റഗ്രേഷൻ റോഡ്മാപ്പ്',
    'about.roadmapSubtitle':
      'പ്രൊഡക്ഷൻ-റെഡി സിസ്റ്റത്തിലേക്ക് പ്രോജക്റ്റ് മതുതിരുമ്പോൾ ആസൂത്രണം ചെയ്ത മെച്ചപ്പെടുത്തലുകൾ.',
    'about.roadmap.ml.title': 'പരിശീലിപ്പിച്ച ML മോഡലുകൾ',
    'about.roadmap.ml.desc':
      'ഔഷധ ഇലകളുടെയും ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റുകളുടെയും ക്യുറേറ്റഡ് ഡാറ്റാസെറ്റുകളിൽ പരിശീലിപ്പിച്ച കസ്റ്റം കോൺവോല്യൂഷണൽ ന്യൂറൽ നെറ്റ്‌വർക്കുകൾ വിന്യസിക്കുക.',
    'about.roadmap.backend.title': 'FastAPI ബാക്ക്‌എൻഡ്',
    'about.roadmap.backend.desc':
      'FastAPI ഉപയോഗിച്ച് നിർമ്മിച്ച ഹൈ-പെർഫോർമൻസ് Python API വഴി മോഡൽ പ്രവചനങ്ങൾ നൽകുക.',
    'about.roadmap.eval.title': 'മോഡൽ വിലയിരുത്തൽ',
    'about.roadmap.eval.desc':
      'വിശ്വസനീയമായ പ്രവചനങ്ങൾ ഉറപ്പാക്കാൻ കൃത്യത, പ്രീസിഷൻ, റീക്കോൾ, F1 സ്കോർ അളക്കുക.',
    'about.roadmap.improve.title': 'തുടർച്ചയായ മെച്ചപ്പെടുത്തൽ',
    'about.roadmap.improve.desc':
      'പുതിയ ഡാറ്റ ഉപയോഗിച്ച് മോഡലുകൾ വീണ്ടും പരിശീലിപ്പിച്ച് കൃത്യത മെച്ചപ്പെടുത്തുക.',
    'about.disclaimerTitle': 'പ്രധാന നിരാകരണം',
    'about.disclaimerDesc':
      'നിലവിലെ ഫ്രണ്ട്‌എൻഡ് ആപ്ലിക്കേഷൻ ഡെമോൺസ്ട്രേഷൻ ഉദ്ദേശ്യങ്ങൾക്കായി മോക്ക് ഡാറ്റയിൽ പ്രവർത്തിക്കുന്നു.',

    'hiw.eyebrow': 'വർക്ക്‌ഫ്ലോ',
    'hiw.title': 'എങ്ങനെ പ്രവർത്തിക്കുന്നു',
    'hiw.subtitle':
      'MedScan AI തിരിച്ചറിയൽ പൈപ്പ്‌ലൈന്റെ നാല് ഘട്ട അവലോകനം — ചിത്ര അപ്‌ലോഡ് മുതൽ വിശദമായ ഫലം വരെ.',
    'hiw.steps.upload.title': 'ചിത്രം അപ്‌ലോഡ് ചെയ്യുക',
    'hiw.steps.upload.desc':
      'നിങ്ങളുടെ ഉപകരണ ക്യാമറ ഉപയോഗിച്ച് ഫോട്ടോ എടുക്കുകയോ ഔഷധ ഇല, ടാബ്ലറ്റ്, അല്ലെങ്കിൽ പ്രെസ്ക്രിപ്ഷൻ ഡോക്യുമെന്റിന്റെ നിലവിലുള്ള ചിത്രം അപ്‌ലോഡ് ചെയ്യുകയോ ചെയ്യുക.',
    'hiw.steps.analysis.title': 'ചിത്ര വിശകലനം',
    'hiw.steps.analysis.desc':
      'അപ്‌ലോഡ് ചെയ്ത ചിത്രം പ്രീപ്രോസസ്സിംഗിന് വിധേയമാകുന്നു — വലുതാക്കൽ, നോർമലൈസേഷൻ, സവിശേഷത എക്സ്ട്രാക്ഷൻ.',
    'hiw.steps.prediction.title': 'AI പ്രവചനം',
    'hiw.steps.prediction.desc':
      'ഒരു പരിശീലിപ്പിച്ച ക്ലാസിഫിക്കേഷൻ മോഡൽ പ്രീപ്രോസസ്സ് ചെയ്ത ചിത്രം വിശകലനം ചെയ്യുന്നു.',
    'hiw.steps.display.title': 'വിവര പ്രദർശനം',
    'hiw.steps.display.desc':
      'ഫലങ്ങൾ ഒരു വ്യക്തമായ ഡാഷ്‌ബോർഡിൽ അവതരിപ്പിക്കുന്നു.',
    'hiw.cards.camera.title': 'ക്യാമറ ക്യാപ്ചർ',
    'hiw.cards.camera.desc':
      'റിയൽ-ടൈം തിരിച്ചറിയലിനായി നിങ്ങളുടെ ഉപകരണ ക്യാമറയിൽ നിന്ന് നേരിട്ട് ഫോട്ടോ എടുക്കുക.',
    'hiw.cards.ocr.title': 'പ്രെസ്ക്രിപ്ഷൻ OCR',
    'hiw.cards.ocr.desc':
      'ഒപ്റ്റിക്കൽ കാരക്ടർ റെക്കഗ്നിഷൻ ഉപയോഗിച്ച് വായിക്കാവുന്ന മരുന്ന് വിവരങ്ങൾ എക്സ്ട്രാക്റ്റ് ചെയ്യുക.',
    'hiw.cards.details.title': 'സമ്പൂർണ്ണ വിശദാംശങ്ങൾ',
    'hiw.cards.details.desc':
      'ഉപയോഗങ്ങൾ, സജീവ സംയോജനങ്ങൾ, പാർശ്വ ഫലങ്ങൾ, മുൻകരുതലുകൾ എന്നിവ ഉൾക്കൊള്ളുന്ന വിശദമായ പ്രൊഫൈലുകൾ ആക്സസ് ചെയ്യുക.',

    'disclaimer':
      'ഈ ആപ്ലിക്കേഷൻ വിദ്യാഭ്യാസ, വിവര ഉദ്ദേശ്യങ്ങൾക്കായി AI-സഹായ തിരിച്ചറിയൽ നൽകുന്നു. ഇത് പ്രൊഫഷണൽ മെഡിക്കൽ ഉപദേശത്തിന് പകരമല്ല.',

    'footer.desc':
      'സുരക്ഷിതവും ബോധവല്ക്കരിക്കപ്പെട്ടതുമായ ആരോഗ്യ സംരക്ഷണം പിന്തുണയ്ക്കാൻ ഔഷധ ഇലകളും ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റുകളും തിരിച്ചറിയുന്നതിനുള്ള മെഷീൻ ലേണിംഗ് സമീപനം.',
    'footer.explore': 'പര്യവേക്ഷണം',
    'footer.learnMore': 'കൂടുതൽ അറിയുക',
    'footer.privacy': 'സ്വകാര്യതാ നയം',
    'footer.terms': 'സേവന നിബന്ധനകൾ',
    'footer.getInTouch': 'ബന്ധപ്പെടുക',
    'footer.address': 'യൂണിവേഴ്‌സിറ്റി കാമ്പസ്, കംപ്യൂട്ടിംഗ് ഫാക്കൽറ്റി, ശ്രീലങ്ക',
    'footer.allRights': 'MedScan AI. എല്ലാ അവകാശങ്ങളും സംരക്ഷിതം.',
    'footer.builtWithPrefix': 'ഇത് ഉപയോഗിച്ച് നിർമ്മിച്ചത്',
    'footer.and': 'ഒപ്പം',
    'footer.builtWithSuffix': 'മെച്ചപ്പെട്ട ആരോഗ്യത്തിനായി',

    'detect.uploadTitle': 'ചിത്രം അപ്‌ലോഡ് ചെയ്യുക',
    'detect.uploadHint': 'നിങ്ങളുടെ ചിത്രം ഇവിടെ വലിച്ചിടുക അല്ലെങ്കിൽ ഫയലുകൾ ബ്രൗസ് ചെയ്യുക',
    'detect.uploadLabel': 'ഒരു ചിത്രം അപ്‌ലോഡ് ചെയ്യുക',
    'detect.supportedFormats': 'പിന്തുണയ്ക്കുന്ന ഫോർമാറ്റുകൾ: JPG, JPEG, PNG',
    'detect.captureTitle': 'ക്യാമറ ഉപയോഗിച്ച് എടുക്കുക',
    'detect.captureHint': 'ഫോട്ടോ എടുക്കാൻ ക്യാമറ അനുമതി നൽകുക.',
    'detect.cameraPreview': 'ക്യാമറ പ്രീവ്യൂ',
    'detect.analyze': 'വിശകലനം',
    'detect.analyzing': 'വിശകലനം നടക്കുന്നു…',
    'detect.analyzeLeaf': 'ഇല വിശകലനം',
    'detect.analyzeTablet': 'ടാബ്ലറ്റ് വിശകലനം',
    'detect.analyzePrescription': 'പ്രെസ്ക്രിപ്ഷൻ വിശകലനം',

    'leafDetection.eyebrow': 'ഇല തിരിച്ചറിയൽ',
    'leafDetection.title': 'ഔഷധ ഇല തിരിച്ചറിയൽ',
    'leafDetection.subtitle':
      'ചെടിയെ തിരിച്ചറിയാൻ ഔഷധ ഇലയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക അല്ലെങ്കിൽ എടുക്കുക.',
    'tabletDetection.eyebrow': 'ടാബ്ലറ്റ് തിരിച്ചറിയൽ',
    'tabletDetection.title': 'ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റ് തിരിച്ചറിയൽ',
    'tabletDetection.subtitle':
      'മരുന്ന് തിരിച്ചറിയാൻ ഫാർമസ്യൂട്ടിക്കൽ ടാബ്ലറ്റിന്റെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക അല്ലെങ്കിൽ എടുക്കുക.',
    'rxScanner.eyebrow': 'പ്രെസ്ക്രിപ്ഷൻ സ്കാനർ',
    'rxScanner.title': 'പ്രെസ്ക്രിപ്ഷൻ സ്കാനർ',
    'rxScanner.subtitle':
      'വായിക്കാവുന്ന മരുന്ന് വിവരങ്ങൾ എക്സ്ട്രാക്റ്റ് ചെയ്യാൻ പ്രെസ്ക്രിപ്ഷൻ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക.',
    'rxScanner.uploadTitle': 'പ്രെസ്ക്രിപ്ഷൻ അപ്‌ലോഡ് ചെയ്യുക',
    'rxScanner.uploadLabel': 'പ്രെസ്ക്രിപ്ഷൻ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക',
    'rxScanner.uploadHint': 'നിങ്ങളുടെ പ്രെസ്ക്രിപ്ഷൻ ഇവിടെ വലിച്ചിടുക അല്ലെങ്കിൽ ഫയലുകൾ ബ്രൗസ് ചെയ്യുക',
    'rxScanner.changeImage': 'ചിത്രം മാറ്റുക',
    'rxScanner.supportedFormats': 'പിന്തുണയ്ക്കുന്ന ഫോർമാറ്റുകൾ: JPG, JPEG, PNG, WEBP',
    'rxScanner.handwritten': 'കൈയെഴുത്തുള്ള പ്രെസ്ക്രിപ്ഷൻ',
    'rxScanner.overlayTitle': 'കൈയെഴുത്തുള്ള പ്രെസ്ക്രിപ്ഷൻ വായിക്കുന്നു',
    'rxScanner.overlayDesc':
      'ഡെമോ ഡാറ്റ ഉപയോഗിച്ച് മരുന്ന് വിശദാംശങ്ങൾ എക്സ്ട്രാക്റ്റ് ചെയ്യുന്നത് അനുകരിക്കുന്നു…',
    'rxScanner.scanning': 'സ്കാൻ ചെയ്യുന്നു…',
    'rxScanner.scan': 'പ്രെസ്ക്രിപ്ഷൻ സ്കാൻ ചെയ്യുക',
    'rxScanner.ocrTitle': 'OCR സ്കാനിംഗ്',
    'rxScanner.ocrDesc': 'വായിക്കാവുന്ന മരുന്ന് വിവരങ്ങൾ എക്സ്ട്രാക്റ്റ് ചെയ്യുന്നു…',
    'rxScanner.error': 'പ്രെസ്ക്രിപ്ഷൻ സ്കാൻ ചെയ്യാൻ കഴിഞ്ഞില്ല. വീണ്ടും ശ്രമിക്കുക.',
    'rxScanner.genericError': 'പ്രെസ്ക്രിപ്ഷൻ സ്കാൻ ചെയ്യുമ്പോൾ എന്തോ കുഴപ്പം സംഭവിച്ചു. വീണ്ടും ശ്രമിക്കുക.',

    'camera.starting': 'ക്യാമറ ആരംഭിക്കുന്നു…',
    'camera.requesting': 'ക്യാമറ അനുമതി അഭ്യർത്ഥിക്കുന്നു…',
    'camera.opening': 'ക്യാമറ തുറക്കുന്നു…',
    'camera.ready': 'ലൈവ് പ്രീവ്യൂ തയ്യാറാണ്. ഫോട്ടോ എടുക്കാൻ വീണ്ടും അമർത്തുക.',
    'camera.captured': 'ഫോട്ടോ എടുത്തു.',
    'camera.capture': 'ഫോട്ടോ എടുക്കുക',
    'camera.stop': 'ക്യാമറ നിർത്തുക',
    'camera.notReady': 'ക്യാമറ തയ്യാറായിട്ടില്ല. എടുക്കുന്നതിന് മുമ്പ് പ്രീവ്യൂ ലോഡാകുന്നത് വരെ കാത്തിരിക്കുക.',
    'camera.captureFailed': 'ഫോട്ടോ എടുക്കാൻ കഴിഞ്ഞില്ല. വീണ്ടും ശ്രമിക്കുക.',
    'camera.streamError': 'ക്യാമറ സ്ട്രീം പ്രദർശിപ്പിക്കാൻ കഴിഞ്ഞില്ല.',
    'camera.previewNotReady': 'ക്യാമറ പ്രീവ്യൂ തയ്യാറില്ല. വീണ്ടും ശ്രമിക്കുക.',
    'camera.notAllowed': 'ക്യാമറ അനുമതി നിരസിച്ചു. അനുമതി അനുവദിച്ച് വീണ്ടും ശ്രമിക്കുക.',
    'camera.notFound': 'ഈ ഉപകരണത്തിൽ ക്യാമറ കണ്ടെത്തിയില്ല. ക്യാമറ കണക്റ്റ് ചെയ്തിട്ടുണ്ടോയെന്ന് പരിശോധിക്കുക.',
    'camera.notReadable': 'നിങ്ങളുടെ ക്യാമറ മറ്റൊരു ആപ്പ് ഉപയോഗിക്കുന്നു. അത് അടച്ച് വീണ്ടും ശ്രമിക്കുക.',
    'camera.security': 'ക്യാമറ ആക്സസിന് സുരക്ഷിത (HTTPS) കണക്ഷൻ അല്ലെങ്കിൽ localhost ആവശ്യമാണ്.',
    'camera.aborted': 'ക്യാമറ തുറക്കൽ റദ്ദാക്കി. വീണ്ടും ശ്രമിക്കുക.',
    'camera.generic': 'ക്യാമറ ആക്സസ് ചെയ്യാൻ കഴിഞ്ഞില്ല. അത് കണക്റ്റ് ചെയ്തിട്ടുണ്ടോയെന്നും ഉപയോഗത്തിലില്ലെന്നും പരിശോധിക്കുക.',
    'camera.unsupported': 'ഈ ബ്രൗസറിൽ ക്യാമറ ക്യാപ്ചർ പിന്തുണയ്ക്കുന്നില്ല. നിങ്ങൾക്ക് ഇപ്പോഴും ഒരു ചിത്രം അപ്‌ലോഡ് ചെയ്യാം.',
    'camera.insecure': 'ക്യാമറ ആക്സസിന് സുരക്ഷിത (HTTPS) കണക്ഷൻ അല്ലെങ്കിൽ localhost ആവശ്യമാണ്.',

    'lang.en': 'English',
    'lang.kn': 'Kannada',
    'lang.hi': 'Hindi',
    'lang.ml': 'Malayalam',
  },
}

export default translations