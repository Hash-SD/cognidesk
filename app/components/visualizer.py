"""
Visualizer component for ATK Classifier.
Provides chart functions for dashboard visualization.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app.config import settings


@dataclass
class ModelMetrics:
    """Data class for model metrics."""
    version: str
    accuracy: float
    loss: float
    f1_score: float
    created_date: str


def create_class_distribution_chart(
    class_counts: Dict[str, int],
    title: str = "Class Distribution"
) -> go.Figure:
    """
    Create a bar chart showing class distribution.
    
    Args:
        class_counts: Dictionary mapping class names to counts
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    df = pd.DataFrame({
        "Class": list(class_counts.keys()),
        "Count": list(class_counts.values())
    })
    
    fig = px.bar(
        df,
        x="Class",
        y="Count",
        title=title,
        color="Count",
        color_continuous_scale="Blues"
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig


def create_metrics_gauge(
    value: float,
    title: str,
    max_value: float = 1.0,
    threshold_good: float = 0.8,
    threshold_medium: float = 0.6
) -> go.Figure:
    """
    Create a gauge chart for displaying a metric.
    
    Args:
        value: Current metric value
        title: Metric title
        max_value: Maximum value for the gauge
        threshold_good: Threshold for good (green) zone
        threshold_medium: Threshold for medium (yellow) zone
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={
            "axis": {"range": [0, max_value]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, threshold_medium], "color": "lightcoral"},
                {"range": [threshold_medium, threshold_good], "color": "lightyellow"},
                {"range": [threshold_good, max_value], "color": "lightgreen"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": value
            }
        }
    ))
    
    fig.update_layout(height=250)
    
    return fig


def create_confusion_matrix_chart(
    confusion_matrix: List[List[int]],
    class_names: List[str] = None
) -> go.Figure:
    """
    Create a heatmap for confusion matrix visualization.
    
    Args:
        confusion_matrix: 2D list of confusion matrix values
        class_names: List of class names for labels
        
    Returns:
        Plotly Figure object
    """
    class_names = class_names or settings.CLASS_NAMES
    
    fig = px.imshow(
        confusion_matrix,
        labels=dict(x="Predicted", y="Actual", color="Count"),
        x=class_names,
        y=class_names,
        title="Confusion Matrix",
        color_continuous_scale="Blues"
    )
    
    fig.update_layout(
        xaxis_tickangle=-45
    )
    
    return fig


def create_training_history_chart(
    history: Dict[str, List[float]],
    title: str = "Training History"
) -> go.Figure:
    """
    Create a line chart showing training history.
    
    Args:
        history: Dictionary with 'accuracy', 'val_accuracy', 'loss', 'val_loss' keys
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    epochs = list(range(1, len(history.get("accuracy", [])) + 1))
    
    fig = go.Figure()
    
    if "accuracy" in history:
        fig.add_trace(go.Scatter(
            x=epochs,
            y=history["accuracy"],
            mode="lines",
            name="Training Accuracy"
        ))
    
    if "val_accuracy" in history:
        fig.add_trace(go.Scatter(
            x=epochs,
            y=history["val_accuracy"],
            mode="lines",
            name="Validation Accuracy"
        ))
    
    if "loss" in history:
        fig.add_trace(go.Scatter(
            x=epochs,
            y=history["loss"],
            mode="lines",
            name="Training Loss",
            yaxis="y2"
        ))
    
    if "val_loss" in history:
        fig.add_trace(go.Scatter(
            x=epochs,
            y=history["val_loss"],
            mode="lines",
            name="Validation Loss",
            yaxis="y2"
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Epoch",
        yaxis_title="Accuracy",
        yaxis2=dict(
            title="Loss",
            overlaying="y",
            side="right"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def display_model_metrics(metrics: ModelMetrics) -> None:
    """
    Display model metrics in Streamlit.
    
    Args:
        metrics: ModelMetrics object to display
    """
    st.markdown(f"### Model Version: {metrics.version}")
    st.caption(f"Created: {metrics.created_date}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Accuracy", f"{metrics.accuracy:.2%}")
    
    with col2:
        st.metric("Loss", f"{metrics.loss:.4f}")
    
    with col3:
        st.metric("F1 Score", f"{metrics.f1_score:.2%}")


def display_class_distribution(class_counts: Dict[str, int]) -> None:
    """
    Display class distribution chart in Streamlit.
    
    Args:
        class_counts: Dictionary mapping class names to counts
    """
    fig = create_class_distribution_chart(class_counts)
    st.plotly_chart(fig, use_container_width=True)


def get_demo_metrics() -> ModelMetrics:
    """
    Get demo metrics for display when no real model exists.
    
    Returns:
        ModelMetrics with demo values
    """
    return ModelMetrics(
        version="demo-v1.0.0",
        accuracy=0.0,
        loss=0.0,
        f1_score=0.0,
        created_date="N/A (Demo Mode)"
    )


def get_demo_class_distribution() -> Dict[str, int]:
    """
    Get demo class distribution for display.
    
    Returns:
        Dictionary with demo class counts
    """
    return {name: 0 for name in settings.CLASS_NAMES}
