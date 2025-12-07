"""
ATK Classifier - Simple and Clean Interface
"""
import streamlit as st
from PIL import Image

from app.config import settings
from app.components.predictor import PredictionEngine, display_results


# Page configuration
st.set_page_config(
    page_title="ATK Classifier",
    page_icon="✏️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


def render_header():
    """Render app header."""
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1>✏️ ATK Classifier</h1>
        <p style="color: #666; font-size: 1.1rem;">
            Klasifikasi Alat Tulis Kantor dengan AI
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_categories():
    """Show supported categories."""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
            <div style="font-size: 2rem;">🧹</div>
            <div style="font-weight: bold;">Eraser</div>
            <div style="color: #666; font-size: 0.9rem;">Penghapus</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
            <div style="font-size: 2rem;">📄</div>
            <div style="font-weight: bold;">Kertas</div>
            <div style="color: #666; font-size: 0.9rem;">Paper</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
            <div style="font-size: 2rem;">✏️</div>
            <div style="font-weight: bold;">Pensil</div>
            <div style="color: #666; font-size: 0.9rem;">Pencil</div>
        </div>
        """, unsafe_allow_html=True)


def render_upload_section():
    """Render image upload and prediction."""
    st.markdown("---")
    st.markdown("### 📸 Upload Gambar ATK")
    
    # Tab for upload methods
    tab1, tab2 = st.tabs(["📁 Upload File", "📷 Kamera"])
    
    with tab1:
        uploaded_file = st.file_uploader(
            "Pilih gambar",
            type=["jpg", "jpeg", "png"],
            help="Format: JPG, JPEG, PNG. Max: 5MB",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            process_image(uploaded_file)
    
    with tab2:
        camera_image = st.camera_input(
            "Ambil foto",
            label_visibility="collapsed"
        )
        
        if camera_image:
            process_image(camera_image)


def process_image(image_source):
    """Process and predict image."""
    try:
        image = Image.open(image_source)
        
        # Show image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption="Gambar Input", use_container_width=True)
        
        with col2:
            # Run prediction
            engine = get_prediction_engine()
            
            with st.spinner("🔄 Menganalisis..."):
                result = engine.predict(image, top_k=3)
            
            # Show result
            if result.is_demo:
                st.warning("⚠️ Mode Demo - Model belum tersedia")
            
            # Main prediction
            st.markdown(f"""
            <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
                <div style="font-size: 0.9rem; opacity: 0.9;">Hasil Prediksi</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{result.predicted_class.upper()}</div>
                <div style="font-size: 1.5rem;">{result.percentage:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence bar
            st.markdown("<br>", unsafe_allow_html=True)
            
            if result.is_low_confidence:
                st.warning("⚠️ Confidence rendah - hasil mungkin kurang akurat")
            
            # Top predictions
            st.markdown("**Semua Prediksi:**")
            for pred in result.top_predictions:
                st.progress(pred["confidence"], text=f"{pred['class']}: {pred['percentage']:.1f}%")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")


@st.cache_resource
def get_prediction_engine():
    """Get cached prediction engine."""
    return PredictionEngine()


def render_footer():
    """Render footer."""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.85rem; padding: 1rem;">
        <p>🤖 Powered by Deep Learning | CNN Model</p>
        <p>Made with ❤️ by Hash-SD</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main app entry point."""
    render_header()
    render_categories()
    render_upload_section()
    render_footer()


if __name__ == "__main__":
    main()
