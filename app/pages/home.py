"""
Home page for ATK Classifier application.
Landing page with overview and quick actions.
"""
import streamlit as st

from app.config import settings
from app.components.predictor import PredictionEngine


def render_header() -> None:
    """Render the page header with app info."""
    st.title(f"🏠 {settings.APP_NAME}")
    st.markdown(f"*{settings.APP_DESCRIPTION}*")
    st.markdown(f"**Version:** {settings.APP_VERSION}")


def render_demo_mode_banner(is_demo: bool) -> None:
    """Render demo mode banner if applicable."""
    if is_demo:
        st.info(
            "ℹ️ **Demo Mode Active** - No trained model found. "
            "Predictions will be simulated for demonstration purposes."
        )


def render_overview() -> None:
    """Render the application overview section."""
    st.markdown("---")
    st.markdown("## 📋 Overview")
    
    st.markdown("""
    ATK Classifier adalah aplikasi berbasis AI untuk mengklasifikasi gambar 
    Alat Tulis Kantor (ATK) menggunakan Convolutional Neural Network (CNN).
    
    **Fitur Utama:**
    - 🖼️ Upload atau capture gambar ATK
    - 🎯 Klasifikasi otomatis dengan confidence score
    - 📊 Dashboard monitoring performa model
    - 🔄 Manajemen versi model
    """)


def render_supported_classes() -> None:
    """Render the supported ATK classes."""
    st.markdown("## 🏷️ Kategori ATK yang Didukung")
    
    # Display classes in a grid
    cols = st.columns(4)
    for i, class_name in enumerate(settings.CLASS_NAMES):
        with cols[i % 4]:
            st.markdown(f"- {class_name}")


def render_quick_actions() -> None:
    """Render quick action buttons."""
    st.markdown("---")
    st.markdown("## ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Predict")
        st.markdown("Upload atau capture gambar untuk klasifikasi")
        if st.button("Go to Predict", key="btn_predict", use_container_width=True):
            st.session_state.nav_page = "Predict"
            st.rerun()
    
    with col2:
        st.markdown("### 📊 Dashboard")
        st.markdown("Lihat metrics dan performa model")
        if st.button("Go to Dashboard", key="btn_dashboard", use_container_width=True):
            st.session_state.nav_page = "Dashboard"
            st.rerun()
    
    with col3:
        st.markdown("### 🔧 Model Management")
        st.markdown("Kelola versi model")
        if st.button("Go to Model Management", key="btn_model", use_container_width=True):
            st.session_state.nav_page = "Model Management"
            st.rerun()


def render_getting_started() -> None:
    """Render getting started guide."""
    st.markdown("---")
    st.markdown("## 🚀 Getting Started")
    
    st.markdown("""
    1. **Upload Gambar** - Pilih gambar ATK dari device Anda
    2. **Capture dari Kamera** - Atau ambil foto langsung menggunakan kamera
    3. **Lihat Hasil** - Dapatkan prediksi kelas dan confidence score
    4. **Monitor Performa** - Pantau metrics model di Dashboard
    """)


def render() -> None:
    """Main render function for home page."""
    # Check demo mode
    engine = PredictionEngine()
    is_demo = engine.is_demo_mode()
    
    render_header()
    render_demo_mode_banner(is_demo)
    render_overview()
    render_supported_classes()
    render_quick_actions()
    render_getting_started()


if __name__ == "__main__":
    render()
