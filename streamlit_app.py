"""
ATK Classifier - Streamlit Entry Point
"""
import sys
from pathlib import Path

# Ensure app directory is in path
root_dir = Path(__file__).parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import and run main app
from app.main import main

if __name__ == "__main__":
    main()
