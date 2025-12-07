"""
Configuration module for ATK Classifier application.
"""
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Settings:
    """Application settings and configuration."""
    
    # Application Info
    APP_NAME: str = "ATK Classifier"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Klasifikasi gambar Alat Tulis Kantor menggunakan CNN"
    
    # Model Configuration
    MODEL_PATH: Path = field(default_factory=lambda: Path("models/best_model.keras"))
    INPUT_SIZE: Tuple[int, int] = (300, 300)  # Sesuai notebook
    NUM_CLASSES: int = 3  # pensil, eraser, kertas
    CLASS_NAMES: List[str] = field(default_factory=lambda: [
        "eraser",
        "kertas", 
        "pensil"
    ])
    
    # Training Configuration
    DATASET_DIR: Path = field(default_factory=lambda: Path("dataset_alat_tulis"))
    BATCH_SIZE: int = 15
    DEFAULT_EPOCHS: int = 15
    VALIDATION_SPLIT: float = 0.1
    
    # Upload Configuration
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB in bytes
    ALLOWED_EXTENSIONS: List[str] = field(default_factory=lambda: [
        "jpg", "jpeg", "png", "bmp"
    ])
    
    # Prediction Configuration
    TOP_K_PREDICTIONS: int = 3
    LOW_CONFIDENCE_THRESHOLD: float = 0.5
    
    # Demo Mode
    DEMO_MODE_MESSAGE: str = "Running in demo mode - predictions are simulated"


# Global settings instance
settings = Settings()
