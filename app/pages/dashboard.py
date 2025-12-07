"""
Dashboard page for ATK Classifier application.
Displays model metrics and performance charts.
"""
import streamlit as st

from app.config import settings
from app.components.predictor import PredictionEngine
from app.components.visualizer import (
    ModelMetrics,
    display_model_metrics,
    display_class_distribution,
    create_metrics_gauge,
    get_demo_metrics,
    get_demo_class_distribution
)


def render_header() -> None:
    """Render the page header."""
    st.title("📊 Dashboard")
    st.markdown("Monitor model performance dan metrics")


def render_demo_mode_banner(is_demo: bool) -> None:
    """Render demo mode banner if applicable."""
    if is_demo:
        st.info(
            "ℹ️ **Demo Mode** - Displaying placeholder metrics. "
            "Add a trained model to see real performance data."
        )


def render_model_info(metrics: ModelMetrics) -> None:
    """
    Render model information section.
    
    Args:
        metrics: ModelMetrics object with model info
    """
    st.markdown("## 📋 Model Information")
    display_model_metrics(metrics)


def render_performance_gauges(metrics: ModelMetrics) -> None:
    """
    Render performance gauge charts.
    
    Args:
        metrics: ModelMetrics object with performance data
    """
    st.markdown("---")
    st.markdown("## 📈 Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = create_metrics_gauge(
            value=metrics.accuracy,
            title="Accuracy",
            max_value=1.0
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # For loss, lower is better, so we invert the thresholds
        fig = create_metrics_gauge(
            value=metrics.loss,
            title="Loss",
            max_value=2.0,
            threshold_good=0.3,
            threshold_medium=0.7
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        fig = create_metrics_gauge(
            value=metrics.f1_score,
            title="F1 Score",
            max_value=1.0
        )
        st.plotly_chart(fig, use_container_width=True)


def render_class_distribution(class_counts: dict) -> None:
    """
    Render class distribution chart.
    
    Args:
        class_counts: Dictionary mapping class names to counts
    """
    st.markdown("---")
    st.markdown("## 📊 Class Distribution")
    st.markdown("Distribution of training samples per class")
    
    display_class_distribution(class_counts)


def render_model_details() -> None:
    """Render model architecture details."""
    st.markdown("---")
    st.markdown("## 🏗️ Model Architecture")
    
    with st.expander("View Model Details"):
        st.markdown(f"""
        **Model Type:** Custom CNN
        
        **Input Shape:** {settings.INPUT_SIZE[0]} x {settings.INPUT_SIZE[1]} x 3
        
        **Number of Classes:** {settings.NUM_CLASSES}
        
        **Classes:**
        """)
        
        for i, class_name in enumerate(settings.CLASS_NAMES, 1):
            st.markdown(f"{i}. {class_name}")
        
        st.markdown("""
        **Architecture Layers:**
        - Conv2D (32 filters) + BatchNorm + MaxPool
        - Conv2D (64 filters) + BatchNorm + MaxPool
        - Conv2D (128 filters) + BatchNorm + MaxPool
        - Conv2D (256 filters) + BatchNorm + MaxPool
        - Flatten + Dense (512) + Dropout (0.5)
        - Dense (256) + Dropout (0.3)
        - Dense (8, softmax)
        """)


def render_quick_stats(is_demo: bool) -> None:
    """
    Render quick statistics.
    
    Args:
        is_demo: Whether running in demo mode
    """
    st.markdown("---")
    st.markdown("## 📌 Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Classes",
            value=settings.NUM_CLASSES
        )
    
    with col2:
        st.metric(
            label="Input Size",
            value=f"{settings.INPUT_SIZE[0]}x{settings.INPUT_SIZE[1]}"
        )
    
    with col3:
        st.metric(
            label="Mode",
            value="Demo" if is_demo else "Production"
        )
    
    with col4:
        st.metric(
            label="Top-K",
            value=settings.TOP_K_PREDICTIONS
        )


def render() -> None:
    """Main render function for dashboard page."""
    # Check demo mode
    engine = PredictionEngine()
    is_demo = engine.is_demo_mode()
    
    # Get metrics (demo or real)
    if is_demo:
        metrics = get_demo_metrics()
        class_counts = get_demo_class_distribution()
    else:
        # In production, these would come from model metadata
        metrics = get_demo_metrics()  # Placeholder
        class_counts = get_demo_class_distribution()  # Placeholder
    
    # Render page
    render_header()
    render_demo_mode_banner(is_demo)
    render_quick_stats(is_demo)
    render_model_info(metrics)
    render_performance_gauges(metrics)
    render_class_distribution(class_counts)
    render_model_details()


if __name__ == "__main__":
    render()
