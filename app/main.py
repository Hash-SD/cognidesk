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
    """Inject CSS untuk CogniDesk - Minimalist Modern Dashboard."""
    st.markdown("""
    <style>
        /* ============ HIDE STREAMLIT BRANDING ============ */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* ============ ROOT VARIABLES ============ */
        :root {
            --primary: #2563EB; /* Modern Blue */
            --primary-light: #60A5FA;
            --accent: #10B981; /* Emerald */
            --success: #059669;
            --warning: #D97706;
            --danger: #DC2626;
            --bg-main: #F3F4F6; /* Cool Gray 100 */
            --bg-surface: #FFFFFF;
            --bg-sidebar: #F9FAFB; /* Cool Gray 50 */
            --text-primary: #111827; /* Cool Gray 900 */
            --text-secondary: #4B5563; /* Cool Gray 600 */
            --text-muted: #9CA3AF; /* Cool Gray 400 */
            --border: #E5E7EB;
            --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 1rem;
        }
        
        /* ============ MAIN LAYOUT ============ */
        .main {
            background: var(--bg-main);
        }
        
        .block-container {
            padding: 1.5rem 2rem 2rem 2rem;
            max-width: 100%;
        }
        

        
        /* ============ MAIN HEADER ============ */
        .main-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .main-title {
            font-size: clamp(1.5rem, 4vw, 2.2rem);
            font-weight: 800;
            color: var(--text-primary);
            margin: 0 0 0.5rem 0;
        }
        
        .main-subtitle {
            font-size: clamp(0.9rem, 2vw, 1rem);
            color: var(--text-secondary);
            margin: 0;
        }
        
        /* ============ INPUT METHOD CARDS ============ */
        .input-cards-container {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        
        .input-card {
            background: var(--bg-surface);
            border: 2px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 2rem 3rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 180px;
            flex: 1;
            max-width: 250px;
        }
        
        .input-card:hover {
            border-color: var(--primary);
            box-shadow: 0 8px 25px var(--shadow);
            transform: translateY(-3px);
        }
        
        .input-card-icon {
            font-size: 3rem;
            margin-bottom: 0.8rem;
        }
        
        .input-card-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        /* ============ TWIN FRAMES (RESULT SECTION) ============ */
        .twin-frames {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-top: 2rem;
        }
        
        .frame {
            background: var(--bg-surface);
            border-radius: var(--radius-lg);
            box-shadow: 0 4px 20px var(--shadow);
            overflow: hidden;
            min-height: 350px;
            display: flex;
            flex-direction: column;
        }
        
        .frame-header {
            padding: 0.8rem 1rem;
            background: var(--bg-sidebar);
            border-bottom: 1px solid var(--border);
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .frame-content {
            padding: 1.5rem;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        /* ============ IMAGE FRAME ============ */
        .image-frame img {
            max-width: 100%;
            max-height: 280px;
            object-fit: contain;
            border-radius: var(--radius-md);
        }
        
        /* ============ ANALYSIS FRAME ============ */
        .analysis-result {
            text-align: center;
            width: 100%;
        }
        
        .result-emoji {
            font-size: 4rem;
            margin-bottom: 0.5rem;
        }
        
        .result-label {
            font-size: clamp(1.5rem, 3vw, 2rem);
            font-weight: 800;
            color: var(--success);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        
        .result-label.warning {
            color: var(--warning);
        }
        
        .confidence-container {
            margin: 1.5rem 0;
            width: 100%;
        }
        
        .confidence-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
        }
        
        .confidence-text {
            color: var(--text-secondary);
        }
        
        .confidence-value {
            font-weight: 700;
            color: var(--success);
        }
        
        .confidence-bar-bg {
            height: 12px;
            background: var(--border);
            border-radius: 6px;
            overflow: hidden;
        }
        
        .confidence-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
            border-radius: 6px;
            transition: width 0.5s ease;
        }
        
        .confidence-bar-fill.high {
            background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
        }
        
        .confidence-bar-fill.medium {
            background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 100%);
        }
        
        .confidence-bar-fill.low {
            background: linear-gradient(90deg, #EF4444 0%, #F87171 100%);
        }
        
        /* ============ DETAIL PREDICTIONS ============ */
        .detail-predictions {
            width: 100%;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }
        
        .detail-title {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.8rem;
        }
        
        .detail-item {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 0.6rem;
            font-size: 0.9rem;
        }
        
        .detail-item-emoji {
            font-size: 1.2rem;
        }
        
        .detail-item-name {
            flex: 1;
            color: var(--text-primary);
        }
        
        .detail-item-value {
            font-weight: 600;
        }
        
        /* ============ PLACEHOLDER STATE ============ */
        .placeholder-state {
            text-align: center;
            color: var(--text-muted);
            padding: 2rem;
        }
        
        .placeholder-icon {
            font-size: 4rem;
            opacity: 0.3;
            margin-bottom: 1rem;
        }
        
        .placeholder-text {
            font-size: 0.95rem;
        }
        
        /* ============ BUTTONS ============ */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: white;
            border: none;
            border-radius: var(--radius-md);
            padding: 0.7rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(14, 76, 146, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(14, 76, 146, 0.4);
        }
        
        /* ============ TABS ============ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: var(--bg-sidebar);
            border-radius: var(--radius-md);
            padding: 4px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: var(--radius-sm);
            padding: 0.6rem 1.2rem;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--bg-surface);
            box-shadow: 0 2px 8px var(--shadow);
        }
        
        /* ============ FILE UPLOADER ============ */
        .stFileUploader {
            background: var(--bg-surface);
            border: 2px dashed var(--border);
            border-radius: var(--radius-md);
            padding: 1rem;
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: var(--primary);
        }
        
        /* ============ EXPANDER ============ */
        .streamlit-expanderHeader {
            background: var(--bg-surface);
            border-radius: var(--radius-md);
            font-weight: 600;
        }
        
        /* ============ ALERTS ============ */
        .stAlert {
            border-radius: var(--radius-md);
        }
        
        /* ============ RESPONSIVE - MOBILE ============ */
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar dengan komponen Streamlit native."""
    with st.sidebar:
        # Logo Header - Besar
        st.markdown("# 🧠 CogniDesk")
        st.caption("AI Stationery Detector")
        
        st.divider()

        # Mode Selection
        st.subheader("Pengaturan Tampilan")
        mode = st.radio(
            "Mode Pengguna",
            ["Pemula (Simple)", "Ahli (Expert)"],
            index=0,
            help="Pilih 'Pemula' untuk tampilan sederhana atau 'Ahli' untuk detail teknis."
        )
        st.session_state.user_mode = "expert" if "Ahli" in mode else "simple"
        
        st.divider()
        
        # Panduan Section
        st.subheader("Panduan Input")
        
        with st.expander("Cara Mendapatkan Hasil Terbaik", expanded=False):
            st.markdown("""
            **Tips Foto:**
            - 💡 Gunakan pencahayaan yang cukup
            - 📸 Pastikan objek tidak blur
            - ⬜ Gunakan background polos
            - 🎯 Posisikan objek di tengah frame
            
            **Format File:**
            - JPG, JPEG, atau PNG
            - Maksimal ukuran 5MB
            - Satu objek per gambar
            """)
        
        st.divider()
        
        # Kategori yang Didukung - tanpa emoji, hanya bullet points
        st.subheader("Kategori Didukung")
        st.markdown("""
        - Eraser (Penghapus)
        - Kertas (Paper)
        - Pensil (Pencil)
        """)
        
        st.divider()
        
        # Tim Pengembang - tanpa emoji, hanya bullet points
        st.subheader("Tim Pengembang")
        st.markdown("""
        - Izza
        - Haikal
        - Hermawan
        """)
        
        st.divider()
        
        # Footer
        st.caption("© 2024 CogniDesk v1.0")


@st.cache_resource
def get_prediction_engine():
    """Get cached prediction engine."""
    return PredictionEngine()


def render_main_header():
    """Render main content header - rata kiri."""
    st.title("Identifikasi Alat Tulis")
    st.markdown("""
    Selamat datang di **CogniDesk**! 👋
    
    Aplikasi ini membantu Anda mengenali jenis alat tulis (Penghapus, Kertas, Pensil) menggunakan kecerdasan buatan.
    Silakan upload gambar atau ambil foto langsung.
    """)


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
    
    # Main emoji - centered
    st.markdown(f"<div style='text-align:center; font-size:5rem; padding:1rem 0; animation: bounce 1s infinite alternate;'>{emoji}</div>", unsafe_allow_html=True)
    
    # Result label
    if result.percentage >= 50:
        st.success(f"Sepertinya ini adalah **{result.predicted_class.upper()}**")
    else:
        st.warning(f"Kemungkinan ini adalah **{result.predicted_class.upper()}**")
    
    # Simple Mode Content
    if user_mode == "simple":
        st.write("Tingkat Keyakinan:")
        if result.percentage >= 80:
            st.progress(result.confidence, text="Sangat Yakin")
        elif result.percentage >= 50:
            st.progress(result.confidence, text="Cukup Yakin")
        else:
            st.progress(result.confidence, text="Kurang Yakin")
            st.info("💡 Tips: Coba ambil foto dengan pencahayaan yang lebih baik atau background yang lebih bersih.")

    # Expert Mode Content
    else:
        st.write(f"**Confidence Score:** {result.percentage:.2f}%")
        st.progress(result.confidence)
        
        st.divider()
        
        # All predictions with progress bars
        st.write("**Distribusi Probabilitas (Softmax):**")
        
        for pred in result.top_predictions:
            pct = pred["percentage"]
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.progress(pred["confidence"])
            with col_b:
                st.write(f"{pred['class']}: {pct:.2f}%")
        
        st.divider()
        with st.expander("🔍 Debug Info (JSON)"):
            st.json({
                "predicted_class": result.predicted_class,
                "confidence": result.confidence,
                "is_low_confidence": result.is_low_confidence,
                "raw_predictions": result.top_predictions
            })


def render_twin_frames(image: Image.Image, source_name: str):
    """Render twin frames layout - Image & Analysis side by side dengan ukuran tetap."""
    engine = get_prediction_engine()
    
    # Process prediction
    with st.spinner("Menganalisis gambar..."):
        result = engine.predict(image, top_k=3)
    
    # Demo mode check
    if result.is_demo:
        st.warning("Mode Demo - Model sedang dimuat, hasil adalah simulasi")
        return
    
    # Twin Frames Layout
    col_image, col_analysis = st.columns(2)
    
    with col_image:
        st.subheader("Input Gambar")
        # Container dengan ukuran tetap untuk gambar
        st.markdown("""
        <style>
        .fixed-image-container {
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f8f9fa;
            border-radius: 8px;
            overflow: hidden;
        }
        .fixed-image-container img {
            max-height: 280px;
            max-width: 100%;
            object-fit: contain;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Resize image untuk konsistensi
        img_display = image.copy()
        img_display.thumbnail((400, 280), Image.Resampling.LANCZOS)
        st.image(img_display, caption=source_name, use_container_width=True)
    
    with col_analysis:
        st.subheader("Hasil Analisis")
        render_analysis_result(result)
        
        # Low confidence warning
        if result.is_low_confidence:
            st.warning("Confidence rendah - coba gunakan gambar yang lebih jelas")


def render_input_section():
    """Render input section with tabs."""
    tab_upload, tab_camera = st.tabs(["Upload File", "Ambil Foto"])
    
    with tab_upload:
        st.info("ℹ️ **Tips:** Gunakan gambar yang jelas dengan satu objek utama.")
        
        uploaded_file = st.file_uploader(
            "Pilih gambar dari perangkat Anda",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=False,
            help="Format yang didukung: JPG, JPEG, PNG. Maksimal 5MB.",
            label_visibility="visible"
        )
        
        if uploaded_file:
            # Validasi ukuran file (5MB = 5 * 1024 * 1024 bytes)
            max_size = 5 * 1024 * 1024
            if uploaded_file.size > max_size:
                st.error(f"⚠️ Ukuran file terlalu besar ({uploaded_file.size / (1024*1024):.1f}MB). Maksimal 5MB.")
            else:
                try:
                    image = Image.open(uploaded_file)
                    st.markdown("---")
                    render_twin_frames(image, uploaded_file.name)
                except Exception:
                    st.error("❌ File tidak valid. Pastikan format gambar JPG atau PNG.")
        else:
            # Placeholder state
            st.markdown("""
            <div class="placeholder-state">
                <div class="placeholder-icon">📁</div>
                <div class="placeholder-text">Belum ada gambar yang dipilih.<br>Silakan upload gambar untuk memulai analisis.</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab_camera:
        # Initialize session state untuk camera
        if "camera_enabled" not in st.session_state:
            st.session_state.camera_enabled = False
        
        # Tombol untuk mengaktifkan kamera (lazy loading)
        if not st.session_state.camera_enabled:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <p>Gunakan kamera perangkat Anda untuk mengambil foto langsung.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📸 Aktifkan Kamera", use_container_width=True):
                st.session_state.camera_enabled = True
                st.rerun()
        else:
            # CSS untuk mengatur ukuran kamera
            st.markdown("""
            <style>
            /* Atur ukuran container kamera */
            [data-testid="stCameraInput"] > div {
                width: 100%;
                max-width: 100%;
            }
            [data-testid="stCameraInput"] video {
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            </style>
            """, unsafe_allow_html=True)
            
            col_cam_action, col_cam_close = st.columns([3, 1])
            with col_cam_close:
                # Tombol untuk menonaktifkan kamera
                if st.button("❌ Tutup", use_container_width=True):
                    st.session_state.camera_enabled = False
                    st.rerun()
            
            st.caption("Arahkan kamera ke alat tulis dan klik tombol capture di bawah")
            
            # Camera input dengan ukuran terbatas
            camera_image = st.camera_input(
                "Ambil foto",
                label_visibility="collapsed"
            )
            
            if camera_image:
                try:
                    image = Image.open(camera_image)
                    st.markdown("---")
                    render_twin_frames(image, "Camera Capture")
                except Exception:
                    st.error("❌ Gagal memproses foto. Silakan coba lagi.")


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
    """Render sample images section dengan ukuran gambar yang sama."""
    with st.expander("🧪 Coba dengan Contoh Gambar (Demo)"):
        st.markdown("Tidak punya gambar? Coba salah satu gambar di bawah ini:")
        samples_dir = Path("samples")
        
        if not samples_dir.exists():
            st.info("Folder samples tidak ditemukan")
            return
        
        col1, col2, col3 = st.columns(3)
        
        sample_files = {
            "eraser": ("eraser_sample.jpg", "Eraser"),
            "kertas": ("kertas_sample.jpg", "Kertas"),
            "pensil": ("pensil_sample.jpg", "Pensil")
        }
        
        # Ukuran tetap untuk semua sample images
        SAMPLE_SIZE = (200, 150)
        
        for col, (key, (filename, label)) in zip([col1, col2, col3], sample_files.items()):
            filepath = samples_dir / filename
            if filepath.exists():
                with col:
                    img = Image.open(filepath)
                    # Resize ke ukuran yang sama
                    img_resized = resize_sample_image(img, SAMPLE_SIZE)
                    st.image(img_resized, caption=label, use_container_width=True)
                    if st.button(f"Pilih {label}", key=f"try_{key}", use_container_width=True):
                        st.session_state.selected_sample = key
                        st.session_state.sample_image = img  # Simpan gambar asli untuk prediksi
        
        # Process selected sample
        if "sample_image" in st.session_state and st.session_state.sample_image is not None:
            st.markdown("---")
            render_twin_frames(
                st.session_state.sample_image,
                f"Sample: {st.session_state.selected_sample}"
            )
            if st.button("🔄 Reset Pilihan", use_container_width=True):
                st.session_state.sample_image = None
                st.session_state.selected_sample = None
                st.rerun()


def main():
    """Main app entry point."""
    inject_custom_css()
    render_sidebar()
    render_main_header()
    render_input_section()
    render_sample_section()


if __name__ == "__main__":
    main()
