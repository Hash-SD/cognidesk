"""
CNN Model module for ATK Classifier.
Contains model architecture and prediction functionality.
"""
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
import random
import json

import numpy as np

# Try to import TensorFlow/Keras, but allow demo mode without it
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, optimizers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False


@dataclass
class PredictionResult:
    """Data class for prediction results."""
    predicted_class: str
    confidence: float
    percentage: float
    top_predictions: List[Dict[str, Any]]
    is_demo: bool
    is_low_confidence: bool


class ATKClassifier:
    """CNN model architecture for ATK classification."""
    
    @staticmethod
    def build_model(
        input_shape: tuple = (300, 300, 3), 
        num_classes: int = 3,
        conv1_filters: int = 32,
        conv2_filters: int = 64,
        conv3_filters: int = 128,
        dense_units: int = 128,
        dropout_rate: float = 0.5,
        learning_rate: float = 0.001
    ) -> Any:
        """
        Build CNN model architecture for ATK classification.
        Architecture matches the notebook training code.
        
        Args:
            input_shape: Input image shape (height, width, channels)
            num_classes: Number of output classes
            conv1_filters: Filters in first conv layer
            conv2_filters: Filters in second conv layer
            conv3_filters: Filters in third conv layer
            dense_units: Units in dense layer
            dropout_rate: Dropout rate
            learning_rate: Learning rate for optimizer
            
        Returns:
            Compiled Keras model
        """
        if not TENSORFLOW_AVAILABLE:
            raise RuntimeError("TensorFlow is not available. Cannot build model.")

        model = models.Sequential([
            # Rescaling layer - normalizes pixels to [0, 1]
            layers.Rescaling(1./255, input_shape=input_shape),
            
            # Conv Block 1
            layers.Conv2D(conv1_filters, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            
            # Conv Block 2
            layers.Conv2D(conv2_filters, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            
            # Conv Block 3
            layers.Conv2D(conv3_filters, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            
            # Dense layers
            layers.Flatten(),
            layers.Dense(dense_units, activation='relu'),
            layers.Dropout(dropout_rate),
            
            # Output
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=optimizers.Adam(learning_rate=learning_rate),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
            metrics=['accuracy']
        )
        
        return model


class ModelPredictor:
    """Handles model loading and prediction."""
    
    # Default class names for ATK
    DEFAULT_CLASS_NAMES = [
        "eraser", "kertas", "pensil"
    ]
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        class_names: Optional[List[str]] = None,
        low_confidence_threshold: float = 0.5
    ):
        """
        Initialize predictor with optional model path.
        
        Args:
            model_path: Path to saved model file (.keras or .h5)
            class_names: List of class names for predictions
            low_confidence_threshold: Threshold below which confidence is considered low
        """
        self.model_path = Path(model_path) if model_path else None
        self.class_names = class_names or self.DEFAULT_CLASS_NAMES
        self.low_confidence_threshold = low_confidence_threshold
        self._model = None
        self._demo_mode = False
        self._model_metadata = None
        
        # Try to load model
        self._load_model()
    
    def _load_model(self) -> None:
        """Attempt to load the model from disk."""
        if not TENSORFLOW_AVAILABLE:
            self._demo_mode = True
            return
            
        if self.model_path and self.model_path.exists():
            try:
                self._model = keras.models.load_model(str(self.model_path))
                self._demo_mode = False
                
                # Try to load metadata for class names
                metadata_path = self.model_path.with_suffix('.json')
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        self._model_metadata = json.load(f)
                        if 'class_names' in self._model_metadata:
                            self.class_names = self._model_metadata['class_names']
                            
            except Exception as e:
                print(f"Error loading model: {e}")
                self._demo_mode = True
        else:
            self._demo_mode = True
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if self._demo_mode:
            return {"mode": "demo", "model_loaded": False}
        
        info = {
            "mode": "production",
            "model_loaded": True,
            "model_path": str(self.model_path),
            "class_names": self.class_names,
            "num_classes": len(self.class_names)
        }
        
        if self._model_metadata:
            info["metadata"] = self._model_metadata
        
        return info
    
    def is_demo_mode(self) -> bool:
        """
        Check if predictor is running in demo mode.
        
        Returns:
            True if in demo mode (no real model), False otherwise
        """
        return self._demo_mode
    
    def _generate_demo_predictions(self, top_k: int = 3) -> np.ndarray:
        """
        Generate simulated predictions for demo mode.
        
        Args:
            top_k: Number of top predictions to emphasize
            
        Returns:
            Simulated probability array
        """
        # Generate random probabilities
        probs = np.random.dirichlet(np.ones(len(self.class_names)))
        return probs
    
    def predict(self, preprocessed_image: np.ndarray, top_k: int = 3) -> PredictionResult:
        """
        Make prediction on preprocessed image.
        
        Args:
            preprocessed_image: Preprocessed image array with shape (1, 224, 224, 3)
            top_k: Number of top predictions to return
            
        Returns:
            PredictionResult with predicted class, confidence, and top-k predictions
        """
        if self._demo_mode:
            probabilities = self._generate_demo_predictions(top_k)
        else:
            probabilities = self._model.predict(preprocessed_image, verbose=0)[0]
        
        # Get top-k indices sorted by probability (descending)
        top_indices = np.argsort(probabilities)[::-1][:top_k]
        
        # Build top predictions list
        top_predictions = []
        for idx in top_indices:
            top_predictions.append({
                "class": self.class_names[idx],
                "confidence": float(probabilities[idx]),
                "percentage": float(probabilities[idx] * 100)
            })
        
        # Get best prediction
        best_idx = top_indices[0]
        best_confidence = float(probabilities[best_idx])
        
        return PredictionResult(
            predicted_class=self.class_names[best_idx],
            confidence=best_confidence,
            percentage=best_confidence * 100,
            top_predictions=top_predictions,
            is_demo=self._demo_mode,
            is_low_confidence=best_confidence < self.low_confidence_threshold
        )
