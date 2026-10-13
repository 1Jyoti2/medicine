# 🚨 CRITICAL: Dataset Discrepancy Investigation Report

**Date:** 2026-09-18  
**Status:** ⚠️ **SEVERE DATA LEAKAGE DETECTED**  
**Investigator:** Dataset Analysis Script  

---

## Executive Summary

The investigation revealed that **579 images (26.5%)** were "excluded" from training compared to the planned split. However, the root cause is much more serious:

1. ✅ The source dataset contains **1,094 unique images**
2. ❌ The preprocessing **double-counted** every image, reporting **2,188 images**
3. ❌ The split was planned for 2,188 images but only 1,094 existed
4. ❌ **515 images (47% of unique images) appear in MULTIPLE splits**
5. ❌ **SEVERE DATA LEAKAGE**: Same images in train, validation, AND test sets

---

## 1. Which 579 Images Were "Excluded"?

**Answer:** NONE. The 579 "missing" images **never existed**.

### Breakdown:
- **Source dataset:** 1,094 unique images
- **Preprocessing reported:** 2,188 images (2x double-count)
- **Split planned for:** 2,188 images
- **Actually copied:** 1,609 image files (1.47x the source)
- **Unique images:** Only 1,094 (same as source)
- **"Missing":** 2,188 - 1,609 = 579 images that never existed

---

## 2. Why Were They "Excluded"?

**They weren't excluded—they were phantom images from double-counting.**

### Root Cause Analysis:

**Bug Location:** Image scanning in `utils/image_validator.py` or `utils/dataset_stats.py`

The preprocessing pipeline double-counted every image during the initial scan:

| Class | Source Count | Reported Count | Ratio |
|-------|--------------|----------------|-------|
| Centella Asiatica | 207 | 414 | 2.00x |
| Coccinia Grandis | 200 | 400 | 2.00x |
| Eclipta Prostrata | 209 | 418 | 2.00x |
| Mikania Micrantha | 68 | 136 | 2.00x |
| Murraya koenigii | 204 | 408 | 2.00x |
| Stephania Japonica | 206 | 412 | 2.00x |
| **TOTAL** | **1,094** | **2,188** | **2.00x** |

**Possible causes:**
- Scanning both `.jpg` and `.JPG` extensions (case-sensitive double-scan)
- Iterating through the same directory twice
- Counting files in both glob patterns

---

## 3. Were They Invalid/Corrupted/Duplicates?

**NO.**

- ✅ **Validation:** All 1,094 source images are valid (100% pass rate)
- ✅ **Corruption:** 0 corrupted files found
- ❌ **Duplicates (perceptual):** 0 duplicate pairs found (preprocessing correctly reported)
- ❌ **Duplicates (filename):** **515 filenames appear multiple times across splits** (DATA LEAKAGE)

---

## 4. Was Exclusion Intentional?

**NO.**

The exclusion was NOT intentional. It was a side effect of:
1. Planning a split for 2,188 (doubled) images
2. Only 1,094 unique images existing
3. The split logic copying images multiple times to reach the planned counts

---

## 5. Do Train/Validation/Test Contain Duplicates?

**YES - SEVERE DATA LEAKAGE**

### Duplicate Analysis:
```
Total unique images in source:     1,094
Total files in processed folders:  1,610 (includes 1 split_info.json file + 1,609 images)
Unique filenames in processed:     1,094
Duplicate filenames:               515 (47.1% of unique images)
Total duplicate instances:         1,030 file copies
```

### Overlap Breakdown:
| Overlap Type | Count | Impact |
|--------------|-------|--------|
| Train + Val | 246 images | Model sees validation data during training |
| Train + Test | 225 images | **Test accuracy artificially inflated** |
| Val + Test | 44 images | **Both metrics contaminated** |
| All 3 splits | 0 images | (None in all three, but combinations are bad enough) |

### Why This Happened:
The splitter planned to split 2,188 images with 70/15/15 ratios:
- Train: 1,529 planned
- Val: 326 planned
- Test: 333 planned

But only 1,094 unique images existed. To fill the folders, the same images were copied multiple times with random shuffling, leading to overlap.

---

## 6. Is There Data Leakage?

**YES - CRITICAL DATA LEAKAGE**

### Evidence:
1. **515 images (47% of dataset) appear in multiple splits**
2. **246 images** are in both train and val → Model memorizes validation data
3. **225 images** are in both train and test → **100% test accuracy is INVALID**
4. **44 images** are in both val and test → Validation metrics unreliable

### Impact on Training:
- The reported **100% test accuracy is NOT trustworthy**
- The model saw 225 test images during training
- Validation metrics contaminated by 246 overlapping images
- The **97.73% validation accuracy** is also inflated

**The 100% test accuracy does NOT represent true generalization ability.**

---

## 7. Can the 100% Test Accuracy Be Trusted?

**NO - ABSOLUTELY NOT**

### Reasons:
1. ❌ **225 test images (74.8% of test set) were seen during training**
2. ❌ **The model memorized these images, not learned to generalize**
3. ❌ **True test set should have 0 overlap with training data**
4. ❌ **The test set has only 301 images, 225 of which are compromised**

### What the 100% Actually Means:
- The model correctly classified images it had **already seen during training**
- It's like giving students the exact same questions they practiced on
- **TRUE generalization performance is UNKNOWN**

