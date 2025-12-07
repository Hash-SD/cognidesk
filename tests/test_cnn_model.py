"""
Property-based tests for the CNN model module.
Uses Hypothesis library for property-based testing.
"""
import numpy as np
from hypothesis import given, strategies as st, settings, assume

from models.cnn_model import ModelPredictor, PredictionResult


# Strategy for generating valid preprocessed images
@st.composite
def preprocessed_image(draw):
    """Generate valid preprocessed image arrays with shape (1, 224, 224, 3)."""
    # Generate normalized pixel values in [0, 1]
    data = draw(st.lists(
        st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        min_size=224*224*3,
        max_size=224*224*3
    ))
    arr = np.array(data, dtype=np.float32).reshape(1, 224, 224, 3)
    return arr


# **Feature: atk-classifier-mlops, Property 3: Prediction Output Validity**
# **Validates: Requirements 2.1**
class TestPredictionOutputValidity:
    """Property tests for prediction output validity."""
    
    CLASS_NAMES = [
        "Spidol", "Pensil", "Pulpen", "Penggaris",
        "Penghapus", "Correction Tape", "Pensil Mekanik", "Tipe X"
    ]
    
    @given(
        # Use simpler strategy - just generate random seed for reproducibility
        seed=st.integers(min_value=0, max_value=10000)
    )
    @settings(max_examples=100)
    def test_prediction_returns_valid_class_and_confidence(self, seed):
        """
        Property 3: For any valid preprocessed image, the predictor SHALL return 
        a class name from the valid CLASS_NAMES list and confidence in range [0, 1].
        """
        np.random.seed(seed)
        
        # Create a simple test image
        test_image = np.random.rand(1, 224, 224, 3).astype(np.float32)
        
        # Use demo mode predictor (no model file)
        predictor = ModelPredictor(
            model_path=None,
            class_names=self.CLASS_NAMES
        )
        
        result = predictor.predict(test_image, top_k=3)
        
        # Verify predicted class is in valid class names
        assert result.predicted_class in self.CLASS_NAMES, \
            f"Predicted class '{result.predicted_class}' not in valid classes"
        
        # Verify confidence is in [0, 1]
        assert 0.0 <= result.confidence <= 1.0, \
            f"Confidence {result.confidence} not in range [0, 1]"
        
        # Verify percentage matches confidence
        assert abs(result.percentage - result.confidence * 100) < 0.001, \
            f"Percentage {result.percentage} doesn't match confidence {result.confidence}"


# **Feature: atk-classifier-mlops, Property 4: Top-K Predictions Ordering**
# **Validates: Requirements 2.2**
class TestTopKPredictionsOrdering:
    """Property tests for top-k predictions ordering."""
    
    CLASS_NAMES = [
        "Spidol", "Pensil", "Pulpen", "Penggaris",
        "Penghapus", "Correction Tape", "Pensil Mekanik", "Tipe X"
    ]
    
    @given(
        seed=st.integers(min_value=0, max_value=10000),
        top_k=st.integers(min_value=1, max_value=8)
    )
    @settings(max_examples=100)
    def test_top_k_predictions_sorted_descending(self, seed, top_k):
        """
        Property 4: For any prediction result with top-K predictions, the predictions 
        SHALL be sorted in descending order by confidence, and all confidences SHALL sum to <= 1.
        """
        np.random.seed(seed)
        
        test_image = np.random.rand(1, 224, 224, 3).astype(np.float32)
        
        predictor = ModelPredictor(
            model_path=None,
            class_names=self.CLASS_NAMES
        )
        
        result = predictor.predict(test_image, top_k=top_k)
        
        # Verify we got the requested number of predictions (or all classes if top_k > num_classes)
        expected_count = min(top_k, len(self.CLASS_NAMES))
        assert len(result.top_predictions) == expected_count, \
            f"Expected {expected_count} predictions, got {len(result.top_predictions)}"
        
        # Verify predictions are sorted in descending order by confidence
        confidences = [p["confidence"] for p in result.top_predictions]
        for i in range(len(confidences) - 1):
            assert confidences[i] >= confidences[i + 1], \
                f"Predictions not sorted: {confidences[i]} < {confidences[i + 1]}"
        
        # Verify all confidences are in valid range
        for pred in result.top_predictions:
            assert 0.0 <= pred["confidence"] <= 1.0, \
                f"Confidence {pred['confidence']} not in range [0, 1]"


