"""
Download model file from GitHub releases or alternative source.
Run this script to download the trained model before running the app.
"""
import os
import sys
from pathlib import Path
import urllib.request
import json

# Model configuration
MODEL_DIR = Path("models")
MODEL_FILE = MODEL_DIR / "best_model.keras"
MODEL_URL = "https://github.com/Hash-SD/cnn-custom-datagambar/releases/download/v1.0.0/best_model.keras"

def download_model():
    """Download model file from GitHub releases."""
    
    # Create models directory if it doesn't exist
    MODEL_DIR.mkdir(exist_ok=True)
    
    # Check if model already exists
    if MODEL_FILE.exists():
        print(f"✅ Model already exists at {MODEL_FILE}")
        return True
    
    print(f"📥 Downloading model from {MODEL_URL}...")
    print("This may take a few minutes...")
    
    try:
        # Download with progress
        def download_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 // total_size, 100)
            print(f"\r📊 Progress: {percent}% ({downloaded / 1024 / 1024:.1f}MB / {total_size / 1024 / 1024:.1f}MB)", end="")
        
        urllib.request.urlretrieve(MODEL_URL, MODEL_FILE, download_progress)
        print("\n✅ Model downloaded successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading model: {e}")
        print("\nAlternative: Download manually from GitHub releases:")
        print(f"  {MODEL_URL}")
        return False

def verify_model():
    """Verify model file exists and is valid."""
    if not MODEL_FILE.exists():
        print(f"❌ Model file not found at {MODEL_FILE}")
        return False
    
    file_size = MODEL_FILE.stat().st_size / 1024 / 1024
    print(f"✅ Model file verified: {file_size:.1f}MB")
    return True

if __name__ == "__main__":
    print("🤖 ATK Classifier - Model Downloader")
    print("=" * 50)
    
    # Try to download
    if download_model():
        # Verify
        if verify_model():
            print("\n✨ Ready to run the app!")
            print("   Run: streamlit run streamlit_app.py")
            sys.exit(0)
    
    sys.exit(1)
