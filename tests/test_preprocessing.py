"""
Property-based tests for the preprocessing module.
Uses Hypothesis library for property-based testing.
"""
import numpy as np
from PIL import Image
from hypothesis import given, strategies as st, settings, HealthCheck

from models.preprocessing import ImagePreprocessor, ImageValidator


# Strategies for generating test data
@st.composite
def random_image(draw, min_size=1, max_size=100):
    """Generate random PIL Images with various modes."""
    width = draw(st.integers(min_value=min_size, max_value=max_size))
    height = draw(st.integers(min_value=min_size, max_value=max_size))
    mode = draw(st.sampled_from(['RGB', 'RGBA', 'L']))  # RGB, RGBA (with alpha), L (grayscale)
    
    # Create image with solid color for speed
    if mode == 'L':
        img = Image.new(mode, (width, height), color=draw(st.integers(0, 255)))
    elif mode == 'RGB':
        r = draw(st.integers(0, 255))
        g = draw(st.integers(0, 255))
        b = draw(st.integers(0, 255))
        img = Image.new(mode, (width, height), color=(r, g, b))
    else:  # RGBA
        r = draw(st.integers(0, 255))
        g = draw(st.integers(0, 255))
        b = draw(st.integers(0, 255))
        a = draw(st.integers(0, 255))
        img = Image.new(mode, (width, height), color=(r, g, b, a))
    
    return img


# **Feature: atk-classifier-mlops, Property 6: Resize Output Dimensions**
# **Validates: Requirements 3.1**
class TestResizeOutputDimensions:
    """Property tests for resize output dimensions."""
    
    @given(image=random_image())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_resize_produces_correct_dimensions(self, image):
        """
        Property 6: For any input image of any dimensions, after preprocessing 
        the output SHALL have exactly shape (1, 224, 224, 3).
        """
        preprocessor = ImagePreprocessor(input_size=(224, 224))
        result = preprocessor.preprocess(image)
        
        assert result.shape == (1, 224, 224, 3), \
            f"Expected shape (1, 224, 224, 3), got {result.shape}"


# **Feature: atk-classifier-mlops, Property 7: Normalization Range**
# **Validates: Requirements 3.2**
class TestNormalizationRange:
    """Property tests for normalization range."""
    
    @given(image=random_image())
    @settings(max_examples=100)
    def test_normalized_values_in_range(self, image):
        """
        Property 7: For any preprocessed image array with normalize=True,
        all pixel values SHALL be in the range [0.0, 1.0].
        """
        preprocessor = ImagePreprocessor(input_size=(224, 224), normalize=True)
        result = preprocessor.preprocess(image)
        
        assert np.all(result >= 0.0), \
            f"Found values below 0.0: min={result.min()}"
        assert np.all(result <= 1.0), \
            f"Found values above 1.0: max={result.max()}"
    
    @given(image=random_image())
    @settings(max_examples=100)
    def test_unnormalized_values_in_range(self, image):
        """
        For models with Rescaling layer (normalize=False), pixel values
        SHALL be in the range [0.0, 255.0].
        """
        preprocessor = ImagePreprocessor(input_size=(224, 224), normalize=False)
        result = preprocessor.preprocess(image)
        
        assert np.all(result >= 0.0), \
            f"Found values below 0.0: min={result.min()}"
        assert np.all(result <= 255.0), \
            f"Found values above 255.0: max={result.max()}"


# **Feature: atk-classifier-mlops, Property 8: RGB Channel Count**
# **Validates: Requirements 3.3**
class TestRGBChannelCount:
    """Property tests for RGB channel count."""
    
    @given(image=random_image())
    @settings(max_examples=100)
    def test_output_has_three_channels(self, image):
        """
        Property 8: For any input image (grayscale, RGBA, or RGB), after 
        preprocessing the output SHALL have exactly 3 color channels.
        """
        preprocessor = ImagePreprocessor(input_size=(224, 224))
        result = preprocessor.preprocess(image)
        
        # Shape is (batch, height, width, channels)
        assert result.shape[-1] == 3, \
            f"Expected 3 channels, got {result.shape[-1]}"


# **Feature: atk-classifier-mlops, Property 1: File Validation Correctness**
# **Validates: Requirements 1.1**
class TestFileValidation:
    """Property tests for file validation."""
    
    # Allowed extensions as per requirements
    ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "bmp"]
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    
    @given(
        file_size=st.integers(min_value=0, max_value=10 * 1024 * 1024),
        extension=st.sampled_from(["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp", "pdf", "txt"])
    )
    @settings(max_examples=100)
    def test_file_validation_correctness(self, file_size, extension):
        """
        Property 1: For any file with size and extension, the validator SHALL 
        accept files with allowed extensions (.jpg, .jpeg, .png, .bmp) AND 
        size <= 5MB, and reject all others.
        """
        filename = f"test_image.{extension}"
        
        size_valid = ImageValidator.validate_file_size(file_size, self.MAX_SIZE)
        ext_valid = ImageValidator.validate_extension(filename, self.ALLOWED_EXTENSIONS)
        
        # Check size validation
        expected_size_valid = file_size <= self.MAX_SIZE
        assert size_valid == expected_size_valid, \
            f"Size validation failed: size={file_size}, expected={expected_size_valid}, got={size_valid}"
        
        # Check extension validation
        expected_ext_valid = extension.lower() in [e.lower() for e in self.ALLOWED_EXTENSIONS]
        assert ext_valid == expected_ext_valid, \
            f"Extension validation failed: ext={extension}, expected={expected_ext_valid}, got={ext_valid}"


# **Feature: atk-classifier-mlops, Property 2: Image Info Extraction**
# **Validates: Requirements 1.3**
class TestImageInfoExtraction:
    """Property tests for image info extraction."""
    
    @given(image=random_image())
    @settings(max_examples=100)
    def test_image_info_matches_actual_properties(self, image):
        """
        Property 2: For any valid image, the info extractor SHALL return correct 
        width, height, and format matching the actual image properties.
        """
        info = ImageValidator.get_image_info(image)
        
        # Verify width matches
        assert info["width"] == image.width, \
            f"Width mismatch: expected {image.width}, got {info['width']}"
        
        # Verify height matches
        assert info["height"] == image.height, \
            f"Height mismatch: expected {image.height}, got {info['height']}"
        
        # Verify mode matches
        assert info["mode"] == image.mode, \
            f"Mode mismatch: expected {image.mode}, got {info['mode']}"
        
        # Format may be None for in-memory images, so we check it's present in the dict
        assert "format" in info, "Format key missing from image info"