---

## Data Leakage Impact Analysis

### Training Set Contamination:
- **Expected:** 1,000 images (actual count)
- **Unique images:** ~650-700 (estimated, needs verification)
- **Duplicates from val:** 246 images
- **Duplicates from test:** 225 images
- **Impact:** Model trained on validation and test data

### Validation Set Contamination:
- **Expected:** 308 images (actual count)
- **Unique images:** ~60-80 (estimated)
- **Duplicates from train:** 246 images
- **Duplicates from test:** 44 images
- **Impact:** Validation accuracy inflated, early stopping unreliable

### Test Set Contamination:
- **Expected:** 301 images (actual count)
- **Unique images:** ~75-100 (estimated)
- **Duplicates from train:** 225 images (74.8% of test!)
- **Duplicates from val:** 44 images
- **Impact:** **Test accuracy completely unreliable**

---

## Detailed Per-Class Analysis

### Actual vs Planned Counts:

| Class | Source | Reported | Planned Total | Actual Total | Missing | Missing % |
|-------|--------|----------|---------------|--------------|---------|-----------|
| Centella Asiatica | 207 | 414 | 414 | 306 | 108 | 26.1% |
| Coccinia Grandis | 200 | 400 | 400 | 296 | 104 | 26.0% |
| Eclipta Prostrata | 209 | 418 | 418 | 310 | 108 | 25.8% |
| Mikania Micrantha | 68 | 136 | 136 | 95 | 41 | 30.1% |
| Murraya koenigii | 204 | 408 | 408 | 300 | 108 | 26.5% |
| Stephania Japonica | 206 | 412 | 412 | 302 | 110 | 26.7% |
| **TOTAL** | **1,094** | **2,188** | **2,188** | **1,609** | **579** | **26.5%** |

**Pattern:** All classes uniformly affected at ~26-27% "missing", confirming systematic double-counting bug.

---

## Critical Files for Investigation

### Files to Inspect:
1. `utils/image_validator.py` - May be counting files twice
2. `utils/dataset_stats.py` - May be duplicating file list
3. `utils/dataset_splitter.py` - Verify it's not intentionally duplicating
4. `prepare_dataset.py` - Check file collection logic

### Logs to Review:
- `reports/preprocessing_log.txt` - Check for double-scan evidence
- `reports/dataset_statistics.json` - Verify file dimensions list (has 414 entries per class, suggesting double-count stored)

---

## Recommended Actions

### 🚨 IMMEDIATE (Critical):
1. **DO NOT use the current model for production** - test accuracy is invalid
2. **DO NOT proceed with frontend integration** - model performance is unknown
3. **Identify and fix the double-counting bug** in preprocessing
4. **Re-run preprocessing** from scratch with fixed code
5. **Delete contaminated processed dataset** (`data/leaf_processed/`)
6. **Re-split dataset properly** with NO overlap between splits
7. **Re-train the model** with clean splits
8. **Re-evaluate on CLEAN test set**

### 📋 MEDIUM PRIORITY:
1. Add validation to preprocessing to detect:
   - File count mismatches between source and processed
   - Duplicate filenames across splits
   - Expected vs actual file counts per split
2. Add automated tests for split integrity
3. Implement split verification after each preprocessing run

### 📊 INVESTIGATION:
1. Determine the exact double-counting mechanism
2. Verify if the bug affects other datasets
3. Document the fix for future reference

---

## Technical Debt Created

1. ❌ Invalid model performance metrics
2. ❌ Untrustworthy training run (30 epochs wasted)
3. ❌ Need to retrain from scratch
4. ❌ Frontend integration blocked until clean model available
5. ❌ Project timeline impacted

---

## Verification Steps After Fix

### Before Retraining:
- [ ] Source dataset: 1,094 unique images verified
- [ ] Preprocessing reports: 1,094 images (not 2,188)
- [ ] Split totals match: Train + Val + Test = 1,094
- [ ] NO duplicate filenames across splits
- [ ] Per-class counts match source exactly

### Split Integrity Checks:
```python
# Expected with clean 70/15/15 split of 1,094 images:
train_count = int(1094 * 0.70) = 765 images
val_count = int(1094 * 0.15) = 164 images
test_count = 1094 - 765 - 164 = 165 images

# Verify:
assert len(set(train_files) & set(val_files)) == 0  # No overlap
assert len(set(train_files) & set(test_files)) == 0  # No overlap
assert len(set(val_files) & set(test_files)) == 0  # No overlap
assert len(train_files) + len(val_files) + len(test_files) == 1094
```

---

## Conclusion

The **579 "missing" images** were never missing—they were **phantom images from a double-counting bug**. However, the real problem is much worse:

**🚨 CRITICAL: 47% of the dataset appears in multiple splits, creating severe data leakage. The reported 100% test accuracy is INVALID and cannot be trusted. The model must be retrained from scratch with clean data.**

---

## Status: ⚠️ BLOCKED

**Current model training:** INVALID  
**Test accuracy (100%):** UNRELIABLE  
**Validation accuracy (97.73%):** CONTAMINATED  
**Production readiness:** NOT SAFE  

**Next steps:** Fix preprocessing bug → Clean split → Retrain → Re-evaluate

---

**Report generated:** 2026-09-18  
**Severity:** CRITICAL  
**Action required:** IMMEDIATE
