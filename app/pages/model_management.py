"""
Model Management page for ATK Classifier application.
Provides model version display and comparison functionality.
"""
from typing import List, Dict, Any
from dataclasses import dataclass

import streamlit as st

from app.config import settings
from app.components.predictor import PredictionEngine
from app.components.visualizer import ModelMetrics


@dataclass
class ModelVersion:
    """Data class for model version information."""
    version: str
    filename: str
    accuracy: float
    loss: float
    f1_score: float
    created_date: str
    is_active: bool
    description: str


def get_demo_model_versions() -> List[ModelVersion]:
    """
    Get demo model versions for display.
    
    Returns:
        List of demo ModelVersion objects
    """
    return [
        ModelVersion(
            version="v1.0.0",
            filename="best_model.h5",
            accuracy=0.0,
            loss=0.0,
            f1_score=0.0,
            created_date="N/A",
            is_active=True,
            description="Demo model (no trained model available)"
        )
    ]


def render_header() -> None:
    """Render the page header."""
    st.title("🔧 Model Management")
    st.markdown("Manage model versions and compare performance")


def render_demo_mode_banner(is_demo: bool) -> None:
    """Render demo mode banner if applicable."""
    if is_demo:
        st.info(
            "ℹ️ **Demo Mode** - No trained models available. "
            "Train and save a model to enable version management."
        )


def render_active_model(versions: List[ModelVersion]) -> None:
    """
    Render active model information.
    
    Args:
        versions: List of available model versions
    """
    st.markdown("## 🎯 Active Model")
    
    active_model = next((v for v in versions if v.is_active), None)
    
    if active_model:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {active_model.version}")
            st.markdown(f"**File:** `{active_model.filename}`")
            st.markdown(f"**Created:** {active_model.created_date}")
            st.markdown(f"**Description:** {active_model.description}")
        
        with col2:
            st.metric("Accuracy", f"{active_model.accuracy:.2%}")
            st.metric("Loss", f"{active_model.loss:.4f}")
            st.metric("F1 Score", f"{active_model.f1_score:.2%}")
    else:
        st.warning("No active model selected")


def render_model_versions_table(versions: List[ModelVersion]) -> None:
    """
    Render table of all model versions.
    
    Args:
        versions: List of available model versions
    """
    st.markdown("---")
    st.markdown("## 📋 Available Model Versions")
    
    if not versions:
        st.info("No model versions available")
        return
    
    # Create table data
    table_data = []
    for v in versions:
        table_data.append({
            "Version": v.version,
            "Accuracy": f"{v.accuracy:.2%}",
            "Loss": f"{v.loss:.4f}",
            "F1 Score": f"{v.f1_score:.2%}",
            "Created": v.created_date,
            "Status": "✅ Active" if v.is_active else "⬜ Inactive"
        })
    
    st.table(table_data)


def render_model_comparison(versions: List[ModelVersion]) -> None:
    """
    Render model comparison section.
    
    Args:
        versions: List of available model versions
    """
    st.markdown("---")
    st.markdown("## 📊 Model Comparison")
    
    if len(versions) < 2:
        st.info("Need at least 2 model versions for comparison")
        return
    
    col1, col2 = st.columns(2)
    
    version_names = [v.version for v in versions]
    
    with col1:
        model_a = st.selectbox(
            "Select Model A",
            options=version_names,
            key="compare_model_a"
        )
    
    with col2:
        model_b = st.selectbox(
            "Select Model B",
            options=version_names,
            index=min(1, len(version_names) - 1),
            key="compare_model_b"
        )
    
    if model_a and model_b:
        version_a = next((v for v in versions if v.version == model_a), None)
        version_b = next((v for v in versions if v.version == model_b), None)
        
        if version_a and version_b:
            render_comparison_table(version_a, version_b)


def render_comparison_table(model_a: ModelVersion, model_b: ModelVersion) -> None:
    """
    Render side-by-side comparison of two models.
    
    Args:
        model_a: First model version
        model_b: Second model version
    """
    st.markdown("### Comparison Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**Metric**")
        st.markdown("Accuracy")
        st.markdown("Loss")
        st.markdown("F1 Score")
    
    with col2:
        st.markdown(f"**{model_a.version}**")
        st.markdown(f"{model_a.accuracy:.2%}")
        st.markdown(f"{model_a.loss:.4f}")
        st.markdown(f"{model_a.f1_score:.2%}")
    
    with col3:
        st.markdown(f"**{model_b.version}**")
        st.markdown(f"{model_b.accuracy:.2%}")
        st.markdown(f"{model_b.loss:.4f}")
        st.markdown(f"{model_b.f1_score:.2%}")
    
    # Show difference
    st.markdown("### Difference (A - B)")
    
    acc_diff = model_a.accuracy - model_b.accuracy
    loss_diff = model_a.loss - model_b.loss
    f1_diff = model_a.f1_score - model_b.f1_score
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delta_color = "normal" if acc_diff >= 0 else "inverse"
        st.metric("Accuracy Δ", f"{acc_diff:+.2%}", delta_color=delta_color)
    
    with col2:
        # For loss, lower is better
        delta_color = "inverse" if loss_diff >= 0 else "normal"
        st.metric("Loss Δ", f"{loss_diff:+.4f}", delta_color=delta_color)
    
    with col3:
        delta_color = "normal" if f1_diff >= 0 else "inverse"
        st.metric("F1 Score Δ", f"{f1_diff:+.2%}", delta_color=delta_color)


def render_model_actions(versions: List[ModelVersion], is_demo: bool) -> None:
    """
    Render model action buttons.
    
    Args:
        versions: List of available model versions
        is_demo: Whether running in demo mode
    """
    st.markdown("---")
    st.markdown("## ⚙️ Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Models", use_container_width=True, disabled=is_demo):
            st.rerun()
    
    with col2:
        version_names = [v.version for v in versions if not v.is_active]
        selected = st.selectbox(
            "Switch to version:",
            options=version_names if version_names else ["No other versions"],
            disabled=is_demo or not version_names
        )
        
        if st.button("✅ Activate", use_container_width=True, disabled=is_demo or not version_names):
            st.success(f"Model {selected} activated (demo)")
    
    with col3:
        st.markdown("**Model Path:**")
        st.code(str(settings.MODEL_PATH))


def render_upload_section(is_demo: bool) -> None:
    """
    Render model upload section.
    
    Args:
        is_demo: Whether running in demo mode
    """
    st.markdown("---")
    st.markdown("## 📤 Upload New Model")
    
    with st.expander("Upload Model File"):
        st.markdown("""
        Upload a trained model file (.h5 format) to add a new version.
        
        **Requirements:**
        - File format: HDF5 (.h5)
        - Input shape: 224x224x3
        - Output classes: 8
        """)
        
        uploaded_file = st.file_uploader(
            "Choose model file",
            type=["h5"],
            disabled=is_demo
        )
        
        if uploaded_file:
            version_name = st.text_input("Version name", value="v1.0.1")
            description = st.text_area("Description", value="New model version")
            
            if st.button("Upload Model", disabled=is_demo):
                st.info("Model upload functionality - placeholder for production")


def render() -> None:
    """Main render function for model management page."""
    # Check demo mode
    engine = PredictionEngine()
    is_demo = engine.is_demo_mode()
    
    # Get model versions (demo or real)
    versions = get_demo_model_versions()
    
    # Render page
    render_header()
    render_demo_mode_banner(is_demo)
    render_active_model(versions)
    render_model_versions_table(versions)
    render_model_comparison(versions)
    render_model_actions(versions, is_demo)
    render_upload_section(is_demo)


if __name__ == "__main__":
    render()