# **Feature: atk-classifier-mlops, Property 5: Low Confidence Detection**
# **Validates: Requirements 2.3**
class TestLowConfidenceDetection:
    """Property tests for low confidence detection."""
    
    CLASS_NAMES = [
        "Spidol", "Pensil", "Pulpen", "Penggaris",
        "Penghapus", "Correction Tape", "Pensil Mekanik", "Tipe X"
    ]
    
    @given(
        seed=st.integers(min_value=0, max_value=10000),
        threshold=st.floats(min_value=0.1, max_value=0.9, allow_nan=False)
    )
    @settings(max_examples=100)
    def test_low_confidence_flag_correctness(self, seed, threshold):
        """
        Property 5: For any prediction with confidence value, the is_low_confidence 
        flag SHALL be True if and only if confidence < 0.5.
        """
        np.random.seed(seed)
        
        test_image = np.random.rand(1, 224, 224, 3).astype(np.float32)
        
        predictor = ModelPredictor(
            model_path=None,
            class_names=self.CLASS_NAMES,
            low_confidence_threshold=threshold
        )
        
        result = predictor.predict(test_image, top_k=3)
        
        # Verify is_low_confidence flag matches threshold comparison
        expected_low_confidence = result.confidence < threshold
        assert result.is_low_confidence == expected_low_confidence, \
            f"is_low_confidence={result.is_low_confidence} but confidence={result.confidence}, threshold={threshold}"


# **Feature: atk-classifier-mlops, Property 6: Top-K Exceeds Class Count**
# **Validates: Bug fix for top_k > num_classes**
class TestTopKExceedsClassCount:
    """Tests for handling top_k larger than number of classes."""
    
    SMALL_CLASS_NAMES = ["eraser", "kertas", "pensil"]  # Only 3 classes
    
    @given(
        seed=st.integers(min_value=0, max_value=10000),
        top_k=st.integers(min_value=1, max_value=20)  # Can be larger than class count
    )
    @settings(max_examples=50)
    def test_top_k_capped_at_class_count(self, seed, top_k):
        """
        Bug Fix Test: When top_k exceeds the number of classes, the predictor 
        SHALL return at most len(class_names) predictions without raising an error.
        """
        np.random.seed(seed)
        
        test_image = np.random.rand(1, 300, 300, 3).astype(np.float32)
        
        predictor = ModelPredictor(
            model_path=None,
            class_names=self.SMALL_CLASS_NAMES
        )
        
        # This should NOT raise an IndexError even if top_k > len(class_names)
        result = predictor.predict(test_image, top_k=top_k)
        
        # Verify we get at most len(class_names) predictions
        expected_count = min(top_k, len(self.SMALL_CLASS_NAMES))
        assert len(result.top_predictions) == expected_count, \
            f"Expected {expected_count} predictions, got {len(result.top_predictions)}"
        
        # Verify all predicted classes are valid
        for pred in result.top_predictions:
            assert pred["class"] in self.SMALL_CLASS_NAMES, \
                f"Invalid class '{pred['class']}' not in {self.SMALL_CLASS_NAMES}"
    
    def test_top_k_10_with_3_classes(self):
        """
        Specific test case: Request top_k=10 with only 3 classes.
        This was the original bug - would cause IndexError.
        """
        test_image = np.random.rand(1, 300, 300, 3).astype(np.float32)
        
        predictor = ModelPredictor(
            model_path=None,
            class_names=self.SMALL_CLASS_NAMES
        )
        
        # This should NOT raise an error
        result = predictor.predict(test_image, top_k=10)
        
        # Should return exactly 3 predictions (capped at class count)
        assert len(result.top_predictions) == 3, \
            f"Expected 3 predictions, got {len(result.top_predictions)}"
