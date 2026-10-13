#!/usr/bin/env python3
"""Verify the double-counting hypothesis"""

# Actual source counts
source = {
    'Centella Asiatica': 207,
    'Coccinia Grandis': 200,
    'Eclipta Prostrata': 209,
    'Mikania Micrantha': 68,
    'Murraya koenigii': 204,
    'Stephania Japonica': 206
}

# Reported by preprocessing
reported = {
    'Centella Asiatica': 414,
    'Coccinia Grandis': 400,
    'Eclipta Prostrata': 418,
    'Mikania Micrantha': 136,
    'Murraya koenigii': 408,
    'Stephania Japonica': 412
}

# Actually copied to processed folders
actual = {
    'Centella Asiatica': 306,
    'Coccinia Grandis': 296,
    'Eclipta Prostrata': 310,
    'Mikania Micrantha': 95,
    'Murraya koenigii': 300,
    'Stephania Japonica': 302
}

print("\n" + "="*100)
print("VERIFYING DOUBLE-COUNTING HYPOTHESIS")
print("="*100)
print(f"\n{'Class':<25} {'Source':<10} {'Reported':<10} {'Ratio':<10} {'Actual':<10} {'Act/Src':<10}")
print("-"*100)

for class_name in sorted(source.keys()):
    src = source[class_name]
    rep = reported[class_name]
    act = actual[class_name]
    ratio = rep / src
    act_ratio = act / src
    
    print(f"{class_name:<25} {src:<10} {rep:<10} {ratio:>6.2f}x     {act:<10} {act_ratio:>6.2f}x")

src_total = sum(source.values())
rep_total = sum(reported.values())
act_total = sum(actual.values())
ratio_total = rep_total / src_total
act_ratio_total = act_total / src_total

print("-"*100)
print(f"{'TOTAL':<25} {src_total:<10} {rep_total:<10} {ratio_total:>6.2f}x     {act_total:<10} {act_ratio_total:>6.2f}x")

print("\n" + "="*100)
print("FINDINGS:")
print("="*100)
print(f"✓ Every class shows EXACTLY 2.00x ratio (Reported/Source)")
print(f"  This confirms the preprocessing DOUBLE-COUNTED every image")
print(f"\n✓ Actual split used {act_total} images from {src_total} available")
print(f"  This is {act_ratio_total:.2f}x the source = {(act_total/src_total)*100:.1f}% of source images")
print(f"\n✓ Since preprocessing planned for 2,188 images but only 1,094 exist,")
print(f"  the split logic selected {act_total} unique images from the available {src_total}")
print(f"\n✓ The 579 'missing' images ({rep_total - act_total}) are simply the difference between:")
print(f"  - What was planned based on double-count: {rep_total}")
print(f"  - What actually got copied (1.47x real images): {act_total}")
print("\n" + "="*100)
print("EXPLANATION OF THE DISCREPANCY:")
print("="*100)
print("1. The preprocessing scan found 1,094 real images")
print("2. BUT it double-counted them somehow, reporting 2,188 images")
print("3. The split was PLANNED for 2,188 images (70/15/15 split)")
print("4. BUT when copying files, only 1,094 unique images existed")
print("5. The splitter appears to have used some images MULTIPLE TIMES")
print("   to fill the train/val/test folders, resulting in 1,609 copies")
print(f"6. This means {act_total - src_total} = {act_total - src_total} images appear in MULTIPLE splits")
print("   or some images were duplicated within splits")
print("="*100 + "\n")
