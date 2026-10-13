const handwrittenPrescriptions = [
  {
    id: 'hwrx-demo-001',
    image: '/images/uploads/handwritten-rx-1.svg',
    patientName: 'Demo Patient',
    doctorName: 'Dr. Sharma',
    organization: 'City Medical Clinic',
    prescriptionNumber: 'RX-001',
    date: '09/09/2026',
    medicines: [
      {
        medicineName: 'Paracetamol',
        dosage: '500 mg',
        frequency: 'Twice daily',
        duration: '5 days',
        instructions: 'Take after food',
      },
      {
        medicineName: 'Amoxicillin',
        dosage: '500 mg',
        frequency: 'Three times daily',
        duration: '7 days',
        instructions: 'Complete the full course',
      },
    ],
    extractedText: `Dr. Sharma
City Medical Clinic
Patient: Demo Patient
Rx No: RX-001      Date: 09/09/2026

1. Tab. Paracetamol 500 mg  - 1-0-1 - 5 days - after food
2. Tab. Amoxicillin 500 mg  - 1-1-1 - 7 days - complete course

                                                   Dr. Sharma`,
  },
  {
    id: 'hwrx-demo-002',
    image: '/images/uploads/handwritten-rx-2.svg',
    patientName: 'Rahul Mehta',
    doctorName: 'Dr. Priya Verma',
    organization: 'Green Valley Clinic',
    prescriptionNumber: 'RX-002',
    date: '08/09/2026',
    medicines: [
      {
        medicineName: 'Cetirizine',
        dosage: '10 mg',
        frequency: 'Once daily',
        duration: '7 days',
        instructions: 'Take at night',
      },
      {
        medicineName: 'Ibuprofen',
        dosage: '200 mg',
        frequency: 'As needed',
        duration: '3 days',
        instructions: 'Max 3 tablets daily. Take with food.',
      },
    ],
    extractedText: `Dr. Priya Verma
Green Valley Clinic
Patient: Rahul Mehta, 28 yrs
Rx No: RX-002      Date: 08/09/2026

1. Tab. Cetirizine 10 mg  - Once daily - 7 days - At night
2. Tab. Ibuprofen 200 mg  - As needed - 3 days - Max 3 per day

                                                   Dr. Priya Verma`,
  },
  {
    id: 'hwrx-demo-003',
    image: '/images/uploads/handwritten-rx-3.svg',
    patientName: 'Amara Silva',
    doctorName: 'Dr. R. Nimali Fernando',
    organization: 'City General Hospital',
    prescriptionNumber: 'RX-003',
    date: '06/09/2026',
    medicines: [
      {
        medicineName: 'Metformin',
        dosage: '500 mg',
        frequency: 'Twice daily',
        duration: '30 days',
        instructions: 'Take with meals',
      },
      {
        medicineName: 'Omeprazole',
        dosage: '20 mg',
        frequency: 'Once daily',
        duration: '14 days',
        instructions: 'Take before breakfast',
      },
    ],
    extractedText: `Dr. R. Nimali Fernando
City General Hospital
Patient: Amara Silva, 45 yrs
Rx No: RX-003      Date: 06/09/2026

1. Tab. Metformin 500 mg  - Twice daily - 30 days - With meals
2. Cap. Omeprazole 20 mg  - Once daily - 14 days - Before breakfast

                                                   Dr. R. Nimali Fernando`,
  },
  {
    id: 'hwrx-demo-004',
    image: '/images/uploads/handwritten-rx-4.svg',
    patientName: 'Rohan Kumar',
    doctorName: 'Dr. Ayesha Khan',
    organization: 'Sunrise Pediatric Center',
    prescriptionNumber: 'RX-004',
    date: '05/09/2026',
    medicines: [
      {
        medicineName: 'Paracetamol Syrup',
        dosage: '5 ml (120 mg/5ml)',
        frequency: 'Twice daily',
        duration: '3 days',
        instructions: 'Give after food only',
      },
      {
        medicineName: 'Amoxicillin Syrup',
        dosage: '5 ml (125 mg/5ml)',
        frequency: 'Three times daily',
        duration: '7 days',
        instructions: 'Finish the full course',
      },
    ],
    extractedText: `Dr. Ayesha Khan
Sunrise Pediatric Center
Patient: Rohan Kumar, 7 yrs
Rx No: RX-004      Date: 05/09/2026

1. Syr. Paracetamol 120 mg/5ml  - 1-0-1 - 3 days - after food only
2. Syr. Amoxycilin 125 mg/5ml   - 1-1-1 - 7 days - finish full course

                                                   Dr. Ayesha Khan`,
  },
  {
    id: 'hwrx-demo-005',
    image: '/images/uploads/handwritten-rx-5.svg',
    patientName: 'Meera Iyer',
    doctorName: 'Dr. Sanjay Gupta',
    organization: 'Care & Cure Heart Clinic',
    prescriptionNumber: 'RX-005',
    date: '04/09/2026',
    medicines: [
      {
        medicineName: 'Amlodipine',
        dosage: '5 mg',
        frequency: 'Once daily',
        duration: '30 days',
        instructions: 'Take in the morning, before food',
      },
      {
        medicineName: 'Atorvastatin',
        dosage: '10 mg',
        frequency: 'Once daily',
        duration: '30 days',
        instructions: 'Take at night, after food',
      },
    ],
    extractedText: `Dr. Sanjay Gupta
Care & Cure Heart Clinic
Patient: Meera Iyer, 54 yrs
Rx No: RX-005      Date: 04/09/2026

1. Tab. Amlodipine 5 mg   - 1-0-0 - 30 days - morning before food
2. Tab. Atorvastatin 10 mg - 0-0-1 - 30 days - night after food

                                                   Dr. Sanjay Gupta`,
  },
]

function getHandwrittenPrescriptionById(id) {
  return handwrittenPrescriptions.find((item) => item.id === id) ?? null
}

export { handwrittenPrescriptions, getHandwrittenPrescriptionById }
export default handwrittenPrescriptions