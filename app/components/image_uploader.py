"""
Image uploader component for ATK Classifier.
Provides file upload and camera capture widgets with validation.
"""
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
import io

import streamlit as st
from PIL import Image

from models.preprocessing import ImageValidator
from app.config import settings


@dataclass
class UploadResult:
    """Result of image upload/capture operation."""
    image: Optional[Image.Image]
    filename: str
    file_size: int
    is_valid: bool
    error_message: Optional[str]
    image_info: Optional[Dict[str, Any]]


class ImageUploader:
    """Handles image upload and camera capture with validation."""
    
    def __init__(
        self,
        max_size: int = None,
        allowed_extensions: list = None
    ):
        """
        Initialize uploader with validation settings.
        
        Args:
            max_size: Maximum file size in bytes (default from settings)
            allowed_extensions: List of allowed extensions (default from settings)
        """
        self.max_size = max_size or settings.MAX_UPLOAD_SIZE
        self.allowed_extensions = allowed_extensions or settings.ALLOWED_EXTENSIONS
        self.validator = ImageValidator()
    
    def _validate_file(self, filename: str, file_size: int) -> Tuple[bool, Optional[str]]:
        """
        Validate uploaded file.
        
        Args:
            filename: Name of the uploaded file
            file_size: Size of the file in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate extension
        if not self.validator.validate_extension(filename, self.allowed_extensions):
            return False, f"Invalid file type. Allowed: {', '.join(self.allowed_extensions)}"
        
        # Validate size
        if not self.validator.validate_file_size(file_size, self.max_size):
            max_mb = self.max_size / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_mb:.1f}MB"
        
        return True, None
    
    def _get_image_info(self, image: Image.Image, file_size: int) -> Dict[str, Any]:
        """
        Get image information including size in KB.
        
        Args:
            image: PIL Image object
            file_size: Original file size in bytes
            
        Returns:
            Dictionary with image information
        """
        info = self.validator.get_image_info(image)
        info["size_kb"] = file_size / 1024
        return info

    def render_file_upload(self, key: str = "file_uploader") -> Optional[UploadResult]:
        """
        Render file upload widget with validation.
        
        Args:
            key: Unique key for the widget
            
        Returns:
            UploadResult if file uploaded, None otherwise
        """
        # Create file type string for uploader
        file_types = [f".{ext}" for ext in self.allowed_extensions]
        
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=self.allowed_extensions,
            key=key,
            help=f"Supported formats: {', '.join(self.allowed_extensions)}. Max size: {self.max_size / (1024*1024):.0f}MB"
        )
        
        if uploaded_file is None:
            return None
        
        # Get file info
        filename = uploaded_file.name
        file_size = uploaded_file.size
        
        # Validate file
        is_valid, error_message = self._validate_file(filename, file_size)
        
        if not is_valid:
            return UploadResult(
                image=None,
                filename=filename,
                file_size=file_size,
                is_valid=False,
                error_message=error_message,
                image_info=None
            )
        
        # Load image
        try:
            image = Image.open(uploaded_file)
            image_info = self._get_image_info(image, file_size)
            
            return UploadResult(
                image=image,
                filename=filename,
                file_size=file_size,
                is_valid=True,
                error_message=None,
                image_info=image_info
            )
        except Exception as e:
            return UploadResult(
                image=None,
                filename=filename,
                file_size=file_size,
                is_valid=False,
                error_message=f"Failed to load image: {str(e)}",
                image_info=None
            )
    
    def render_camera_capture(self, key: str = "camera_input") -> Optional[UploadResult]:
        """
        Render camera capture widget.
        
        Args:
            key: Unique key for the widget
            
        Returns:
            UploadResult if image captured, None otherwise
        """
        camera_image = st.camera_input(
            "Capture from camera",
            key=key,
            help="Take a photo using your device camera"
        )
        
        if camera_image is None:
            return None
        
        # Camera images are always valid format (JPEG from browser)
        try:
            image = Image.open(camera_image)
            file_size = camera_image.size
            
            image_info = self._get_image_info(image, file_size)
            
            return UploadResult(
                image=image,
                filename="camera_capture.jpg",
                file_size=file_size,
                is_valid=True,
                error_message=None,
                image_info=image_info
            )
        except Exception as e:
            return UploadResult(
                image=None,
                filename="camera_capture.jpg",
                file_size=0,
                is_valid=False,
                error_message=f"Failed to process camera image: {str(e)}",
                image_info=None
            )
    
    def display_image_preview(self, result: UploadResult) -> None:
        """
        Display image preview with basic info.
        
        Args:
            result: UploadResult containing image and info
        """
        if not result.is_valid or result.image is None:
            st.error(result.error_message or "Invalid image")
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(result.image, caption=result.filename, use_container_width=True)
        
        with col2:
            st.markdown("**Image Info**")
            if result.image_info:
                st.write(f"📐 Dimensions: {result.image_info['width']} x {result.image_info['height']}")
                st.write(f"🎨 Format: {result.image_info.get('format', 'Unknown')}")
                st.write(f"📁 Size: {result.image_info['size_kb']:.1f} KB")
                st.write(f"🖼️ Mode: {result.image_info.get('mode', 'Unknown')}")
