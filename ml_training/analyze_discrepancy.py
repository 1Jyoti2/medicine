#!/usr/bin/env python3
"""Quick analysis of dataset discrepancy"""

# Planned (from split_info.json)
planned = {
    'Centella Asiatica': {'train': 289, 'val': 62, 'test': 63},
    'Coccinia Grandis': {'train': 280, 'val': 60, 'test': 60},
    'Eclipta Prostrata': {'train': 292, 'val': 62, 'test': 64},
    'Mikania Micrantha': {'train': 95, 'val': 20, 'test': 21},
    'Murraya koenigii': {'train': 285, 'val': 61, 'test': 62},
    'Stephania Japonica': {'train': 288, 'val': 61, 'test': 63}
}

# Actual (from folder counts)
actual = {
    'Centella Asiatica': {'train': 192, 'val': 58, 'test': 56},
    'Coccinia Grandis': {'train': 185, 'val': 56, 'test': 55},
    'Eclipta Prostrata': {'train': 192, 'val': 59, 'test': 59},
    'Mikania Micrantha': {'train': 58, 'val': 20, 'test': 17},
    'Murraya koenigii': {'train': 187, 'val': 57, 'test': 56},
    'Stephania Japonica': {'train': 186, 'val': 58, 'test': 58}
}

print("\n" + "="*100)
print("DATASET DISCREPANCY ANALYSIS")
print("="*100)
print(f"\n{'Class':<25} {'Planned':<10} {'Actual':<10} {'Missing':<10} {'Missing %':<12} {'Train-':<10} {'Val-':<10} {'Test-'}")
print("-"*100)

total_planned = 0
total_actual = 0
total_missing = 0

for class_name in sorted(planned.keys()):
    p = planned[class_name]
    a = actual[class_name]
    
    p_total = p['train'] + p['val'] + p['test']
    a_total = a['train'] + a['val'] + a['test']
    missing = p_total - a_total
    percent = (missing / p_total) * 100
    
    train_diff = p['train'] - a['train']
    val_diff = p['val'] - a['val']
    test_diff = p['test'] - a['test']
    
    print(f"{class_name:<25} {p_total:<10} {a_total:<10} {missing:<10} {percent:>6.1f}%      {train_diff:<10} {val_diff:<10} {test_diff}")
    
    total_planned += p_total
    total_actual += a_total
    total_missing += missing

print("-"*100)
print(f"{'TOTAL':<25} {total_planned:<10} {total_actual:<10} {total_missing:<10} {(total_missing/total_planned)*100:>6.1f}%")
print("="*100)

# Check if all classes are affected equally
print("\nPATTERN ANALYSIS:")
print("-"*100)
missing_percentages = []
for class_name in sorted(planned.keys()):
    p = planned[class_name]
    a = actual[class_name]
    p_total = p['train'] + p['val'] + p['test']
    a_total = a['train'] + a['val'] + a['test']
    percent = (p_total - a_total) / p_total * 100
    missing_percentages.append(percent)
    
avg_missing = sum(missing_percentages) / len(missing_percentages)
min_missing = min(missing_percentages)
max_missing = max(missing_percentages)

print(f"Average missing percentage: {avg_missing:.1f}%")
print(f"Range: {min_missing:.1f}% to {max_missing:.1f}%")

if max_missing - min_missing < 5:
    print("\n✓ All classes are affected UNIFORMLY (~26-27% missing from each)")
    print("  This suggests a SYSTEMATIC reduction, not random corruption or selective exclusion.")
else:
    print("\n⚠ Classes are affected NON-UNIFORMLY")
    print("  This suggests selective filtering or corruption.")

print("\n" + "="*100)
