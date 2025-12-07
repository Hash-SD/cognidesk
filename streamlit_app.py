"""
ATK Classifier - Streamlit Cloud Entry Point
Automatically handles model download if needed.
"""
import sys
from pathlib import Path

# Ensure app directory is in path
root_dir = Path(__file__).parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Check and download model if needed
def ensure_model_exists():
    """Ensure model file exists, download if necessary."""
    model_path = Path("models/best_model.keras")
    
    if not model_path.exists():
        import streamlit as st
        st.warning("⏳ Downloading model for first time... This may take a minute.")
        
        try:
            from download_model import download_model
            if not download_model():
                st.error("Failed to download model. Please try again.")
                st.stop()
        except Exception as e:
            st.error(f"Error downloading model: {e}")
            st.stop()

# Ensure model exists before importing main app
ensure_model_exists()

# Import and run main app
from app.main import main

if __name__ == "__main__":
    main()
