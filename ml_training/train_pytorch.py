"""
ML Model Training Script (PyTorch Version)
Trains a CNN classifier for leaf classification using transfer learning
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import os
import json
import argparse
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from datetime import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm

from config.dataset_config import (
    DATASET_PROCESSED_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    IMAGE_SIZE,
    BATCH_SIZE,
    EPOCHS,
    LEARNING_RATE,
    FINE_TUNE_LEARNING_RATE,
    RANDOM_SEED,
    CLASS_MAPPING_FILE,
)


class LeafClassifierTrainer:
    """
    Trainer for leaf classification model using transfer learning with PyTorch
    """
    
    def __init__(self, 
                 data_dir=DATASET_PROCESSED_DIR,
                 model_type='mobilenet_v2',
                 image_size=IMAGE_SIZE,
                 batch_size=BATCH_SIZE,
                 epochs=EPOCHS,
                 learning_rate=LEARNING_RATE,
                 fine_tune_lr=FINE_TUNE_LEARNING_RATE,
                 random_seed=RANDOM_SEED,
                 verbose=True):
        """
        Initialize trainer
        
        Args:
            data_dir: Directory with train/val/test splits
            model_type: 'mobilenet_v2', 'resnet50', or 'efficientnet_b0'
            image_size: Input image size tuple
            batch_size: Training batch size
            epochs: Number of training epochs
            learning_rate: Initial learning rate
            fine_tune_lr: Learning rate for fine-tuning
            random_seed: Random seed for reproducibility
            verbose: Print training progress
        """
        self.data_dir = Path(data_dir)
        self.model_type = model_type
        self.image_size = image_size
        self.batch_size = batch_size
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.fine_tune_lr = fine_tune_lr
        self.random_seed = random_seed
        self.verbose = verbose
        
        # Device configuration
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if self.verbose:
            print(f"Using device: {self.device}")
        
        # Set random seeds for reproducibility
        self._set_seeds()
        
        # Paths
        self.train_dir = self.data_dir / 'train'
        self.val_dir = self.data_dir / 'val'
        self.test_dir = self.data_dir / 'test'
        
        # Load class mapping
        self.class_mapping = self._load_class_mapping()
        self.num_classes = self.class_mapping['num_classes']
        
        # Model and history
        self.model = None
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': [],
            'lr': []
        }
        
        # Output paths
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_dir = MODELS_DIR / f"training_{timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Best model tracking
        self.best_val_acc = 0.0
    
    def _set_seeds(self):
        """Set random seeds for reproducibility"""
        np.random.seed(self.random_seed)
        torch.manual_seed(self.random_seed)
        torch.cuda.manual_seed_all(self.random_seed)
        os.environ['PYTHONHASHSEED'] = str(self.random_seed)
        # Make PyTorch operations deterministic
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    
    def _load_class_mapping(self):
        """Load class mapping from file"""
        with open(CLASS_MAPPING_FILE, 'r') as f:
            return json.load(f)
    
    def create_data_loaders(self):
        """Create data loaders for training, validation and test"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("CREATING DATA LOADERS")
            print(f"{'='*80}")
        
        # Data augmentation for training
        train_transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.RandomRotation(20),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.RandomAffine(degrees=0, translate=(0.2, 0.2), scale=(0.8, 1.2)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # No augmentation for validation and test
        val_test_transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Create datasets
        train_dataset = datasets.ImageFolder(self.train_dir, transform=train_transform)
        val_dataset = datasets.ImageFolder(self.val_dir, transform=val_test_transform)
        test_dataset = datasets.ImageFolder(self.test_dir, transform=val_test_transform)
        
        # Create data loaders
        self.train_loader = DataLoader(
            train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=4,
            pin_memory=True if torch.cuda.is_available() else False
        )
        
        self.val_loader = DataLoader(
            val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=4,
            pin_memory=True if torch.cuda.is_available() else False
        )
        
        self.test_loader = DataLoader(
            test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=4,
            pin_memory=True if torch.cuda.is_available() else False
        )
        
        if self.verbose:
            print(f"Training samples: {len(train_dataset)}")
            print(f"Validation samples: {len(val_dataset)}")
            print(f"Test samples: {len(test_dataset)}")
            print(f"Number of classes: {self.num_classes}")
            print(f"Classes: {train_dataset.classes}")
    
    def build_model(self):
        """Build transfer learning model"""
        if self.verbose:
            print(f"\n{'='*80}")
            print(f"BUILDING MODEL: {self.model_type}")
            print(f"{'='*80}")
        
        # Select base model
        if self.model_type == 'mobilenet_v2':
            base_model = models.mobilenet_v2(weights='DEFAULT')
            num_features = base_model.classifier[1].in_features
            # Replace classifier
            base_model.classifier = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_features, 256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(128, self.num_classes)
            )
            self.model = base_model
            
        elif self.model_type == 'resnet50':
            base_model = models.resnet50(weights='DEFAULT')
            num_features = base_model.fc.in_features
            # Replace final layer
            base_model.fc = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_features, 512),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(512, 256),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(256, self.num_classes)
            )
            self.model = base_model
            
        elif self.model_type == 'efficientnet_b0':
            base_model = models.efficientnet_b0(weights='DEFAULT')
            num_features = base_model.classifier[1].in_features
            # Replace classifier
            base_model.classifier = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_features, 256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(128, self.num_classes)
            )
            self.model = base_model
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        # Move model to device
        self.model = self.model.to(self.device)
        
        # Freeze base layers initially
        self._freeze_base_layers()
        
        if self.verbose:
            total_params = sum(p.numel() for p in self.model.parameters())
            trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            print(f"\nModel architecture:")
            print(f"  Base model: {self.model_type}")
            print(f"  Input shape: {(*self.image_size, 3)}")
            print(f"  Number of classes: {self.num_classes}")
            print(f"  Total parameters: {total_params:,}")
            print(f"  Trainable parameters: {trainable_params:,}")
    
    def _freeze_base_layers(self):
        """Freeze base model layers for initial training"""
        if self.model_type == 'mobilenet_v2':
            # Freeze all features
            for param in self.model.features.parameters():
                param.requires_grad = False
        elif self.model_type == 'resnet50':
            # Freeze all layers except fc
            for name, param in self.model.named_parameters():
                if 'fc' not in name:
                    param.requires_grad = False
        elif self.model_type == 'efficientnet_b0':
            # Freeze all features
            for param in self.model.features.parameters():
                param.requires_grad = False
    
    def _unfreeze_base_layers(self, unfreeze_percentage=0.3):
        """Unfreeze later layers of base model for fine-tuning"""
        if self.model_type == 'mobilenet_v2':
            # Unfreeze later 30% of feature layers
            total_layers = len(list(self.model.features.parameters()))
            unfreeze_from = int(total_layers * (1 - unfreeze_percentage))
            for i, param in enumerate(self.model.features.parameters()):
                if i >= unfreeze_from:
                    param.requires_grad = True
        elif self.model_type == 'resnet50':
            # Unfreeze layer4 and fc
            for name, param in self.model.named_parameters():
                if 'layer4' in name or 'fc' in name:
                    param.requires_grad = True
        elif self.model_type == 'efficientnet_b0':
            # Unfreeze later 30% of feature layers
            total_layers = len(list(self.model.features.parameters()))
            unfreeze_from = int(total_layers * (1 - unfreeze_percentage))
            for i, param in enumerate(self.model.features.parameters()):
                if i >= unfreeze_from:
                    param.requires_grad = True
    
    def train_epoch(self, epoch, criterion, optimizer):
        """Train for one epoch"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(self.train_loader, desc=f'Epoch {epoch+1}/{self.epochs}', disable=not self.verbose)
        
        for inputs, labels in pbar:
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)
            
            # Zero gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = self.model(inputs)
            loss = criterion(outputs, labels)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            # Statistics
            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            # Update progress bar
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100 * correct / total:.2f}%'
            })
        
        epoch_loss = running_loss / total
        epoch_acc = correct / total
        
        return epoch_loss, epoch_acc
    
    def validate(self, criterion):
        """Validate the model"""
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for inputs, labels in self.val_loader:
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                
                running_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        epoch_loss = running_loss / total
        epoch_acc = correct / total
        
        return epoch_loss, epoch_acc
    
    def train(self):
        """Train the model"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("TRAINING MODEL")
            print(f"{'='*80}")
            print(f"Phase 1: Training top layers with frozen base")
            print(f"Epochs: {self.epochs}")
            print(f"Learning rate: {self.learning_rate}")
        
        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        # Learning rate scheduler
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=5
        )
        
        # Early stopping
        patience = 10
        patience_counter = 0
        best_val_loss = float('inf')
        
        # Training loop
        for epoch in range(self.epochs):
            # Train
            train_loss, train_acc = self.train_epoch(epoch, criterion, optimizer)
            
            # Validate
            val_loss, val_acc = self.validate(criterion)
            
            # Get current learning rate
            current_lr = optimizer.param_groups[0]['lr']
            
            # Update history
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
            self.history['lr'].append(current_lr)
            
            # Print epoch results
            if self.verbose:
                print(f"Epoch {epoch+1}/{self.epochs}")
                print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
                print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
                print(f"  LR: {current_lr:.6f}")
            
            # Save best model
            if val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                best_model_path = self.output_dir / 'best_model.pth'
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_acc': val_acc,
                    'val_loss': val_loss,
                }, best_model_path)
                if self.verbose:
                    print(f"  ✓ Saved best model (val_acc: {val_acc:.4f})")
            
            # Learning rate scheduling
            scheduler.step(val_loss)
            
            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    if self.verbose:
                        print(f"  Early stopping triggered after {epoch+1} epochs")
                    break
        
        if self.verbose:
            print(f"\n✓ Training complete!")
            print(f"  Best validation accuracy: {self.best_val_acc:.4f}")
    
    def fine_tune(self, fine_tune_epochs=20):
        """Fine-tune the model by unfreezing base layers"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("FINE-TUNING MODEL")
            print(f"{'='*80}")
            print(f"Phase 2: Fine-tuning with unfrozen base layers")
            print(f"Epochs: {fine_tune_epochs}")
            print(f"Learning rate: {self.fine_tune_lr}")
        
        # Load best model from phase 1
        best_model_path = self.output_dir / 'best_model.pth'
        checkpoint = torch.load(best_model_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        
        # Unfreeze base layers
        self._unfreeze_base_layers()
        
        if self.verbose:
            trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            print(f"  Trainable parameters: {trainable_params:,}")
        
        # Loss and optimizer with lower learning rate
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.fine_tune_lr)
        
        # Learning rate scheduler
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=3
        )
        
        # Early stopping
        patience = 7
        patience_counter = 0
        best_val_loss = float('inf')
        
        # Fine-tuning loop
        for epoch in range(fine_tune_epochs):
            # Train
            train_loss, train_acc = self.train_epoch(epoch, criterion, optimizer)
            
            # Validate
            val_loss, val_acc = self.validate(criterion)
            
            # Get current learning rate
            current_lr = optimizer.param_groups[0]['lr']
            
            # Update history
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
            self.history['lr'].append(current_lr)
            
            # Print epoch results
            if self.verbose:
                print(f"Fine-tune Epoch {epoch+1}/{fine_tune_epochs}")
                print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
                print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
                print(f"  LR: {current_lr:.6f}")
            
            # Save best model
            if val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_acc': val_acc,
                    'val_loss': val_loss,
                }, best_model_path)
                if self.verbose:
                    print(f"  ✓ Saved best model (val_acc: {val_acc:.4f})")
            
            # Learning rate scheduling
            scheduler.step(val_loss)
            
            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    if self.verbose:
                        print(f"  Early stopping triggered after {epoch+1} fine-tune epochs")
                    break
        
        if self.verbose:
            print(f"\n✓ Fine-tuning complete!")
            print(f"  Best validation accuracy: {self.best_val_acc:.4f}")
    
    def evaluate(self):
        """Evaluate model on test set"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("EVALUATING MODEL")
            print(f"{'='*80}")
        
        # Load best model
        best_model_path = self.output_dir / 'best_model.pth'
        checkpoint = torch.load(best_model_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        
        self.model.eval()
        correct = 0
        total = 0
        running_loss = 0.0
        criterion = nn.CrossEntropyLoss()
        
        with torch.no_grad():
            for inputs, labels in self.test_loader:
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                
                running_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        test_loss = running_loss / total
        test_acc = correct / total
        
        if self.verbose:
            print(f"\nTest Results:")
            print(f"  Loss: {test_loss:.4f}")
            print(f"  Accuracy: {test_acc:.4f} ({100 * test_acc:.2f}%)")
        
        # Save results
        test_results = {
            'test_loss': float(test_loss),
            'test_accuracy': float(test_acc),
            'test_samples': total
        }
        
        results_path = self.output_dir / 'test_results.json'
        with open(results_path, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        return test_results
    
    def plot_training_history(self):
        """Plot and save training history"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("PLOTTING TRAINING HISTORY")
            print(f"{'='*80}")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        epochs_range = range(1, len(self.history['train_loss']) + 1)
        
        # Plot accuracy
        axes[0, 0].plot(epochs_range, self.history['train_acc'], label='Train Accuracy')
        axes[0, 0].plot(epochs_range, self.history['val_acc'], label='Val Accuracy')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Plot loss
        axes[0, 1].plot(epochs_range, self.history['train_loss'], label='Train Loss')
        axes[0, 1].plot(epochs_range, self.history['val_loss'], label='Val Loss')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Plot learning rate
        axes[1, 0].plot(epochs_range, self.history['lr'])
        axes[1, 0].set_title('Learning Rate')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Learning Rate')
        axes[1, 0].set_yscale('log')
        axes[1, 0].grid(True)
        
        # Hide unused subplot
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.output_dir / 'training_history.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        
        if self.verbose:
            print(f"  Training history plot saved to: {plot_path}")
        
        plt.close()
    
    def save_model_and_config(self):
        """Save final model and configuration"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("SAVING MODEL AND CONFIGURATION")
            print(f"{'='*80}")
        
        # Save final model
        final_model_path = self.output_dir / 'final_model.pth'
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'model_type': self.model_type,
            'num_classes': self.num_classes,
            'image_size': self.image_size,
        }, final_model_path)
        
        if self.verbose:
            print(f"  Final model saved to: {final_model_path}")
        
        # Save model configuration
        config = {
            'model_type': self.model_type,
            'image_size': list(self.image_size),
            'num_classes': self.num_classes,
            'classes': self.class_mapping['classes'],
            'class_to_idx': self.class_mapping['class_to_idx'],
            'idx_to_class': self.class_mapping['idx_to_class'],
            'batch_size': self.batch_size,
            'epochs_trained': len(self.history['train_loss']),
            'random_seed': self.random_seed,
            'training_date': datetime.now().isoformat(),
            'best_val_accuracy': float(self.best_val_acc),
            'framework': 'pytorch'
        }
        
        config_path = self.output_dir / 'model_config.json'
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        if self.verbose:
            print(f"  Model configuration saved to: {config_path}")
    
    def generate_summary_report(self, test_results):
        """Generate final training summary report"""
        report_path = self.output_dir / 'training_summary.txt'
        
        with open(report_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("TRAINING SUMMARY REPORT (PyTorch)\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model Type: {self.model_type}\n")
            f.write(f"Number of Classes: {self.num_classes}\n")
            f.write(f"Image Size: {self.image_size}\n")
            f.write(f"Batch Size: {self.batch_size}\n")
            f.write(f"Epochs Trained: {len(self.history['train_loss'])}\n")
            f.write(f"Random Seed: {self.random_seed}\n")
            f.write(f"Device: {self.device}\n\n")
            
            f.write("-"*80 + "\n")
            f.write("DATASET SIZES\n")
            f.write("-"*80 + "\n")
            f.write(f"Training samples: {len(self.train_loader.dataset)}\n")
            f.write(f"Validation samples: {len(self.val_loader.dataset)}\n")
            f.write(f"Test samples: {test_results['test_samples']}\n\n")
            
            f.write("-"*80 + "\n")
            f.write("BEST VALIDATION PERFORMANCE\n")
            f.write("-"*80 + "\n")
            f.write(f"Best Val Accuracy: {self.best_val_acc:.4f}\n")
            f.write(f"Best Val Loss: {min(self.history['val_loss']):.4f}\n\n")
            
            f.write("-"*80 + "\n")
            f.write("TEST SET PERFORMANCE\n")
            f.write("-"*80 + "\n")
            f.write(f"Test Accuracy: {test_results['test_accuracy']:.4f} ({100*test_results['test_accuracy']:.2f}%)\n")
            f.write(f"Test Loss: {test_results['test_loss']:.4f}\n\n")
            
            f.write("-"*80 + "\n")
            f.write("CLASS MAPPING\n")
            f.write("-"*80 + "\n")
            for idx, class_name in self.class_mapping['idx_to_class'].items():
                f.write(f"  {idx}: {class_name}\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("OUTPUT FILES\n")
            f.write("="*80 + "\n")
            f.write(f"  Best model: {self.output_dir / 'best_model.pth'}\n")
            f.write(f"  Final model: {self.output_dir / 'final_model.pth'}\n")
            f.write(f"  Configuration: {self.output_dir / 'model_config.json'}\n")
            f.write(f"  Training plot: {self.output_dir / 'training_history.png'}\n")
            f.write(f"  Test results: {self.output_dir / 'test_results.json'}\n")
        
        if self.verbose:
            print(f"\n  Training summary saved to: {report_path}")
    
    def run_complete_training(self, fine_tune=True, fine_tune_epochs=20):
        """Run complete training pipeline"""
        print("\n" + "="*80)
        print(" LEAF CLASSIFICATION MODEL TRAINING (PyTorch)")
        print("="*80)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        # 1. Create data loaders
        self.create_data_loaders()
        
        # 2. Build model
        self.build_model()
        
        # 3. Train model
        self.train()
        
        # 4. Fine-tune (optional)
        if fine_tune:
            self.fine_tune(fine_tune_epochs)
        
        # 5. Evaluate on test set
        test_results = self.evaluate()
        
        # 6. Plot training history
        self.plot_training_history()
        
        # 7. Save model and configuration
        self.save_model_and_config()
        
        # 8. Generate summary report
        self.generate_summary_report(test_results)
        
        print("\n" + "="*80)
        print(" TRAINING COMPLETE")
        print("="*80)
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nBest validation accuracy: {self.best_val_acc:.4f}")
        print(f"Test accuracy: {test_results['test_accuracy']:.4f}")
        print(f"\nOutput directory: {self.output_dir}")
        print("="*80 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Train leaf classification model with PyTorch",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--model',
        type=str,
        choices=['mobilenet_v2', 'resnet50', 'efficientnet_b0'],
        default='mobilenet_v2',
        help='Model architecture (default: mobilenet_v2)'
    )
    
    parser.add_argument(
        '--epochs',
        type=int,
        default=EPOCHS,
        help=f'Number of training epochs (default: {EPOCHS})'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=BATCH_SIZE,
        help=f'Batch size (default: {BATCH_SIZE})'
    )
    
    parser.add_argument(
        '--lr',
        type=float,
        default=LEARNING_RATE,
        help=f'Learning rate (default: {LEARNING_RATE})'
    )
    
    parser.add_argument(
        '--no-fine-tune',
        action='store_true',
        help='Skip fine-tuning phase'
    )
    
    parser.add_argument(
        '--fine-tune-epochs',
        type=int,
        default=20,
        help='Number of fine-tuning epochs (default: 20)'
    )
    
    args = parser.parse_args()
    
    try:
        # Create trainer
        trainer = LeafClassifierTrainer(
            model_type=args.model,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.lr,
            verbose=True
        )
        
        # Run training
        trainer.run_complete_training(
            fine_tune=not args.no_fine_tune,
            fine_tune_epochs=args.fine_tune_epochs
        )
        
        return 0
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
