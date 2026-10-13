"""
Medicine & Prescription Entity Extractor.
Uses regex patterns, domain heuristics, and fuzzy matching to extract structured medical details.
"""

import difflib
import logging
import re
from typing import List, Dict, Any, Optional, Tuple

from .schemas import MedicineItem, PrescriptionHeader, PrescriptionResult

logger = logging.getLogger("medicine.prescription_ocr.extractor")


# Canonical Pharmaceutical Reference Dictionary
KNOWN_MEDICINES = {
    # Analgesics & Antipyretics
    "paracetamol": {"canonical": "Paracetamol", "generic": "Paracetamol / Acetaminophen", "default_form": "Tablet"},
    "acetaminophen": {"canonical": "Acetaminophen", "generic": "Paracetamol", "default_form": "Tablet"},
    "ibuprofen": {"canonical": "Ibuprofen", "generic": "Ibuprofen", "default_form": "Tablet"},
    "diclofenac": {"canonical": "Diclofenac", "generic": "Diclofenac Sodium", "default_form": "Tablet"},
    "aceclofenac": {"canonical": "Aceclofenac", "generic": "Aceclofenac", "default_form": "Tablet"},
    "aspirin": {"canonical": "Aspirin", "generic": "Acetylsalicylic Acid", "default_form": "Tablet"},
    "tramadol": {"canonical": "Tramadol", "generic": "Tramadol Hydrochloride", "default_form": "Capsule"},
    "naproxen": {"canonical": "Naproxen", "generic": "Naproxen", "default_form": "Tablet"},
    "mefenamic acid": {"canonical": "Mefenamic Acid", "generic": "Mefenamic Acid", "default_form": "Tablet"},

    # Antibiotics & Antifungals
    "amoxicillin": {"canonical": "Amoxicillin", "generic": "Amoxicillin", "default_form": "Capsule"},
    "amox clav": {"canonical": "Amoxicillin + Clavulanate", "generic": "Amoxicillin-Clavulanic Acid", "default_form": "Tablet"},
    "augmentin": {"canonical": "Augmentin", "generic": "Amoxicillin-Clavulanate", "default_form": "Tablet"},
    "azithromycin": {"canonical": "Azithromycin", "generic": "Azithromycin", "default_form": "Tablet"},
    "ciprofloxacin": {"canonical": "Ciprofloxacin", "generic": "Ciprofloxacin", "default_form": "Tablet"},
    "levofloxacin": {"canonical": "Levofloxacin", "generic": "Levofloxacin", "default_form": "Tablet"},
    "cefixime": {"canonical": "Cefixime", "generic": "Cefixime", "default_form": "Tablet"},
    "ceftriaxone": {"canonical": "Ceftriaxone", "generic": "Ceftriaxone", "default_form": "Injection"},
    "doxycycline": {"canonical": "Doxycycline", "generic": "Doxycycline Hyclate", "default_form": "Capsule"},
    "metronidazole": {"canonical": "Metronidazole", "generic": "Metronidazole", "default_form": "Tablet"},
    "fluconazole": {"canonical": "Fluconazole", "generic": "Fluconazole", "default_form": "Tablet"},
    "clotrimazole": {"canonical": "Clotrimazole", "generic": "Clotrimazole", "default_form": "Ointment"},

    # Antihistamines & Respiratory
    "levocetirizine": {"canonical": "Levocetirizine", "generic": "Levocetirizine Dihydrochloride", "default_form": "Tablet"},
    "cetirizine": {"canonical": "Cetirizine", "generic": "Cetirizine Hydrochloride", "default_form": "Tablet"},
    "montelukast": {"canonical": "Montelukast", "generic": "Montelukast Sodium", "default_form": "Tablet"},
    "chlorpheniramine": {"canonical": "Chlorpheniramine", "generic": "Chlorpheniramine Maleate", "default_form": "Tablet"},
    "fexofenadine": {"canonical": "Fexofenadine", "generic": "Fexofenadine Hydrochloride", "default_form": "Tablet"},
    "ambroxol": {"canonical": "Ambroxol", "generic": "Ambroxol Hydrochloride", "default_form": "Syrup"},
    "dextromethorphan": {"canonical": "Dextromethorphan", "generic": "Dextromethorphan Hydrobromide", "default_form": "Syrup"},
    "salbutamol": {"canonical": "Salbutamol", "generic": "Albuterol / Salbutamol", "default_form": "Inhalation"},
    "budesonide": {"canonical": "Budesonide", "generic": "Budesonide", "default_form": "Inhalation"},
    "steam inhalation": {"canonical": "Steam Inhalation", "generic": "Steam Inhalation Therapy", "default_form": "Inhalation"},

    # Gastrointestinal
    "pantoprazole": {"canonical": "Pantoprazole", "generic": "Pantoprazole Sodium", "default_form": "Tablet"},
    "omeprazole": {"canonical": "Omeprazole", "generic": "Omeprazole", "default_form": "Capsule"},
    "rabeprazole": {"canonical": "Rabeprazole", "generic": "Rabeprazole Sodium", "default_form": "Tablet"},
    "esomeprazole": {"canonical": "Esomeprazole", "generic": "Esomeprazole Magnesium", "default_form": "Tablet"},
    "ranitidine": {"canonical": "Ranitidine", "generic": "Ranitidine Hydrochloride", "default_form": "Tablet"},
    "domperidone": {"canonical": "Domperidone", "generic": "Domperidone", "default_form": "Tablet"},
    "ondansetron": {"canonical": "Ondansetron", "generic": "Ondansetron Hydrochloride", "default_form": "Tablet"},
    "antacid": {"canonical": "Antacid", "generic": "Magnesium/Aluminum Hydroxide", "default_form": "Syrup"},
    "loperamide": {"canonical": "Loperamide", "generic": "Loperamide Hydrochloride", "default_form": "Tablet"},

    # Cardiovascular & Metabolic
    "amlodipine": {"canonical": "Amlodipine", "generic": "Amlodipine Besylate", "default_form": "Tablet"},
    "telmisartan": {"canonical": "Telmisartan", "generic": "Telmisartan", "default_form": "Tablet"},
    "losartan": {"canonical": "Losartan", "generic": "Losartan Potassium", "default_form": "Tablet"},
    "atorvastatin": {"canonical": "Atorvastatin", "generic": "Atorvastatin Calcium", "default_form": "Tablet"},
    "rosuvastatin": {"canonical": "Rosuvastatin", "generic": "Rosuvastatin Calcium", "default_form": "Tablet"},
    "metformin": {"canonical": "Metformin", "generic": "Metformin Hydrochloride", "default_form": "Tablet"},
    "glimepiride": {"canonical": "Glimepiride", "generic": "Glimepiride", "default_form": "Tablet"},

    # Vitamins & Supplements
    "vitamin c": {"canonical": "Vitamin C", "generic": "Ascorbic Acid", "default_form": "Tablet"},
    "vitamin d3": {"canonical": "Vitamin D3", "generic": "Cholecalciferol", "default_form": "Capsule"},
    "vitamin b complex": {"canonical": "Vitamin B Complex", "generic": "B-Complex Vitamins", "default_form": "Tablet"},
    "b-complex": {"canonical": "B-Complex", "generic": "B-Complex Vitamins", "default_form": "Tablet"},
    "calcium": {"canonical": "Calcium", "generic": "Calcium Carbonate / Citrate", "default_form": "Tablet"},
    "zinc": {"canonical": "Zinc", "generic": "Zinc Sulfate / Gluconate", "default_form": "Tablet"},
    "iron": {"canonical": "Iron", "generic": "Ferrous Sulfate / Fumarate", "default_form": "Tablet"},
    "folic acid": {"canonical": "Folic Acid", "generic": "Folic Acid / Vitamin B9", "default_form": "Tablet"},

    # Topical
    "calamine": {"canonical": "Calamine", "generic": "Calamine Lotion", "default_form": "Lotion"},
    "mupirocin": {"canonical": "Mupirocin", "generic": "Mupirocin 2%", "default_form": "Ointment"},
    "betamethasone": {"canonical": "Betamethasone", "generic": "Betamethasone Dipropionate", "default_form": "Cream"},
}


