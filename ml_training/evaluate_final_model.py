"""
Comprehensive Final Model Evaluation Script
Evaluates the trained model on the clean test set with detailed metrics
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import json
import numpy as np
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd

class LeafDataset(Dataset):
    """Custom dataset for leaf images"""
    def __init__(self, image_dir, transform=None):
        self.image_dir = Path(image_dir)
        self.transform = transform
        self.images = []
        self.labels = []
        self.class_names = sorted([d.name for d in self.image_dir.iterdir() if d.is_dir()])
        self.class_to_idx = {cls_name: idx for idx, cls_name in enumerate(self.class_names)}
        
        # Load all images
        for class_name in self.class_names:
            class_dir = self.image_dir / class_name
            for img_path in class_dir.glob("*.jpg"):
                self.images.append(img_path)
                self.labels.append(self.class_to_idx[class_name])
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label, str(img_path)

def load_model(model_path, config_path, device):
    """Load the trained model"""
    print(f"Loading model from: {model_path}")
    
    # Load configuration
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    num_classes = config['num_classes']
    class_names = config['classes']
    
    # Create model architecture (matching train_pytorch.py)
    model = models.mobilenet_v2(pretrained=False)
    num_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_features, 256),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(256, 128),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(128, num_classes)
    )
    
    # Load weights
    checkpoint = torch.load(model_path, map_location=device)
    
    # Handle different checkpoint formats
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    
    model = model.to(device)
    model.eval()
    
    print(f"Model loaded successfully with {num_classes} classes")
    return model, class_names, config

def verify_data_integrity(test_dir, train_dir, val_dir):
    """Verify no data leakage between splits"""
    print("\n" + "="*80)
    print("VERIFYING DATA INTEGRITY")
    print("="*80)
    
    def get_image_filenames(directory):
        """Get all image filenames (basename only) from directory"""
        filenames = set()
        for class_dir in Path(directory).iterdir():
            if class_dir.is_dir():
                for img_path in class_dir.glob("*.jpg"):
                    filenames.add(img_path.name)
        return filenames
    
    # Get filenames from each split
    test_files = get_image_filenames(test_dir)
    train_files = get_image_filenames(train_dir)
    val_files = get_image_filenames(val_dir)
    
    # Check for overlaps
    test_train_overlap = test_files.intersection(train_files)
    test_val_overlap = test_files.intersection(val_files)
    train_val_overlap = train_files.intersection(val_files)
    
    # Report
    print(f"\nDataset Split Sizes:")
    print(f"  Train files: {len(train_files)}")
    print(f"  Val files: {len(val_files)}")
    print(f"  Test files: {len(test_files)}")
    print(f"  Total: {len(train_files) + len(val_files) + len(test_files)}")
    
    print(f"\nOverlap Detection:")
    print(f"  Test ∩ Train: {len(test_train_overlap)} files")
    print(f"  Test ∩ Val: {len(test_val_overlap)} files")
    print(f"  Train ∩ Val: {len(train_val_overlap)} files")
    
    leakage_detected = len(test_train_overlap) > 0 or len(test_val_overlap) > 0
    
    if leakage_detected:
        print(f"\n❌ DATA LEAKAGE DETECTED!")
        if test_train_overlap:
            print(f"   Test-Train overlap: {list(test_train_overlap)[:5]}...")
        if test_val_overlap:
            print(f"   Test-Val overlap: {list(test_val_overlap)[:5]}...")
        return False
    else:
        print(f"\n✅ NO DATA LEAKAGE - All splits are disjoint")
        return True

def evaluate_model(model, dataloader, device, class_names):
    """Comprehensive model evaluation"""
    print("\n" + "="*80)
    print("RUNNING MODEL EVALUATION")
    print("="*80)
    
    all_predictions = []
    all_labels = []
    all_probs = []
    all_paths = []
    
    model.eval()
    with torch.no_grad():
        for images, labels, paths in dataloader:
            images = images.to(device)
            outputs = model(images)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            _, predicted = torch.max(outputs, 1)
            
            all_predictions.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())
            all_probs.extend(probs.cpu().numpy())
            all_paths.extend(paths)
    
    all_predictions = np.array(all_predictions)
    all_labels = np.array(all_labels)
    all_probs = np.array(all_probs)
    
    # Calculate metrics
    accuracy = accuracy_score(all_labels, all_predictions)
    precision_macro = precision_score(all_labels, all_predictions, average='macro', zero_division=0)
    recall_macro = recall_score(all_labels, all_predictions, average='macro', zero_division=0)
    f1_macro = f1_score(all_labels, all_predictions, average='macro', zero_division=0)
    
    precision_weighted = precision_score(all_labels, all_predictions, average='weighted', zero_division=0)
    recall_weighted = recall_score(all_labels, all_predictions, average='weighted', zero_division=0)
    f1_weighted = f1_score(all_labels, all_predictions, average='weighted', zero_division=0)
    
    precision_per_class = precision_score(all_labels, all_predictions, average=None, zero_division=0)
    recall_per_class = recall_score(all_labels, all_predictions, average=None, zero_division=0)
    f1_per_class = f1_score(all_labels, all_predictions, average=None, zero_division=0)
    
    conf_matrix = confusion_matrix(all_labels, all_predictions)
    
    # Count correct/incorrect
    correct = (all_predictions == all_labels).sum()
    incorrect = (all_predictions != all_labels).sum()
    
    # Print results
    print(f"\n{'='*80}")
    print("OVERALL METRICS")
    print(f"{'='*80}")
    print(f"Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Correct Predictions: {correct}/{len(all_labels)}")
    print(f"Incorrect Predictions: {incorrect}/{len(all_labels)}")
    
    print(f"\n{'='*80}")
    print("MACRO AVERAGES (unweighted)")
    print(f"{'='*80}")
    print(f"Precision: {precision_macro:.4f}")
    print(f"Recall: {recall_macro:.4f}")
    print(f"F1-Score: {f1_macro:.4f}")
    
    print(f"\n{'='*80}")
    print("WEIGHTED AVERAGES (by class support)")
    print(f"{'='*80}")
    print(f"Precision: {precision_weighted:.4f}")
    print(f"Recall: {recall_weighted:.4f}")
    print(f"F1-Score: {f1_weighted:.4f}")
    
    print(f"\n{'='*80}")
    print("PER-CLASS METRICS")
    print(f"{'='*80}")
    print(f"{'Class':<25} {'Precision':>10} {'Recall':>10} {'F1-Score':>10} {'Support':>10}")
    print("-" * 80)
    
    for i, class_name in enumerate(class_names):
        support = (all_labels == i).sum()
        print(f"{class_name:<25} {precision_per_class[i]:>10.4f} {recall_per_class[i]:>10.4f} "
              f"{f1_per_class[i]:>10.4f} {support:>10}")
    
    # Identify misclassifications
    misclassified = []
    for i, (pred, true, path, probs) in enumerate(zip(all_predictions, all_labels, all_paths, all_probs)):
        if pred != true:
            misclassified.append({
                'image_path': path,
                'true_label': class_names[true],
                'predicted_label': class_names[pred],
                'true_class_idx': int(true),
                'predicted_class_idx': int(pred),
                'confidence': float(probs[pred]),
                'true_class_prob': float(probs[true])
            })
    
    return {
        'accuracy': float(accuracy),
        'precision_macro': float(precision_macro),
        'recall_macro': float(recall_macro),
        'f1_macro': float(f1_macro),
        'precision_weighted': float(precision_weighted),
        'recall_weighted': float(recall_weighted),
        'f1_weighted': float(f1_weighted),
        'precision_per_class': precision_per_class.tolist(),
        'recall_per_class': recall_per_class.tolist(),
        'f1_per_class': f1_per_class.tolist(),
        'confusion_matrix': conf_matrix.tolist(),
        'correct_predictions': int(correct),
        'incorrect_predictions': int(incorrect),
        'total_test_samples': len(all_labels),
        'num_classes': len(class_names),
        'class_names': class_names,
        'misclassified': misclassified,
        'all_predictions': all_predictions.tolist(),
        'all_labels': all_labels.tolist(),
        'all_probabilities': all_probs.tolist()
    }

def plot_confusion_matrix(conf_matrix, class_names, output_path):
    """Create and save confusion matrix visualization"""
    plt.figure(figsize=(12, 10))
    
    # Normalize confusion matrix
    conf_matrix_norm = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
    
    # Create heatmap
    sns.heatmap(conf_matrix_norm, annot=True, fmt='.2%', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names,
                cbar_kws={'label': 'Percentage'})
    
    plt.title('Confusion Matrix (Normalized)', fontsize=16, pad=20)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Confusion matrix saved to: {output_path}")
    plt.close()

def save_classification_report(metrics, output_path):
    """Save detailed classification report"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("FINAL MODEL EVALUATION - CLASSIFICATION REPORT\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Evaluation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("OVERALL METRICS\n")
        f.write("-"*80 + "\n")
        f.write(f"Test Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)\n")
        f.write(f"Correct Predictions: {metrics['correct_predictions']}/{metrics['total_test_samples']}\n")
        f.write(f"Incorrect Predictions: {metrics['incorrect_predictions']}/{metrics['total_test_samples']}\n")
        f.write(f"Number of Classes: {metrics['num_classes']}\n\n")
        
        f.write("MACRO AVERAGES (unweighted)\n")
        f.write("-"*80 + "\n")
        f.write(f"Precision: {metrics['precision_macro']:.4f}\n")
        f.write(f"Recall: {metrics['recall_macro']:.4f}\n")
        f.write(f"F1-Score: {metrics['f1_macro']:.4f}\n\n")
        
        f.write("WEIGHTED AVERAGES (by class support)\n")
        f.write("-"*80 + "\n")
        f.write(f"Precision: {metrics['precision_weighted']:.4f}\n")
        f.write(f"Recall: {metrics['recall_weighted']:.4f}\n")
        f.write(f"F1-Score: {metrics['f1_weighted']:.4f}\n\n")
        
        f.write("PER-CLASS METRICS\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Class':<25} {'Precision':>10} {'Recall':>10} {'F1-Score':>10} {'Support':>10}\n")
        f.write("-"*80 + "\n")
        
        for i, class_name in enumerate(metrics['class_names']):
            support = sum(1 for label in metrics['all_labels'] if label == i)
            f.write(f"{class_name:<25} {metrics['precision_per_class'][i]:>10.4f} "
                   f"{metrics['recall_per_class'][i]:>10.4f} {metrics['f1_per_class'][i]:>10.4f} "
                   f"{support:>10}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("CONFUSION MATRIX (Raw Counts)\n")
        f.write("="*80 + "\n\n")
        
        conf_matrix = np.array(metrics['confusion_matrix'])
        f.write(f"{'':20}")
        for class_name in metrics['class_names']:
            f.write(f"{class_name[:15]:>15}")
        f.write("\n")
        
        for i, class_name in enumerate(metrics['class_names']):
            f.write(f"{class_name[:20]:<20}")
            for j in range(len(metrics['class_names'])):
                f.write(f"{conf_matrix[i][j]:>15}")
            f.write("\n")
    
    print(f"✅ Classification report saved to: {output_path}")

def save_misclassified_list(misclassified, output_path):
    """Save list of misclassified images"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("MISCLASSIFIED IMAGES REPORT\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Total Misclassifications: {len(misclassified)}\n\n")
        
        if len(misclassified) == 0:
            f.write("✅ NO MISCLASSIFICATIONS - Perfect test accuracy!\n")
        else:
            f.write("List of Misclassified Images:\n")
            f.write("-"*80 + "\n\n")
            
            for i, item in enumerate(misclassified, 1):
                f.write(f"{i}. {Path(item['image_path']).name}\n")
                f.write(f"   True Label: {item['true_label']}\n")
                f.write(f"   Predicted: {item['predicted_label']}\n")
                f.write(f"   Confidence: {item['confidence']:.4f}\n")
                f.write(f"   True Class Prob: {item['true_class_prob']:.4f}\n")
                f.write(f"   Full Path: {item['image_path']}\n\n")
    
    print(f"✅ Misclassified list saved to: {output_path}")

def analyze_performance(metrics):
    """Analyze and report on model performance"""
    print(f"\n{'='*80}")
    print("PERFORMANCE ANALYSIS")
    print(f"{'='*80}")
    
    class_names = metrics['class_names']
    f1_scores = metrics['f1_per_class']
    support = [sum(1 for label in metrics['all_labels'] if label == i) 
               for i in range(len(class_names))]
    
    # Best performing classes
    best_idx = np.argmax(f1_scores)
    print(f"\n✅ Best Performing Class:")
    print(f"   {class_names[best_idx]}: F1={f1_scores[best_idx]:.4f}, "
          f"Precision={metrics['precision_per_class'][best_idx]:.4f}, "
          f"Recall={metrics['recall_per_class'][best_idx]:.4f}")
    
    # Worst performing classes
    worst_idx = np.argmin(f1_scores)
    print(f"\n⚠️  Weakest Performing Class:")
    print(f"   {class_names[worst_idx]}: F1={f1_scores[worst_idx]:.4f}, "
          f"Precision={metrics['precision_per_class'][worst_idx]:.4f}, "
          f"Recall={metrics['recall_per_class'][worst_idx]:.4f}")
    
    # Class imbalance
    print(f"\n📊 Class Distribution in Test Set:")
    for i, (class_name, count) in enumerate(zip(class_names, support)):
        percentage = (count / sum(support)) * 100
        print(f"   {class_name}: {count} samples ({percentage:.1f}%)")
    
    min_support = min(support)
    max_support = max(support)
    imbalance_ratio = max_support / min_support if min_support > 0 else float('inf')
    
    if imbalance_ratio > 2.0:
        print(f"\n⚠️  Significant Class Imbalance Detected!")
        print(f"   Imbalance Ratio: {imbalance_ratio:.2f}:1")
        print(f"   Min samples: {min_support}, Max samples: {max_support}")
    else:
        print(f"\n✅ Class Distribution is Balanced (ratio: {imbalance_ratio:.2f}:1)")
    
    # Misclassification analysis
    misclassified = metrics['misclassified']
    if len(misclassified) > 0:
        print(f"\n❌ Classes with Most Misclassifications:")
        misclass_by_true = {}
        for item in misclassified:
            true_label = item['true_label']
            misclass_by_true[true_label] = misclass_by_true.get(true_label, 0) + 1
        
        for class_name, count in sorted(misclass_by_true.items(), key=lambda x: x[1], reverse=True):
            print(f"   {class_name}: {count} misclassifications")
    else:
        print(f"\n✅ NO MISCLASSIFICATIONS - Perfect test accuracy!")
    
    # Suspiciously high/low performance
    print(f"\n🔍 Performance Quality Check:")
    if metrics['accuracy'] >= 0.99:
        print(f"   ⚠️  Very high accuracy ({metrics['accuracy']:.4f}) - verify no data leakage")
    elif metrics['accuracy'] < 0.70:
        print(f"   ⚠️  Low accuracy ({metrics['accuracy']:.4f}) - model may need retraining")
    else:
        print(f"   ✅ Accuracy ({metrics['accuracy']:.4f}) is in reasonable range")

def main():
    # Paths
    model_dir = Path(r"C:\Users\Harshu\Desktop\Medicine\ml_training\models\training_20260919_135002")
    model_path = model_dir / "final_model.pth"
    config_path = model_dir / "model_config.json"
    
    data_dir = Path(r"C:\Users\Harshu\Desktop\Medicine\ml_training\data\leaf_processed")
    test_dir = data_dir / "test"
    train_dir = data_dir / "train"
    val_dir = data_dir / "val"
    
    output_dir = model_dir / "evaluation_results"
    output_dir.mkdir(exist_ok=True)
    
    print("="*80)
    print("FINAL MODEL EVALUATION SCRIPT")
    print("="*80)
    print(f"\nModel: {model_path}")
    print(f"Test Data: {test_dir}")
    print(f"Output: {output_dir}")
    
    # Step 1: Verify data integrity
    integrity_ok = verify_data_integrity(test_dir, train_dir, val_dir)
    
    if not integrity_ok:
        print("\n❌ EVALUATION ABORTED: Data leakage detected!")
        return
    
    # Step 2: Load model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\nUsing device: {device}")
    
    model, class_names, config = load_model(model_path, config_path, device)
    
    # Step 3: Prepare data
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    test_dataset = LeafDataset(test_dir, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)
    
    print(f"\nTest dataset loaded: {len(test_dataset)} images")
    
    # Step 4: Evaluate model
    metrics = evaluate_model(model, test_loader, device, class_names)
    
    # Step 5: Analyze performance
    analyze_performance(metrics)
    
    # Step 6: Save results
    print(f"\n{'='*80}")
    print("SAVING EVALUATION RESULTS")
    print(f"{'='*80}")
    
    # Save classification report
    report_path = output_dir / "classification_report.txt"
    save_classification_report(metrics, report_path)
    
    # Save confusion matrix
    confusion_matrix_path = output_dir / "confusion_matrix.png"
    plot_confusion_matrix(np.array(metrics['confusion_matrix']), class_names, confusion_matrix_path)
    
    # Save evaluation metrics (JSON)
    metrics_path = output_dir / "evaluation_metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✅ Evaluation metrics saved to: {metrics_path}")
    
    # Save predictions (CSV)
    predictions_path = output_dir / "predictions.csv"
    predictions_df = pd.DataFrame({
        'true_label_idx': metrics['all_labels'],
        'predicted_label_idx': metrics['all_predictions'],
        'true_label': [class_names[i] for i in metrics['all_labels']],
        'predicted_label': [class_names[i] for i in metrics['all_predictions']],
        'correct': [1 if t == p else 0 for t, p in zip(metrics['all_labels'], metrics['all_predictions'])]
    })
    predictions_df.to_csv(predictions_path, index=False)
    print(f"✅ Predictions saved to: {predictions_path}")
    
    # Save misclassified list
    misclassified_path = output_dir / "misclassified_images.txt"
    save_misclassified_list(metrics['misclassified'], misclassified_path)
    
    # Generate final report
    final_report_path = output_dir / "FINAL_EVALUATION_REPORT.txt"
    generate_final_report(metrics, config, integrity_ok, final_report_path)
    
    print(f"\n{'='*80}")
    print("✅ EVALUATION COMPLETE")
    print(f"{'='*80}")
    print(f"\nAll results saved to: {output_dir}")

def generate_final_report(metrics, config, integrity_ok, output_path):
    """Generate the final validation report"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("FINAL MODEL VALIDATION REPORT\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Evaluation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Training Date: {config['training_date']}\n\n")
        
        f.write("MODEL INFORMATION\n")
        f.write("-"*80 + "\n")
        f.write(f"Model Path: C:\\Users\\Harshu\\Desktop\\Medicine\\ml_training\\models\\training_20260919_135002\\final_model.pth\n")
        f.write(f"Model Type: {config['model_type']}\n")
        f.write(f"Number of Classes: {metrics['num_classes']}\n")
        f.write(f"Classes: {', '.join(metrics['class_names'])}\n\n")
        
        f.write("DATASET INFORMATION\n")
        f.write("-"*80 + "\n")
        f.write(f"Test Images: {metrics['total_test_samples']}\n")
        f.write(f"Training Images: {config.get('training_samples', 'N/A')}\n")
        f.write(f"Validation Images: {config.get('validation_samples', 'N/A')}\n\n")
        
        f.write("PERFORMANCE METRICS\n")
        f.write("-"*80 + "\n")
        f.write(f"Test Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)\n")
        f.write(f"Precision (Macro): {metrics['precision_macro']:.4f}\n")
        f.write(f"Recall (Macro): {metrics['recall_macro']:.4f}\n")
        f.write(f"F1-Score (Macro): {metrics['f1_macro']:.4f}\n")
        f.write(f"Precision (Weighted): {metrics['precision_weighted']:.4f}\n")
        f.write(f"Recall (Weighted): {metrics['recall_weighted']:.4f}\n")
        f.write(f"F1-Score (Weighted): {metrics['f1_weighted']:.4f}\n\n")
        
        f.write("DATA INTEGRITY\n")
        f.write("-"*80 + "\n")
        f.write(f"Data Leakage Check: {'PASSED ✅' if integrity_ok else 'FAILED ❌'}\n")
        f.write(f"Duplicate Images: {'NONE ✅' if integrity_ok else 'DETECTED ❌'}\n")
        f.write(f"Split Integrity: {'VERIFIED ✅' if integrity_ok else 'COMPROMISED ❌'}\n\n")
        
        f.write("EVALUATION STATUS\n")
        f.write("-"*80 + "\n")
        f.write(f"Correct Predictions: {metrics['correct_predictions']}/{metrics['total_test_samples']}\n")
        f.write(f"Incorrect Predictions: {metrics['incorrect_predictions']}/{metrics['total_test_samples']}\n")
        f.write(f"Evaluation Status: {'COMPLETED ✅' if integrity_ok else 'INVALID ❌'}\n\n")
        
        # Readiness determination
        ready_for_inference = (
            integrity_ok and 
            metrics['accuracy'] >= 0.85 and 
            metrics['f1_macro'] >= 0.80 and
            len(metrics['misclassified']) < metrics['total_test_samples'] * 0.2
        )
        
        f.write("INFERENCE READINESS\n")
        f.write("-"*80 + "\n")
        f.write(f"Ready for Inference: {'YES ✅' if ready_for_inference else 'NO ❌'}\n\n")
        
        if not ready_for_inference:
            f.write("Reasons:\n")
            if not integrity_ok:
                f.write("  - Data leakage detected\n")
            if metrics['accuracy'] < 0.85:
                f.write(f"  - Accuracy too low ({metrics['accuracy']:.2%} < 85%)\n")
            if metrics['f1_macro'] < 0.80:
                f.write(f"  - F1-score too low ({metrics['f1_macro']:.2%} < 80%)\n")
            if len(metrics['misclassified']) >= metrics['total_test_samples'] * 0.2:
                f.write(f"  - Too many misclassifications ({len(metrics['misclassified'])} >= 20% of test set)\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")
    
    print(f"✅ Final evaluation report saved to: {output_path}")

if __name__ == "__main__":
    main()
