"""
Download model file from cloud storage.
Supports Google Drive and direct URLs.
"""
import os
import sys
from pathlib import Path

MODEL_DIR = Path("models")
MODEL_FILE = MODEL_DIR / "best_model.keras"

# Google Drive file ID - REPLACE WITH YOUR ACTUAL FILE ID
# To get file ID: Share file > Copy link > Extract ID from URL
# Example URL: https://drive.google.com/file/d/1ABC123xyz/view
# File ID would be: 1ABC123xyz
GDRIVE_FILE_ID = "YOUR_GOOGLE_DRIVE_FILE_ID"


def download_from_gdrive(file_id: str, destination: Path) -> bool:
    """Download file from Google Drive."""
    try:
        import gdown
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, str(destination), quiet=False)
        return destination.exists()
    except ImportError:
        print("Installing gdown...")
        os.system(f"{sys.executable} -m pip install gdown")
        import gdown
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, str(destination), quiet=False)
        return destination.exists()
    except Exception as e:
        print(f"Error: {e}")
        return False


def download_model() -> bool:
    """Download model file."""
    MODEL_DIR.mkdir(exist_ok=True)
    
    # Check if model exists and is valid
    if MODEL_FILE.exists():
        size_mb = MODEL_FILE.stat().st_size / 1024 / 1024
        if size_mb > 50:  # Valid model should be > 50MB
            print(f"✅ Model exists: {size_mb:.1f}MB")
            return True
        else:
            print(f"⚠️ Model file too small ({size_mb:.1f}MB), re-downloading...")
            MODEL_FILE.unlink()
    
    print("📥 Downloading model from Google Drive...")
    
    if GDRIVE_FILE_ID == "YOUR_GOOGLE_DRIVE_FILE_ID":
        print("❌ Please set GDRIVE_FILE_ID in download_model.py")
        print("   1. Upload best_model.keras to Google Drive")
        print("   2. Share file (Anyone with link)")
        print("   3. Copy file ID from share URL")
        print("   4. Replace YOUR_GOOGLE_DRIVE_FILE_ID with actual ID")
        return False
    
    return download_from_gdrive(GDRIVE_FILE_ID, MODEL_FILE)


if __name__ == "__main__":
    print("🤖 ATK Classifier - Model Downloader")
    print("=" * 50)
    
    if download_model():
        print("\n✨ Model ready!")
        print("   Run: streamlit run streamlit_app.py")
    else:
        print("\n❌ Failed to download model")
        sys.exit(1)
