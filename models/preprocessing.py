"""
Preprocessing module for ATK Classifier.
Handles image loading, validation, resizing, and normalization.
"""
from typing import Union, Dict, Any, Tuple, List
from pathlib import Path
import io

import numpy as np
from PIL import Image


class ImagePreprocessor:
    """Handles image preprocessing for CNN model input."""
    
    def __init__(self, input_size: Tuple[int, int] = (300, 300), normalize: bool = True):
        """
        Initialize preprocessor with target input size.
        
        Args:
            input_size: Target dimensions (width, height) for resizing
            normalize: Whether to normalize pixel values (set False if model has Rescaling layer)
        """
        self.input_size = input_size
        self.normalize = normalize
    
    def load_image(self, image_source: Union[str, Path, bytes, io.BytesIO, Image.Image]) -> Image.Image:
        """
        Load image from various sources.
        
        Args:
            image_source: File path, bytes, BytesIO, or PIL Image
            
        Returns:
            PIL Image object
        """
        if isinstance(image_source, Image.Image):
            return image_source
        elif isinstance(image_source, (str, Path)):
            return Image.open(image_source)
        elif isinstance(image_source, bytes):
            return Image.open(io.BytesIO(image_source))
        elif isinstance(image_source, io.BytesIO):
            return Image.open(image_source)
        else:
            raise ValueError(f"Unsupported image source type: {type(image_source)}")
    
    def resize_image(self, image: Image.Image) -> Image.Image:
        """
        Resize image to target input size.
        
        Args:
            image: PIL Image to resize
            
        Returns:
            Resized PIL Image
        """
        return image.resize(self.input_size, Image.Resampling.LANCZOS)

    def normalize_image(self, image: Image.Image) -> np.ndarray:
        """
        Convert image to RGB and optionally normalize pixel values to [0, 1] range.
        
        Args:
            image: PIL Image to normalize
            
        Returns:
            Numpy array with shape (height, width, 3)
        """
        # Convert to RGB (handles grayscale, RGBA, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        if self.normalize:
            # Normalize to [0, 1] for models without Rescaling layer
            img_array = np.array(image, dtype=np.float32) / 255.0
        else:
            # Keep as uint8 [0, 255] for models with Rescaling layer
            img_array = np.array(image, dtype=np.float32)
        
        return img_array
    
    def preprocess(self, image_source: Union[str, Path, bytes, io.BytesIO, Image.Image]) -> np.ndarray:
        """
        Full preprocessing pipeline: load, resize, normalize, and add batch dimension.
        
        Args:
            image_source: Image source (path, bytes, BytesIO, or PIL Image)
            
        Returns:
            Preprocessed numpy array with shape (1, height, width, 3)
        """
        # Load image
        image = self.load_image(image_source)
        
        # Resize to target dimensions
        image = self.resize_image(image)
        
        # Normalize and convert to RGB
        img_array = self.normalize_image(image)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def preprocess_for_model_with_rescaling(self, image_source: Union[str, Path, bytes, io.BytesIO, Image.Image]) -> np.ndarray:
        """
        Preprocess for models that have built-in Rescaling layer.
        Does NOT normalize - model handles normalization.
        
        Args:
            image_source: Image source
            
        Returns:
            Preprocessed numpy array with pixel values in [0, 255]
        """
        # Load image
        image = self.load_image(image_source)
        
        # Resize to target dimensions
        image = self.resize_image(image)
        
        # Convert to RGB without normalizing
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        img_array = np.array(image, dtype=np.float32)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array


class ImageValidator:
    """Validates image files for upload requirements."""
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int) -> bool:
        """
        Validate file size against maximum allowed.
        
        Args:
            file_size: Size of file in bytes
            max_size: Maximum allowed size in bytes
            
        Returns:
            True if file size is valid (within limit), False otherwise
        """
        return file_size <= max_size
    
    @staticmethod
    def validate_extension(filename: str, allowed: List[str]) -> bool:
        """
        Validate file extension against allowed list.
        
        Args:
            filename: Name of the file
            allowed: List of allowed extensions (without dots)
            
        Returns:
            True if extension is allowed, False otherwise
        """
        if not filename or '.' not in filename:
            return False
        
        extension = filename.rsplit('.', 1)[-1].lower()
        return extension in [ext.lower() for ext in allowed]
    
    @staticmethod
    def get_image_info(image: Image.Image) -> Dict[str, Any]:
        """
        Extract basic information from an image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with width, height, format, and mode
        """
        return {
            "width": image.width,
            "height": image.height,
            "format": image.format or "Unknown",
            "mode": image.mode
        }
