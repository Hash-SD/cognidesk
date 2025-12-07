"""
Training module for ATK Classifier.
Handles dataset preparation, model training, and hyperparameter tuning.
"""
import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple, List, Callable
from dataclasses import dataclass, asdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models, optimizers
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    keras = tf.keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    keras = None

try:
    import cv2
    import imghdr
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False


@dataclass
class TrainingConfig:
    """Configuration for model training."""
    img_height: int = 300
    img_width: int = 300
    batch_size: int = 15
    epochs: int = 15
    validation_split: float = 0.1
    learning_rate: float = 0.001
    early_stopping_patience: int = 3
    
    # Model architecture params
    conv1_filters: int = 32
    conv2_filters: int = 64
    conv3_filters: int = 128
    dense_units: int = 128
    dropout_rate: float = 0.5


@dataclass
class TrainingResult:
    """Results from model training."""
    model_path: str
    accuracy: float
    val_accuracy: float
    loss: float
    val_loss: float
    epochs_trained: int
    class_names: List[str]
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    timestamp: str


class DatasetManager:
    """Manages dataset loading and preprocessing."""
    
    VALID_EXTENSIONS = ['jpeg', 'jpg', 'png']
    
    def __init__(self, dataset_dir: str, img_size: Tuple[int, int] = (300, 300)):
        self.dataset_dir = Path(dataset_dir)
        self.img_size = img_size
    
    def validate_and_clean_images(self, progress_callback: Optional[Callable] = None) -> Dict[str, int]:
        """
        Validate images and remove corrupted files.
        
        Returns:
            Dictionary with counts of valid, removed, and total images
        """
        if not CV2_AVAILABLE:
            return {"valid": 0, "removed": 0, "total": 0, "error": "OpenCV not available"}
        
        stats = {"valid": 0, "removed": 0, "total": 0}
        
        if not self.dataset_dir.exists():
            return {"valid": 0, "removed": 0, "total": 0, "error": "Dataset directory not found"}
        
        for class_dir in self.dataset_dir.iterdir():
            if not class_dir.is_dir():
                continue
                
            for image_path in class_dir.iterdir():
                stats["total"] += 1
                try:
                    img = cv2.imread(str(image_path))
                    if img is None:
                        image_path.unlink()
                        stats["removed"] += 1
                        continue
                    
                    tip = imghdr.what(str(image_path))
                    if tip not in self.VALID_EXTENSIONS:
                        image_path.unlink()
                        stats["removed"] += 1
                        continue
                    
                    stats["valid"] += 1
                    
                except Exception:
                    try:
                        image_path.unlink()
                    except:
                        pass
                    stats["removed"] += 1
                
                if progress_callback:
                    progress_callback(stats["total"])
        
        return stats
    
    def load_dataset(self) -> Tuple[Any, Any, List[str]]:
        """
        Load dataset using TensorFlow image_dataset_from_directory.
        
        Returns:
            Tuple of (train_ds, val_ds, class_names)
        """
        if not TENSORFLOW_AVAILABLE:
            raise RuntimeError("TensorFlow not available")
        
        if not self.dataset_dir.exists():
            raise FileNotFoundError(f"Dataset directory not found: {self.dataset_dir}")
        
        # Training set
        train_ds = tf.keras.utils.image_dataset_from_directory(
            str(self.dataset_dir),
            validation_split=0.1,
            subset="training",
            seed=123,
            image_size=self.img_size,
            batch_size=15
        )
        
        # Validation set
        val_ds = tf.keras.utils.image_dataset_from_directory(
            str(self.dataset_dir),
            validation_split=0.1,
            subset="validation",
            seed=123,
            image_size=self.img_size,
            batch_size=15
        )
        
        class_names = train_ds.class_names
        
        # Optimize performance
        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
        
        return train_ds, val_ds, class_names
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about the dataset."""
        info = {
            "exists": self.dataset_dir.exists(),
            "classes": [],
            "total_images": 0,
            "class_counts": {}
        }
        
        if not info["exists"]:
            return info
        
        for class_dir in self.dataset_dir.iterdir():
            if class_dir.is_dir():
                class_name = class_dir.name
                image_count = len(list(class_dir.glob("*")))
                info["classes"].append(class_name)
                info["class_counts"][class_name] = image_count
                info["total_images"] += image_count
        
        return info


class ATKModelTrainer:
    """Handles model building and training."""
    
    def __init__(self, config: Optional[TrainingConfig] = None):
        self.config = config or TrainingConfig()
        self.model = None
        self.history = None
        self.class_names = []
    
    def build_model(self, num_classes: int):
        """
        Build CNN model architecture matching the notebook.
        
        Args:
            num_classes: Number of output classes
            
        Returns:
            Compiled Keras model
        """
        if not TENSORFLOW_AVAILABLE:
            raise RuntimeError("TensorFlow not available")
        
        model = models.Sequential([
            # Rescaling layer (normalization)
            layers.Rescaling(1./255, input_shape=(self.config.img_height, self.config.img_width, 3)),
            
            # Conv Block 1
            layers.Conv2D(self.config.conv1_filters, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            
            # Conv Block 2
            layers.Conv2D(self.config.conv2_filters, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            
            # Conv Block 3
            layers.Conv2D(self.config.conv3_filters, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            
            # Dense layers
            layers.Flatten(),
            layers.Dense(self.config.dense_units, activation='relu'),
            layers.Dropout(self.config.dropout_rate),
            
            # Output
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=optimizers.Adam(learning_rate=self.config.learning_rate),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def train(
        self,
        train_ds,
        val_ds,
        class_names: List[str],
        model_save_path: str = "models/best_model.keras",
        progress_callback: Optional[Callable] = None
    ) -> TrainingResult:
        """
        Train the model.
        
        Args:
            train_ds: Training dataset
            val_ds: Validation dataset
            class_names: List of class names
            model_save_path: Path to save the trained model
            progress_callback: Optional callback for progress updates
            
        Returns:
            TrainingResult with training metrics
        """
        self.class_names = class_names
        num_classes = len(class_names)
        
        # Build model if not already built
        if self.model is None:
            self.build_model(num_classes)
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=self.config.early_stopping_patience,
                restore_best_weights=True
            ),
            ModelCheckpoint(
                model_save_path,
                monitor='val_accuracy',
                save_best_only=True,
                mode='max'
            )
        ]
        
        # Custom callback for progress
        if progress_callback:
            class ProgressCallback(keras.callbacks.Callback):
                def on_epoch_end(self, epoch, logs=None):
                    progress_callback(epoch + 1, logs)
            callbacks.append(ProgressCallback())
        
        # Train
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=self.config.epochs,
            callbacks=callbacks
        )
        
        self.history = history
        
        # Get final metrics
        final_metrics = {
            'accuracy': history.history['accuracy'][-1],
            'val_accuracy': history.history['val_accuracy'][-1],
            'loss': history.history['loss'][-1],
            'val_loss': history.history['val_loss'][-1]
        }
        
        # Save model metadata
        metadata = {
            'class_names': class_names,
            'config': asdict(self.config),
            'final_metrics': final_metrics,
            'timestamp': datetime.now().isoformat()
        }
        
        metadata_path = Path(model_save_path).with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return TrainingResult(
            model_path=model_save_path,
            accuracy=final_metrics['accuracy'],
            val_accuracy=final_metrics['val_accuracy'],
            loss=final_metrics['loss'],
            val_loss=final_metrics['val_loss'],
            epochs_trained=len(history.history['accuracy']),
            class_names=class_names,
            config=asdict(self.config),
            history={k: [float(v) for v in vals] for k, vals in history.history.items()},
            timestamp=datetime.now().isoformat()
        )


def train_model_from_dataset(
    dataset_dir: str = "dataset_alat_tulis",
    model_save_path: str = "models/best_model.keras",
    config: Optional[TrainingConfig] = None,
    progress_callback: Optional[Callable] = None
) -> TrainingResult:
    """
    Complete training pipeline.
    
    Args:
        dataset_dir: Path to dataset directory
        model_save_path: Path to save trained model
        config: Training configuration
        progress_callback: Optional progress callback
        
    Returns:
        TrainingResult with training metrics
    """
    config = config or TrainingConfig()
    
    # Initialize dataset manager
    dataset_manager = DatasetManager(
        dataset_dir,
        img_size=(config.img_height, config.img_width)
    )
    
    # Validate and clean images
    print("Validating images...")
    stats = dataset_manager.validate_and_clean_images()
    print(f"Valid: {stats['valid']}, Removed: {stats['removed']}")
    
    # Load dataset
    print("Loading dataset...")
    train_ds, val_ds, class_names = dataset_manager.load_dataset()
    print(f"Classes: {class_names}")
    
    # Train model
    print("Training model...")
    trainer = ATKModelTrainer(config)
    result = trainer.train(
        train_ds,
        val_ds,
        class_names,
        model_save_path,
        progress_callback
    )
    
    print(f"Training complete! Accuracy: {result.accuracy:.4f}, Val Accuracy: {result.val_accuracy:.4f}")
    
    return result


if __name__ == "__main__":
    # Run training from command line
    result = train_model_from_dataset()
    print(f"\nModel saved to: {result.model_path}")
    print(f"Final accuracy: {result.accuracy:.4f}")
    print(f"Final val_accuracy: {result.val_accuracy:.4f}")
