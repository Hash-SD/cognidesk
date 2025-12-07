"""
CogniDesk 🧠 - AI Stationery Detector
Minimalist Modern, Clean Dashboard, Professional
"""
import streamlit as st
from PIL import Image
from pathlib import Path

from app.config import settings
from app.components.predictor import PredictionEngine


# Page configuration - HARUS di baris pertama
st.set_page_config(
    page_title="CogniDesk - AI Stationery Detector",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


def inject_custom_css():
    """Inject CSS untuk CogniDesk - Google Material Design Style."""
    st.markdown("""
    <style>
        /* ============ GOOGLE MATERIAL DESIGN THEME ============ */
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500;700&display=swap');

        /* ============ HIDE STREAMLIT BRANDING ============ */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* ============ ROOT VARIABLES ============ */
        :root {
            --primary: #1a73e8; /* Google Blue */
            --primary-hover: #1557b0;
            --bg-main: #ffffff;
            --bg-surface: #ffffff;
            --text-primary: #202124;
            --text-secondary: #5f6368;
            --border: #dadce0;
            --shadow-card: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
            --shadow-hover: 0 1px 3px 0 rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15);
            --radius: 8px;
        }
        
        /* ============ GLOBAL STYLES ============ */
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
            color: var(--text-primary);
            background-color: var(--bg-main);
        }
        
        h1, h2, h3 {
            font-family: 'Google Sans', sans-serif;
            color: var(--text-primary);
        }

        /* ============ MAIN CONTAINER ============ */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 900px; /* Limit width for better readability like Google Search */
        }

        /* ============ HEADER ============ */
        .main-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .main-title {
            font-family: 'Google Sans', sans-serif;
            font-size: 2.5rem;
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }
        
        .main-subtitle {
            font-family: 'Roboto', sans-serif;
            font-size: 1.1rem;
            color: var(--text-secondary);
            font-weight: 300;
        }

        /* ============ CARDS (MATERIAL STYLE) ============ */
        .material-card {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: box-shadow 0.2s ease-in-out;
        }
        
        .material-card:hover {
            box-shadow: var(--shadow-card);
            border-color: transparent;
        }

        /* ============ BUTTONS ============ */
        .stButton > button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1.5rem;
            font-family: 'Google Sans', sans-serif;
            font-weight: 500;
            font-size: 0.875rem;
            letter-spacing: 0.25px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            transition: background-color 0.2s, box-shadow 0.2s;
        }
        
        .stButton > button:hover {
            background-color: var(--primary-hover);
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            border: none;
        }

        /* ============ FILE UPLOADER ============ */
        .stFileUploader {
            border: 1px dashed var(--border);
            border-radius: var(--radius);
            padding: 2rem;
            text-align: center;
            background-color: #f8f9fa;
        }
        
        .stFileUploader:hover {
            background-color: #f1f3f4;
            border-color: var(--primary);
        }

        /* ============ RESULT CARD ============ */
        .result-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            padding: 2rem;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: white;
        }

        .result-emoji {
            font-size: 4rem;
            margin-bottom: 1rem;
        }

        .result-title {
            font-family: 'Google Sans', sans-serif;
            font-size: 1.5rem;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .result-confidence {
            font-family: 'Roboto', sans-serif;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        /* ============ PROGRESS BAR ============ */
        .stProgress > div > div > div > div {
            background-color: var(--primary);
        }

        /* ============ SIDEBAR ============ */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid var(--border);
        }
        
        [data-testid="stSidebar"] h1 {
            font-size: 1.5rem;
            color: var(--text-primary);
        }

    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar dengan komponen Streamlit native."""
    with st.sidebar:
        # Styled to match the main title (Identifikasi Alat Tulis)
        st.markdown("""
        <div style="font-family: 'Google Sans', sans-serif; font-size: 2.5rem; font-weight: 500; color: #202124; margin-bottom: 0.5rem; line-height: 1.2;">
            🧠 CogniDesk
        </div>
        """, unsafe_allow_html=True)
        
        # Mode Selection
        st.caption("Pengaturan")
        mode = st.radio(
            "Mode Tampilan",
            ["Simple", "Expert"],
            index=0,
            label_visibility="collapsed"
        )
        st.session_state.user_mode = "expert" if mode == "Expert" else "simple"
        
        st.divider()
        
        with st.expander("ℹ️ Tentang Aplikasi"):
            st.markdown("""
            **CogniDesk** menggunakan AI untuk mengenali alat tulis.
            
            **Didukung:**
            - 🧹 Eraser
            - 📄 Kertas
            - ✏️ Pensil
            
            **Versi:** 1.0.0
            """)
        
        st.caption("© 2024 CogniDesk")


@st.cache_resource
def get_prediction_engine():
    """Get cached prediction engine."""
    return PredictionEngine()


def render_main_header():
    """Render main content header - Google Style."""
    st.markdown("""
    <div class="main-header">
        <div class="main-title">Identifikasi Alat Tulis</div>
        <div class="main-subtitle">Powered by CogniDesk AI</div>
    </div>
    """, unsafe_allow_html=True)


def get_emoji_for_class(class_name: str) -> str:
    """Get emoji for predicted class."""
    emoji_map = {"eraser": "🧹", "kertas": "📄", "pensil": "✏️"}
    return emoji_map.get(class_name.lower(), "🏷️")


def get_confidence_class(percentage: float) -> str:
    """Get CSS class based on confidence level."""
    if percentage >= 80:
        return "high"
    elif percentage >= 50:
        return "medium"
    return "low"


def render_analysis_result(result):
    """Render analysis result using native Streamlit components."""
    emoji = get_emoji_for_class(result.predicted_class)
    user_mode = st.session_state.get("user_mode", "simple")
    
    # Clean Result Card
    st.markdown(f"""
    <div class="result-card">
        <div class="result-emoji">{emoji}</div>
        <div class="result-title">{result.predicted_class.title()}</div>
        <div class="result-confidence">{result.percentage:.1f}% Confidence</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Expert Mode Content
    if user_mode == "expert":
        st.markdown("### Detailed Analysis")
        
        for pred in result.top_predictions:
            col_name, col_bar, col_val = st.columns([2, 6, 2])
            with col_name:
                st.write(pred['class'].title())
            with col_bar:
                st.progress(pred["confidence"])
            with col_val:
                st.write(f"{pred['percentage']:.1f}%")
        
        with st.expander("Raw JSON Data"):
            st.json(result.top_predictions)


def render_twin_frames(image: Image.Image, source_name: str):
    """Render twin frames layout - Image & Analysis side by side dengan ukuran tetap."""
    engine = get_prediction_engine()
    
    # Process prediction
    with st.spinner("Analyzing..."):
        result = engine.predict(image, top_k=3)
    
    # Demo mode check
    if result.is_demo:
        st.warning("Demo Mode Active")
        return
    
    # Google-like Result Layout (Card based)
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image, caption="Input Image", use_container_width=True)
        
    with col2:
        render_analysis_result(result)


def render_input_section():
    """Render input section - Google Search Style."""
    
    # Central Action Area
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    
    # Tabs for Upload vs Camera
    tab_upload, tab_camera = st.tabs(["Upload Image", "Use Camera"])
    
    with tab_upload:
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                render_twin_frames(image, uploaded_file.name)
            except Exception:
                st.error("Invalid file format.")
    
    with tab_camera:
        if st.checkbox("Enable Camera"):
            camera_image = st.camera_input("Take a photo", label_visibility="collapsed")
            if camera_image:
                image = Image.open(camera_image)
                render_twin_frames(image, "Camera Capture")
                
    st.markdown('</div>', unsafe_allow_html=True)


def resize_sample_image(img: Image.Image, target_size: tuple = (200, 150)) -> Image.Image:
    """Resize sample image ke ukuran tetap dengan padding untuk menjaga aspek rasio."""
    # Buat canvas dengan ukuran target dan background putih
    canvas = Image.new("RGB", target_size, (255, 255, 255))
    
    # Resize image dengan menjaga aspek rasio
    img_copy = img.copy()
    img_copy.thumbnail(target_size, Image.Resampling.LANCZOS)
    
    # Hitung posisi untuk center image
    x = (target_size[0] - img_copy.width) // 2
    y = (target_size[1] - img_copy.height) // 2
    
    # Paste image ke canvas
    canvas.paste(img_copy, (x, y))
    
    return canvas


def render_sample_section():
    """Render sample images section - Minimalist."""
    st.markdown('<div style="text-align: center; margin-top: 2rem; color: #5f6368;">Or try these examples</div>', unsafe_allow_html=True)
    
    samples_dir = Path("samples")
    if not samples_dir.exists():
        return
    
    col1, col2, col3 = st.columns(3)
    sample_files = {
        "eraser": ("eraser_sample.jpg", "Eraser"),
        "kertas": ("kertas_sample.jpg", "Paper"),
        "pensil": ("pensil_sample.jpg", "Pencil")
    }
    
    SAMPLE_SIZE = (200, 150)
    
    for col, (key, (filename, label)) in zip([col1, col2, col3], sample_files.items()):
        filepath = samples_dir / filename
        if filepath.exists():
            with col:
                if st.button(label, key=f"try_{key}", use_container_width=True):
                    img = Image.open(filepath)
                    render_twin_frames(img, f"Sample: {label}")


def main():
    """Main app entry point."""
    inject_custom_css()
    render_sidebar()
    render_main_header()
    render_input_section()
    render_sample_section()


if __name__ == "__main__":
    main()
