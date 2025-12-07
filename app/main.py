"""
ATK Classifier - Simple and Clean Interface
"""
import streamlit as st
from PIL import Image
from pathlib import Path

from app.config import settings
from app.components.predictor import PredictionEngine


# Page configuration
st.set_page_config(
    page_title="ATK Classifier",
    page_icon="✏️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .category-card {
        text-align: center;
        padding: 1.2rem;
        background: #f8f9fa;
        border-radius: 12px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .category-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
    }
    .result-card {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .sample-btn {
        width: 100%;
        padding: 0.5rem;
        border-radius: 8px;
    }
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_prediction_engine():
    """Get cached prediction engine."""
    return PredictionEngine()


def render_header():
    """Render app header."""
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0;">✏️ ATK Classifier</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            Klasifikasi Alat Tulis Kantor dengan AI
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_categories():
    """Show supported categories as clickable cards."""
    st.markdown("#### 🏷️ Kategori yang Didukung")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="category-card">
            <div style="font-size: 2.5rem;">🧹</div>
            <div style="font-weight: bold; font-size: 1.1rem;">Eraser</div>
            <div style="color: #666; font-size: 0.85rem;">Penghapus</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="category-card">
            <div style="font-size: 2.5rem;">📄</div>
            <div style="font-weight: bold; font-size: 1.1rem;">Kertas</div>
            <div style="color: #666; font-size: 0.85rem;">Paper</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="category-card">
            <div style="font-size: 2.5rem;">✏️</div>
            <div style="font-weight: bold; font-size: 1.1rem;">Pensil</div>
            <div style="color: #666; font-size: 0.85rem;">Pencil</div>
        </div>
        """, unsafe_allow_html=True)


def render_sample_images():
    """Render sample images that users can try."""
    st.markdown("---")
    st.markdown("#### 🎯 Coba Contoh Gambar")
    st.caption("Klik salah satu untuk langsung mencoba")
    
    samples_dir = Path("samples")
    
    # Check if samples exist
    if not samples_dir.exists():
        return
    
    col1, col2, col3 = st.columns(3)
    
    sample_files = {
        "eraser": samples_dir / "eraser_sample.jpg",
        "kertas": samples_dir / "kertas_sample.jpg",
        "pensil": samples_dir / "pensil_sample.jpg"
    }
    
    with col1:
        if sample_files["eraser"].exists():
            img = Image.open(sample_files["eraser"])
            st.image(img, caption="Eraser", use_container_width=True)
            if st.button("🧹 Coba Eraser", use_container_width=True, key="try_eraser"):
                st.session_state.selected_sample = "eraser"
                st.session_state.sample_image = img
    
    with col2:
        if sample_files["kertas"].exists():
            img = Image.open(sample_files["kertas"])
            st.image(img, caption="Kertas", use_container_width=True)
            if st.button("📄 Coba Kertas", use_container_width=True, key="try_kertas"):
                st.session_state.selected_sample = "kertas"
                st.session_state.sample_image = img
    
    with col3:
        if sample_files["pensil"].exists():
            img = Image.open(sample_files["pensil"])
            st.image(img, caption="Pensil", use_container_width=True)
            if st.button("✏️ Coba Pensil", use_container_width=True, key="try_pensil"):
                st.session_state.selected_sample = "pensil"
                st.session_state.sample_image = img
    
    # Process selected sample
    if "sample_image" in st.session_state and st.session_state.sample_image is not None:
        st.markdown("---")
        process_image(st.session_state.sample_image, f"Contoh {st.session_state.selected_sample}")
        # Clear after processing
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.sample_image = None
            st.session_state.selected_sample = None
            st.rerun()


def render_upload_section():
    """Render image upload section."""
    st.markdown("---")
    st.markdown("#### 📸 Upload Gambar Anda")
    
    tab1, tab2 = st.tabs(["📁 Upload File", "📷 Kamera"])
    
    with tab1:
        uploaded_file = st.file_uploader(
            "Pilih gambar ATK",
            type=["jpg", "jpeg", "png"],
            help="Format: JPG, JPEG, PNG. Max: 5MB",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            process_image(image, uploaded_file.name)
    
    with tab2:
        st.caption("Gunakan kamera untuk mengambil foto ATK")
        camera_image = st.camera_input(
            "Ambil foto",
            label_visibility="collapsed"
        )
        
        if camera_image:
            image = Image.open(camera_image)
            process_image(image, "Camera Capture")


def process_image(image: Image.Image, source_name: str = ""):
    """Process and predict image."""
    try:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption=f"📷 {source_name}", use_container_width=True)
        
        with col2:
            engine = get_prediction_engine()
            
            with st.spinner("🔄 Menganalisis gambar..."):
                result = engine.predict(image, top_k=3)
            
            # Demo mode warning
            if result.is_demo:
                st.warning("⚠️ Mode Demo - Model sedang dimuat")
                return
            
            # Get emoji for result
            emoji_map = {"eraser": "🧹", "kertas": "📄", "pensil": "✏️"}
            result_emoji = emoji_map.get(result.predicted_class.lower(), "🏷️")
            
            # Main result card
            color = "#11998e" if not result.is_low_confidence else "#f39c12"
            st.markdown(f"""
            <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {color} 0%, #38ef7d 100%); border-radius: 15px; color: white;">
                <div style="font-size: 3rem;">{result_emoji}</div>
                <div style="font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0;">
                    {result.predicted_class.upper()}
                </div>
                <div style="font-size: 1.3rem; opacity: 0.95;">
                    Confidence: {result.percentage:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Low confidence warning
            if result.is_low_confidence:
                st.warning("⚠️ Confidence rendah - coba dengan gambar yang lebih jelas")
            
            # All predictions
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**📊 Detail Prediksi:**")
            
            for pred in result.top_predictions:
                emoji = emoji_map.get(pred["class"].lower(), "🏷️")
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.progress(pred["confidence"])
                with col_b:
                    st.write(f"{emoji} {pred['percentage']:.1f}%")
                    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def render_tips():
    """Render tips for better results."""
    with st.expander("💡 Tips untuk Hasil Terbaik"):
        st.markdown("""
        - **Pencahayaan**: Pastikan gambar terang dan jelas
        - **Fokus**: Objek ATK harus fokus, tidak blur
        - **Background**: Gunakan background polos jika memungkinkan
        - **Posisi**: Letakkan objek di tengah frame
        - **Satu Objek**: Idealnya satu objek ATK per gambar
        """)


def render_footer():
    """Render footer."""
    st.markdown("""
    <div class="footer">
        <p>🤖 Powered by Deep Learning | CNN Model</p>
        <p>Made with ❤️ by <a href="https://github.com/Hash-SD" target="_blank">Hash-SD</a></p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main app entry point."""
    render_header()
    render_categories()
    render_sample_images()
    render_upload_section()
    render_tips()
    render_footer()


if __name__ == "__main__":
    main()