class MedicineExtractor:
    """
    Rule-based and fuzzy entity extractor specialized in medical prescriptions.
    Extracts Header, Patient info, Diagnosis, Medicines, Dosage, Frequency, Duration, and Advice.
    """

    def __init__(self, fuzzy_threshold: float = 0.72):
        self.fuzzy_threshold = fuzzy_threshold

    def match_medicine_name(self, text: str) -> Optional[Tuple[str, str, str, float]]:
        """
        Detect if text contains a known medicine name using substring and fuzzy matching.

        Returns:
            Tuple of (canonical_name, generic_name, default_form, match_confidence) or None
        """
        clean = re.sub(r"[^\w\s]", " ", text.lower()).strip()
        words = clean.split()

        # 1. Exact phrase or substring match (prioritize longer names like levocetirizine before cetirizine)
        for key in sorted(KNOWN_MEDICINES.keys(), key=lambda k: len(k), reverse=True):
            info = KNOWN_MEDICINES[key]
            if re.search(r"\b" + re.escape(key) + r"\b", clean):
                return info["canonical"], info["generic"], info["default_form"], 1.0

        # 2. Token-level fuzzy match
        best_match = None
        best_score = 0.0

        for key in sorted(KNOWN_MEDICINES.keys(), key=lambda k: len(k), reverse=True):
            info = KNOWN_MEDICINES[key]
            key_words = key.split()
            if len(key_words) == 1:
                for w in words:
                    if len(w) < 4:
                        continue
                    ratio = difflib.SequenceMatcher(None, key, w).ratio()
                    if ratio > best_score and ratio >= self.fuzzy_threshold:
                        best_score = ratio
                        best_match = (info["canonical"], info["generic"], info["default_form"], ratio)
            else:
                for i in range(len(words) - len(key_words) + 1):
                    ngram = " ".join(words[i : i + len(key_words)])
                    ratio = difflib.SequenceMatcher(None, key, ngram).ratio()
                    if ratio > best_score and ratio >= self.fuzzy_threshold:
                        best_score = ratio
                        best_match = (info["canonical"], info["generic"], info["default_form"], ratio)

        return best_match

    def extract_dosage(self, text: str) -> Optional[str]:
        """Extract medication strength (e.g. 500 mg, 10 mg, 400, 0.5%)."""
        # Pattern 1: explicit unit (500 mg, 10 mcg, 250ml, 2%, 10 mj, 10 ng, 500mj)
        m = re.search(r"\b(\d+(\.\d+)?)\s*(mg|mcg|gm?|ml|iu|%|mj|ng|ms)\b", text, re.IGNORECASE)
        if m:
            val = m.group(1)
            unit = m.group(3).lower()
            if unit in ["m", "gm", "mj", "ng", "ms"]:
                unit = "mg"
            return f"{val} {unit}"

        # Pattern 2: standalone standard strength numbers (650, 500, 400, 250, 100, 75, 50, 40, 25, 20, 10, 5)
        # Avoid matching years like 2026, or rx numbers like 1023
        m = re.search(r"\b(650|500|400|250|100|75|50|40|25|20|10|5)\b", text)
        if m:
            return f"{m.group(1)} mg"

        return None

    def extract_form(self, text: str, default_form: Optional[str] = None) -> Optional[str]:
        """Extract formulation type (Tablet, Capsule, Syrup, Lotion, etc.)."""
        patterns = [
            (r"\b(tablets?|tablct|tab|teblct|taolet|fablct|jaolet|#ablct)\b", "Tablet"),
            (r"\b(capsules?|caps?)\b", "Capsule"),
            (r"\b(syrups?|syp)\b", "Syrup"),
            (r"\b(lotions?)\b", "Lotion"),
            (r"\b(inhalations?|inhaler|inkalation)\b", "Inhalation"),
            (r"\b(injections?|inj)\b", "Injection"),
            (r"\b(ointments?|oint|creams?|gel)\b", "Ointment"),
            (r"\b(drops?)\b", "Drops"),
        ]
        for pat, form in patterns:
            if re.search(pat, text, re.IGNORECASE):
                return form

        return default_form

    def extract_frequency(self, text: str) -> Optional[str]:
        """Extract dose timing frequency (once daily, twice daily, thrice daily, etc.)."""
        patterns = [
            (r"\b(thrice\s*daily|three\s*times|3\s*times|tds|1-1-1|#hrice\s*daily|sarice\s*daily)\b", "Thrice daily"),
            (r"\b(twice\s*daily|two\s*times|bid|bd|1-0-1|ewice\s*daily)\b", "Twice daily"),
            (r"\b(once\s*daily|1\s*time|od|1-0-0|0-0-1|orce\s*daily)\b", "Once daily"),
            (r"\b(at\s*night|night|rigat|nigkt|bedtime|hs)\b", "At night"),
            (r"\b(in\s*the\s*morning|morning)\b", "Morning"),
            (r"\b(daily)\b", "Daily"),
            (r"\b(sos|as\s*needed)\b", "SOS (As needed)"),
        ]
        for pat, freq in patterns:
            if re.search(pat, text, re.IGNORECASE):
                return freq
        return None

    def extract_duration(self, text: str) -> Optional[str]:
        """Extract course duration (e.g. 5 days, 3 days, 30 days)."""
        m = re.search(r"\b(\d+)\s*(days?|jays?|doys?|weeks?|months?)\b", text, re.IGNORECASE)
        if m:
            count = m.group(1)
            unit = m.group(2).lower()
            if unit.startswith("j") or unit.startswith("d"):
                unit = "days" if count != "1" else "day"
            return f"{count} {unit}"

        m2 = re.search(r"\((\d+)\s*(days?)?\)", text, re.IGNORECASE)
        if m2:
            return f"{m2.group(1)} days"

        return None

    def extract_instructions(self, text: str) -> Optional[str]:
        """Extract administration instructions (after food, before breakfast, apply locally)."""
        patterns = [
            (r"\b(after\s*(food|meals?|eating)|aftar\s*food|4ftcr\s*food|fvod)\b", "After food"),
            (r"\b(before\s*breakfast|bcfore\s*brcakfast|empty\s*stomach)\b", "Before breakfast"),
            (r"\b(before\s*(food|meals?))\b", "Before food"),
            (r"\b(apply\s*locally|external\s*use)\b", "Apply locally"),
            (r"\b(with\s*warm\s*water)\b", "With warm water"),
        ]
        for pat, inst in patterns:
            if re.search(pat, text, re.IGNORECASE):
                return inst
        return None

    def parse_header(self, text_lines: List[str]) -> PrescriptionHeader:
        """Extract clinic, doctor, patient, date, diagnosis from header lines."""
        header = PrescriptionHeader()
        full_text = " \n ".join(text_lines)

        # 1. Clinic / Hospital name (top lines)
        for line in text_lines[:4]:
            if re.search(r"(clinic|hospital|health|centre|hall|dispensary|care)", line, re.IGNORECASE):
                header.clinic_or_hospital = line.strip()
                break

        # 2. Doctor name & qualification
        doc_m = re.search(r"\b(Dr\.?\s*[A-Za-z\s]+?)(?=\s*(MBBS|MD|MS|BAMS|Reg|Date|\n|$))", full_text, re.IGNORECASE)
        if doc_m:
            candidate = doc_m.group(1).strip()
            # Verify not advice
            if not re.search(r"\b(drink|avoid|reduce|rest|take|water)\b", candidate, re.IGNORECASE):
                header.doctor_name = candidate

        # 3. Patient Name
        pat_m = re.search(r"(?:Patient\s*Name|Patient\s*Namc|Patient)\s*[:\-]?\s*([A-Za-z\s]+?)(?=\s*(Sex|Age|Diagnosis|Rx|\n|$))", full_text, re.IGNORECASE)
        if pat_m:
            name_cand = pat_m.group(1).strip()
            if len(name_cand) > 1 and name_cand.lower() not in ["namie", "nce", "name", "namc"]:
                header.patient_name = name_cand

        # 4. Age & Sex
        age_m = re.search(r"\bAge\s*[:\-]?\s*(\d{1,3})\b", full_text, re.IGNORECASE)
        if age_m:
            header.patient_age = age_m.group(1)

        sex_m = re.search(r"\b(?:Sex|Gender)\s*[:\-]?\s*(Male|Female|M|F)\b", full_text, re.IGNORECASE)
        if sex_m:
            header.patient_sex = "Male" if sex_m.group(1).upper() in ["M", "MALE"] else "Female"

        # 5. Date
        date_m = re.search(r"\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b", full_text)
        if date_m:
            header.date = date_m.group(1)

        # 6. Rx Number
        rx_m = re.search(r"Rx\s*(?:No|Nb)?\s*[:\-]?\s*([A-Za-z0-9]+)", full_text, re.IGNORECASE)
        if rx_m:
            val = rx_m.group(1).strip()
            if val.lower() not in ["no", "nb"]:
                header.rx_number = val

        # 7. Diagnosis
        diag_m = re.search(r"(?:Diagnosis|Diag|Aosis)\s*[:\-]?\s*([A-Za-z\s]+?)(?=\s*(Rx|Advice|Tab|Cap|\d|\n|$))", full_text, re.IGNORECASE)
        if diag_m:
            diag_str = diag_m.group(1).strip()
            if len(diag_str) > 2 and diag_str.lower() not in ["diagnosis", "diag"]:
                header.diagnosis = diag_str
        else:
            for cond in ["Viral Fever", "Fever", "Migraine", "Hypertension", "Allergy", "Cold & Cough", "Cold", "Cough", "Gastritis", "Asthma"]:
                if re.search(r"\b" + re.escape(cond) + r"\b", full_text, re.IGNORECASE):
                    header.diagnosis = cond
                    break

        return header

    def extract_advice(self, text_lines: List[str]) -> List[str]:
        """Extract general doctor advice items."""
        advice_items = []
        in_advice_section = False

        for line in text_lines:
            if re.search(r"\bAdvice\b", line, re.IGNORECASE):
                in_advice_section = True
                cleaned = re.sub(r"\bAdvice\b\s*[:\-]?", "", line, flags=re.IGNORECASE).strip()
                if cleaned and len(cleaned) > 3:
                    advice_items.append(cleaned)
                continue

            if in_advice_section:
                if re.search(r"\b(Dr\.|MBBS|Reg|Date|Signature)\b", line, re.IGNORECASE):
                    in_advice_section = False
                    continue
                if len(line.strip()) > 3:
                    advice_items.append(line.strip())

        if not advice_items:
            full_text = " \n ".join(text_lines)
            advice_patterns = [
                r"Drink\s+plenty\s*(?:of)?\s*fluids?",
                r"Drink\s+warm\s*water",
                r"Avoid\s+(?:oily|spicy)\s*food",
                r"Avoid\s+screen\s*light",
                r"Avoid\s+allergens",
                r"Take\s+dark\s*room\s*rest",
                r"Reduce\s+salt\s*intake",
                r"Regular\s+BP\s*monitoring",
                r"Keep\s+the\s+affected\s+area\s+clean",
                r"\bRest\b",
            ]
            for pat in advice_patterns:
                m = re.search(pat, full_text, re.IGNORECASE)
                if m:
                    advice_items.append(m.group(0).strip())

        return list(dict.fromkeys(advice_items))

    def extract_medicines(self, text_lines: List[str], detections: List[Dict[str, Any]]) -> List[MedicineItem]:
        """
        Extract structured medicine entries from text lines and detection bounding boxes.
        """
        medicines: List[MedicineItem] = []
        seen_names = set()

        for i, line in enumerate(text_lines):
            matched = self.match_medicine_name(line)
            if not matched:
                for word in line.split():
                    matched = self.match_medicine_name(word)
                    if matched:
                        break

            if matched:
                canon_name, generic, def_form, match_conf = matched
                if canon_name in seen_names:
                    continue

                seen_names.add(canon_name)

                # Prioritize single line for dosage
                line_dosage = self.extract_dosage(line)

                # If dosage is not on current line, look ahead 1 line
                context_text = line
                if not line_dosage and i + 1 < len(text_lines):
                    context_text += " " + text_lines[i + 1]

                dosage = line_dosage or self.extract_dosage(context_text)
                form = self.extract_form(context_text, default_form=def_form)
                frequency = self.extract_frequency(context_text)
                duration = self.extract_duration(context_text)
                instructions = self.extract_instructions(context_text)

                # Find line confidence from detections
                matching_confs = [
                    d["confidence"]
                    for d in detections
                    if d["text"].lower() in line.lower() or line.lower() in d["text"].lower()
                ]
                conf = float(sum(matching_confs) / len(matching_confs)) if matching_confs else match_conf
                conf = round(conf * 0.5 + match_conf * 0.5, 4)

                item = MedicineItem(
                    name=canon_name,
                    original_text=line,
                    dosage=dosage,
                    form=form,
                    frequency=frequency,
                    duration=duration,
                    instructions=instructions,
                    confidence=conf,
                    matched_generic=generic,
                )
                medicines.append(item)

        return medicines

    def process(
        self,
        ocr_result: Dict[str, Any],
        image_path: Optional[str] = None
    ) -> PrescriptionResult:
        """
        Transform raw OCR detections into a clean PrescriptionResult.
        """
        lines = ocr_result.get("lines", [])
        detections = ocr_result.get("detections", [])
        full_text = ocr_result.get("full_text", "")
        elapsed_ms = ocr_result.get("elapsed_ms", 0.0)

        header = self.parse_header(lines)
        medicines = self.extract_medicines(lines, detections)
        advice = self.extract_advice(lines)

        overall_conf = (
            float(sum(m.confidence for m in medicines) / len(medicines))
            if medicines
            else ocr_result.get("average_confidence", 0.0)
        )

        return PrescriptionResult(
            success=True,
            image_path=image_path,
            header=header,
            medicines=medicines,
            advice=advice,
            raw_text=full_text,
            raw_lines=lines,
            overall_confidence=round(overall_conf, 4),
            processing_time_ms=elapsed_ms,
        )


def get_medicine_extractor() -> MedicineExtractor:
    """Factory helper to obtain a MedicineExtractor instance."""
    return MedicineExtractor()
