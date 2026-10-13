"""
ML Model Training Script
Trains a CNN classifier for leaf classification using transfer learning
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import os
import json
import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2, EfficientNetB0
from tensorflow.keras.callbacks import (
    ModelCheckpoint, 
    EarlyStopping, 
    ReduceLROnPlateau,
    CSVLogger,
    TensorBoard
)
from datetime import datetime
import matplotlib.pyplot as plt

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
    Trainer for leaf classification model using transfer learning
    """
    
    def __init__(self, 
                 data_dir=DATASET_PROCESSED_DIR,
                 model_type='MobileNetV2',
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
            model_type: 'MobileNetV2' or 'EfficientNetB0'
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
        self.history = None
        
        # Output paths
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_dir = MODELS_DIR / f"training_{timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _set_seeds(self):
        """Set random seeds for reproducibility"""
        np.random.seed(self.random_seed)
        tf.random.set_seed(self.random_seed)
        os.environ['PYTHONHASHSEED'] = str(self.random_seed)
    
    def _load_class_mapping(self):
        """Load class mapping from file"""
        with open(CLASS_MAPPING_FILE, 'r') as f:
            return json.load(f)
    
    def create_data_generators(self):
        """Create data generators for training and validation"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("CREATING DATA GENERATORS")
            print(f"{'='*80}")
        
        # Training data generator with augmentation
        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            fill_mode='nearest',
            brightness_range=[0.8, 1.2]
        )
        
        # Validation data generator (no augmentation)
        val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255
        )
        
        # Create generators
        self.train_generator = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=True,
            seed=self.random_seed
        )
        
        self.val_generator = val_datagen.flow_from_directory(
            self.val_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False,
            seed=self.random_seed
        )
        
        if self.verbose:
            print(f"Training samples: {self.train_generator.samples}")
            print(f"Validation samples: {self.val_generator.samples}")
            print(f"Number of classes: {self.num_classes}")
            print(f"Classes: {self.train_generator.class_indices}")
    
    def build_model(self):
        """Build transfer learning model"""
        if self.verbose:
            print(f"\n{'='*80}")
            print(f"BUILDING MODEL: {self.model_type}")
            print(f"{'='*80}")
        
        # Select base model
        if self.model_type == 'MobileNetV2':
            base_model = MobileNetV2(
                input_shape=(*self.image_size, 3),
                include_top=False,
                weights='imagenet'
            )
        elif self.model_type == 'EfficientNetB0':
            base_model = EfficientNetB0(
                input_shape=(*self.image_size, 3),
                include_top=False,
                weights='imagenet'
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        # Freeze base model initially
        base_model.trainable = False
        
        # Build full model
        inputs = keras.Input(shape=(*self.image_size, 3))
        
        # Preprocessing
        x = inputs
        
        # Base model
        x = base_model(x, training=False)
        
        # Classification head
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        
        # Output layer
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        # Create model
        self.model = models.Model(inputs, outputs)
        
        # Compile model
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=2, name='top_2_accuracy')]
        )
        
        if self.verbose:
            print(f"\nModel architecture:")
            print(f"  Base model: {self.model_type}")
            print(f"  Input shape: {(*self.image_size, 3)}")
            print(f"  Number of classes: {self.num_classes}")
            print(f"  Total parameters: {self.model.count_params():,}")
            print(f"  Trainable parameters: {sum([tf.size(w).numpy() for w in self.model.trainable_weights]):,}")
    
    def create_callbacks(self):
        """Create training callbacks"""
        callbacks = []
        
        # Model checkpoint - save best model
        checkpoint_path = self.output_dir / 'best_model.keras'
        callbacks.append(ModelCheckpoint(
            filepath=str(checkpoint_path),
            monitor='val_accuracy',
            mode='max',
            save_best_only=True,
            verbose=1
        ))
        
        # Early stopping
        callbacks.append(EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ))
        
        # Reduce learning rate on plateau
        callbacks.append(ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ))
        
        # CSV logger
        csv_path = self.output_dir / 'training_log.csv'
        callbacks.append(CSVLogger(str(csv_path)))
        
        # TensorBoard
        tensorboard_path = self.output_dir / 'tensorboard'
        callbacks.append(TensorBoard(
            log_dir=str(tensorboard_path),
            histogram_freq=1
        ))
        
        return callbacks
    
    def train(self):
        """Train the model"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("TRAINING MODEL")
            print(f"{'='*80}")
            print(f"Phase 1: Training top layers with frozen base")
            print(f"Epochs: {self.epochs}")
            print(f"Learning rate: {self.learning_rate}")
        
        # Create callbacks
        callbacks = self.create_callbacks()
        
        # Calculate steps
        steps_per_epoch = self.train_generator.samples // self.batch_size
        validation_steps = self.val_generator.samples // self.batch_size
        
        # Train model
        self.history = self.model.fit(
            self.train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=self.epochs,
            validation_data=self.val_generator,
            validation_steps=validation_steps,
            callbacks=callbacks,
            verbose=1 if self.verbose else 0
        )
        
        if self.verbose:
            print(f"\n✓ Training complete!")
    
    def fine_tune(self, fine_tune_epochs=20):
        """Fine-tune the model by unfreezing base layers"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("FINE-TUNING MODEL")
            print(f"{'='*80}")
            print(f"Phase 2: Fine-tuning with unfrozen base layers")
            print(f"Epochs: {fine_tune_epochs}")
            print(f"Learning rate: {self.fine_tune_lr}")
        
        # Unfreeze base model
        self.model.layers[1].trainable = True
        
        # Freeze early layers, unfreeze later layers
        for layer in self.model.layers[1].layers[:100]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.fine_tune_lr),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=2, name='top_2_accuracy')]
        )
        
        if self.verbose:
            print(f"  Trainable parameters: {sum([tf.size(w).numpy() for w in self.model.trainable_weights]):,}")
        
        # Create callbacks
        callbacks = self.create_callbacks()
        
        # Calculate steps
        steps_per_epoch = self.train_generator.samples // self.batch_size
        validation_steps = self.val_generator.samples // self.batch_size
        
        # Continue training
        history_fine = self.model.fit(
            self.train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=fine_tune_epochs,
            validation_data=self.val_generator,
            validation_steps=validation_steps,
            callbacks=callbacks,
            verbose=1 if self.verbose else 0
        )
        
        # Combine histories
        for key in self.history.history.keys():
            self.history.history[key].extend(history_fine.history[key])
        
        if self.verbose:
            print(f"\n✓ Fine-tuning complete!")
    
    def evaluate(self):
        """Evaluate model on test set"""
        if self.verbose:
            print(f"\n{'='*80}")
            print("EVALUATING MODEL")
            print(f"{'='*80}")
        
        # Create test generator
        test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
        test_generator = test_datagen.flow_from_directory(
            self.test_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        # Evaluate
        results = self.model.evaluate(test_generator, verbose=1 if self.verbose else 0)
        
        # Print results
        if self.verbose:
            print(f"\nTest Results:")
            print(f"  Loss: {results[0]:.4f}")
            print(f"  Accuracy: {results[1]:.4f}")
            print(f"  Top-2 Accuracy: {results[2]:.4f}")
        
        # Save results
        test_results = {
            'test_loss': float(results[0]),
            'test_accuracy': float(results[1]),
            'test_top_2_accuracy': float(results[2]),
            'test_samples': test_generator.samples
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
        
        # Plot accuracy
        axes[0, 0].plot(self.history.history['accuracy'], label='Train Accuracy')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Val Accuracy')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Plot loss
        axes[0, 1].plot(self.history.history['loss'], label='Train Loss')
        axes[0, 1].plot(self.history.history['val_loss'], label='Val Loss')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Plot top-2 accuracy
        axes[1, 0].plot(self.history.history['top_2_accuracy'], label='Train Top-2')
        axes[1, 0].plot(self.history.history['val_top_2_accuracy'], label='Val Top-2')
        axes[1, 0].set_title('Top-2 Accuracy')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Top-2 Accuracy')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Plot learning rate (if available)
        if 'lr' in self.history.history:
            axes[1, 1].plot(self.history.history['lr'])
            axes[1, 1].set_title('Learning Rate')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Learning Rate')
            axes[1, 1].set_yscale('log')
            axes[1, 1].grid(True)
        else:
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
        final_model_path = self.output_dir / 'final_model.keras'
        self.model.save(final_model_path)
        
        if self.verbose:
            print(f"  Final model saved to: {final_model_path}")
        
        # Save model configuration
        config = {
            'model_type': self.model_type,
            'image_size': self.image_size,
            'num_classes': self.num_classes,
            'classes': self.class_mapping['classes'],
            'class_to_idx': self.class_mapping['class_to_idx'],
            'idx_to_class': self.class_mapping['idx_to_class'],
            'batch_size': self.batch_size,
            'epochs_trained': len(self.history.history['loss']),
            'random_seed': self.random_seed,
            'training_date': datetime.now().isoformat(),
            'best_val_accuracy': float(max(self.history.history['val_accuracy'])),
            'best_val_loss': float(min(self.history.history['val_loss'])),
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
            f.write("TRAINING SUMMARY REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model Type: {self.model_type}\n")
            f.write(f"Number of Classes: {self.num_classes}\n")
            f.write(f"Image Size: {self.image_size}\n")
            f.write(f"Batch Size: {self.batch_size}\n")
            f.write(f"Epochs Trained: {len(self.history.history['loss'])}\n")
            f.write(f"Random Seed: {self.random_seed}\n\n")
            
            f.write("-"*80 + "\n")
            f.write("DATASET SIZES\n")
            f.write("-"*80 + "\n")
            f.write(f"Training samples: {self.train_generator.samples}\n")
            f.write(f"Validation samples: {self.val_generator.samples}\n")
            f.write(f"Test samples: {test_results['test_samples']}\n\n")
            
            f.write("-"*80 + "\n")
            f.write("BEST VALIDATION PERFORMANCE\n")
            f.write("-"*80 + "\n")
            f.write(f"Best Val Accuracy: {max(self.history.history['val_accuracy']):.4f}\n")
            f.write(f"Best Val Loss: {min(self.history.history['val_loss']):.4f}\n")
            f.write(f"Best Val Top-2 Accuracy: {max(self.history.history['val_top_2_accuracy']):.4f}\n\n")
            
            f.write("-"*80 + "\n")
            f.write("TEST SET PERFORMANCE\n")
            f.write("-"*80 + "\n")
            f.write(f"Test Accuracy: {test_results['test_accuracy']:.4f}\n")
            f.write(f"Test Loss: {test_results['test_loss']:.4f}\n")
            f.write(f"Test Top-2 Accuracy: {test_results['test_top_2_accuracy']:.4f}\n\n")
            
            f.write("-"*80 + "\n")
            f.write("CLASS MAPPING\n")
            f.write("-"*80 + "\n")
            for idx, class_name in self.class_mapping['idx_to_class'].items():
                f.write(f"  {idx}: {class_name}\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("OUTPUT FILES\n")
            f.write("="*80 + "\n")
            f.write(f"  Best model: {self.output_dir / 'best_model.keras'}\n")
            f.write(f"  Final model: {self.output_dir / 'final_model.keras'}\n")
            f.write(f"  Configuration: {self.output_dir / 'model_config.json'}\n")
            f.write(f"  Training log: {self.output_dir / 'training_log.csv'}\n")
            f.write(f"  Training plot: {self.output_dir / 'training_history.png'}\n")
            f.write(f"  Test results: {self.output_dir / 'test_results.json'}\n")
        
        if self.verbose:
            print(f"\n  Training summary saved to: {report_path}")
    
    def run_complete_training(self, fine_tune=True, fine_tune_epochs=20):
        """Run complete training pipeline"""
        print("\n" + "="*80)
        print(" LEAF CLASSIFICATION MODEL TRAINING")
        print("="*80)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        # 1. Create data generators
        self.create_data_generators()
        
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
        print(f"\nBest validation accuracy: {max(self.history.history['val_accuracy']):.4f}")
        print(f"Test accuracy: {test_results['test_accuracy']:.4f}")
        print(f"\nOutput directory: {self.output_dir}")
        print("="*80 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Train leaf classification model",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--model',
        type=str,
        choices=['MobileNetV2', 'EfficientNetB0'],
        default='MobileNetV2',
        help='Model architecture (default: MobileNetV2)'
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
