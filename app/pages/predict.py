"""
Predict page for ATK Classifier application.
Provides prediction interface with upload/camera options.
"""
import streamlit as st

from app.config import settings
from app.components.image_uploader import ImageUploader
from app.components.predictor import PredictionEngine, display_results


def render_header() -> None:
    """Render the page header."""
    st.title("🎯 Predict")
    st.markdown("Upload atau capture gambar ATK untuk klasifikasi")


def render_demo_mode_banner(is_demo: bool) -> None:
    """Render demo mode banner if applicable."""
    if is_demo:
        st.warning(
            "⚠️ **Demo Mode** - Predictions are simulated. "
            "Add a trained model to get real predictions."
        )


def render_input_method_selector() -> str:
    """
    Render input method selector.
    
    Returns:
        Selected input method ('upload' or 'camera')
    """
    st.markdown("### 📥 Input Method")
    
    method = st.radio(
        "Choose input method:",
        options=["Upload File", "Camera Capture"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    return "upload" if method == "Upload File" else "camera"


def render_upload_section(uploader: ImageUploader) -> None:
    """
    Render file upload section and handle prediction.
    
    Args:
        uploader: ImageUploader instance
    """
    result = uploader.render_file_upload(key="predict_upload")
    
    if result is not None:
        if result.is_valid and result.image is not None:
            # Display image preview
            uploader.display_image_preview(result)
            
            # Run prediction
            st.markdown("---")
            run_prediction(result.image)
        else:
            st.error(f"❌ {result.error_message}")


def render_camera_section(uploader: ImageUploader) -> None:
    """
    Render camera capture section and handle prediction.
    
    Args:
        uploader: ImageUploader instance
    """
    st.info("📷 Use your device camera to capture an image of ATK")
    
    result = uploader.render_camera_capture(key="predict_camera")
    
    if result is not None:
        if result.is_valid and result.image is not None:
            # Display image preview
            uploader.display_image_preview(result)
            
            # Run prediction
            st.markdown("---")
            run_prediction(result.image)
        else:
            st.error(f"❌ {result.error_message}")


def run_prediction(image) -> None:
    """
    Run prediction on the provided image.
    
    Args:
        image: PIL Image to classify
    """
    engine = PredictionEngine()
    
    with st.spinner("🔄 Running prediction..."):
        prediction_result = engine.predict(image, top_k=settings.TOP_K_PREDICTIONS)
    
    # Display results
    display_results(prediction_result)


def render_tips() -> None:
    """Render tips for better predictions."""
    with st.expander("💡 Tips for Better Predictions"):
        st.markdown("""
        - **Good Lighting** - Pastikan gambar memiliki pencahayaan yang cukup
        - **Clear Focus** - Gambar harus fokus dan tidak blur
        - **Single Object** - Idealnya satu objek ATK per gambar
        - **Centered** - Posisikan objek di tengah frame
        - **Plain Background** - Background polos membantu akurasi
        """)


def render() -> None:
    """Main render function for predict page."""
    # Initialize components
    engine = PredictionEngine()
    uploader = ImageUploader()
    
    # Render page
    render_header()
    render_demo_mode_banner(engine.is_demo_mode())
    
    st.markdown("---")
    
    # Input method selection
    input_method = render_input_method_selector()
    
    st.markdown("---")
    
    # Render appropriate input section
    if input_method == "upload":
        render_upload_section(uploader)
    else:
        render_camera_section(uploader)
    
    # Tips section
    st.markdown("---")
    render_tips()


if __name__ == "__main__":
    render()
