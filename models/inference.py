"""
Inference pipeline module for ATK Classifier.
Combines preprocessing and prediction in a single pipeline.
"""
from typing import Union, Optional, List
from pathlib import Path
import io

from PIL import Image

from models.preprocessing import ImagePreprocessor, ImageValidator
from models.cnn_model import ModelPredictor, PredictionResult


class InferencePipeline:
    """
    Complete inference pipeline combining preprocessing and prediction.
    Provides a single interface for image classification.
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        input_size: tuple = (300, 300),
        class_names: Optional[List[str]] = None,
        low_confidence_threshold: float = 0.5
    ):
        """
        Initialize the inference pipeline.
        
        Args:
            model_path: Path to the trained model file
            input_size: Target input size for preprocessing
            class_names: List of class names for predictions
            low_confidence_threshold: Threshold for low confidence warning
        """
        # normalize=False karena model sudah punya Rescaling layer
        self.preprocessor = ImagePreprocessor(input_size=input_size, normalize=False)
        self.predictor = ModelPredictor(
            model_path=model_path,
            class_names=class_names,
            low_confidence_threshold=low_confidence_threshold
        )
        self.validator = ImageValidator()
    
    def is_demo_mode(self) -> bool:
        """Check if pipeline is running in demo mode."""
        return self.predictor.is_demo_mode()
    
    def validate_image(
        self,
        filename: str,
        file_size: int,
        allowed_extensions: List[str],
        max_size: int
    ) -> tuple:
        """
        Validate image file before processing.
        
        Args:
            filename: Name of the uploaded file
            file_size: Size of the file in bytes
            allowed_extensions: List of allowed file extensions
            max_size: Maximum allowed file size in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.validator.validate_extension(filename, allowed_extensions):
            return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        
        if not self.validator.validate_file_size(file_size, max_size):
            max_mb = max_size / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_mb:.1f}MB"
        
        return True, None
    
    def predict(
        self,
        image_source: Union[str, Path, bytes, io.BytesIO, Image.Image],
        top_k: int = 3
    ) -> PredictionResult:
        """
        Run full inference pipeline on an image.
        
        Args:
            image_source: Image source (path, bytes, BytesIO, or PIL Image)
            top_k: Number of top predictions to return
            
        Returns:
            PredictionResult with classification results
        """
        # Preprocess the image
        preprocessed = self.preprocessor.preprocess(image_source)
        
        # Run prediction
        result = self.predictor.predict(preprocessed, top_k=top_k)
        
        return result
    
    def get_image_info(
        self,
        image_source: Union[str, Path, bytes, io.BytesIO, Image.Image]
    ) -> dict:
        """
        Get information about an image.
        
        Args:
            image_source: Image source
            
        Returns:
            Dictionary with image information
        """
        image = self.preprocessor.load_image(image_source)
        return self.validator.get_image_info(image)
