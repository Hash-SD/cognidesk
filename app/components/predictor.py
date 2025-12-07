"""
Predictor component for ATK Classifier.
Provides prediction engine with caching and result display.
"""
from typing import Optional
from PIL import Image

import streamlit as st

from models.inference import InferencePipeline
from models.cnn_model import PredictionResult
from app.config import settings


class PredictionEngine:
    """
    Prediction engine with Streamlit caching support.
    Uses st.cache_resource for model caching.
    """
    
    def __init__(self):
        """Initialize prediction engine."""
        self._pipeline = self._get_cached_pipeline()
    
    @staticmethod
    @st.cache_resource
    def _get_cached_pipeline() -> InferencePipeline:
        """
        Get cached inference pipeline.
        Uses st.cache_resource to cache the model across sessions.
        
        Returns:
            Cached InferencePipeline instance
        """
        return InferencePipeline(
            model_path=str(settings.MODEL_PATH),
            input_size=settings.INPUT_SIZE,
            class_names=settings.CLASS_NAMES,
            low_confidence_threshold=settings.LOW_CONFIDENCE_THRESHOLD
        )
    
    def is_demo_mode(self) -> bool:
        """Check if running in demo mode."""
        return self._pipeline.is_demo_mode()
    
    def predict(self, image: Image.Image, top_k: int = None) -> PredictionResult:
        """
        Run prediction on an image.
        
        Args:
            image: PIL Image to classify
            top_k: Number of top predictions (default from settings)
            
        Returns:
            PredictionResult with classification results
        """
        top_k = top_k or settings.TOP_K_PREDICTIONS
        return self._pipeline.predict(image, top_k=top_k)


def display_results(result: PredictionResult) -> None:
    """
    Display prediction results in Streamlit.
    
    Args:
        result: PredictionResult to display
    """
    # Demo mode indicator
    if result.is_demo:
        st.warning(f"⚠️ {settings.DEMO_MODE_MESSAGE}")
    
    # Low confidence warning
    if result.is_low_confidence:
        st.warning(
            f"⚠️ Low confidence prediction ({result.percentage:.1f}%). "
            "The model is uncertain about this classification."
        )
    
    # Main prediction result
    st.markdown("### 🎯 Prediction Result")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Predicted Class",
            value=result.predicted_class
        )
    
    with col2:
        st.metric(
            label="Confidence",
            value=f"{result.percentage:.1f}%"
        )
    
    # Top-K predictions
    st.markdown("### 📊 Top Predictions")
    
    for i, pred in enumerate(result.top_predictions, 1):
        confidence_pct = pred["percentage"]
        
        # Create progress bar with label
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.write(f"**{i}. {pred['class']}**")
        
        with col2:
            st.progress(pred["confidence"])
        
        with col3:
            st.write(f"{confidence_pct:.1f}%")


def display_results_compact(result: PredictionResult) -> None:
    """
    Display prediction results in a compact format.
    
    Args:
        result: PredictionResult to display
    """
    # Demo mode indicator
    if result.is_demo:
        st.caption(f"⚠️ Demo mode - predictions are simulated")
    
    # Main result with confidence bar
    st.markdown(f"**{result.predicted_class}** ({result.percentage:.1f}%)")
    st.progress(result.confidence)
    
    # Low confidence warning
    if result.is_low_confidence:
        st.caption("⚠️ Low confidence - model is uncertain")
