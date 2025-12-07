# Design Document: ATK Classifier MLOps

## Overview

Aplikasi Streamlit untuk klasifikasi gambar Alat Tulis Kantor (ATK) dengan arsitektur modular. Sistem menggunakan Custom CNN untuk mengklasifikasi 8 jenis ATK dengan interface multi-page yang clean. Aplikasi mendukung demo mode untuk testing tanpa model dan production mode dengan model terlatih.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐  │
│  │   Home   │ │ Predict  │ │Dashboard │ │Model Management│  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Components Layer                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │Image Uploader│ │  Predictor   │ │    Visualizer        │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Models Layer                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │Preprocessing │ │  CNN Model   │ │    Inference         │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Configuration Module (app/config.py)

```python
class Settings:
    APP_NAME: str = "ATK Classifier"
    APP_VERSION: str = "1.0.0"
    MODEL_PATH: Path = Path("models/best_model.h5")
    INPUT_SIZE: tuple = (224, 224)
    NUM_CLASSES: int = 8
    CLASS_NAMES: list = ["Spidol", "Pensil", "Pulpen", "Penggaris", 
                         "Penghapus", "Correction Tape", "Pensil Mekanik", "Tipe X"]
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: list = ["jpg", "jpeg", "png", "bmp"]
```

### 2. Preprocessing Module (models/preprocessing.py)

```python
class ImagePreprocessor:
    def __init__(self, input_size: tuple = (224, 224))
    def load_image(image_source) -> PIL.Image
    def resize_image(image: PIL.Image) -> PIL.Image
    def normalize_image(image: PIL.Image) -> np.ndarray
    def preprocess(image) -> np.ndarray  # Returns (1, 224, 224, 3)

class ImageValidator:
    def validate_file_size(file_size: int, max_size: int) -> bool
    def validate_extension(filename: str, allowed: list) -> bool
    def get_image_info(image: PIL.Image) -> dict
```

### 3. Model Module (models/cnn_model.py)

```python
class ATKClassifier:
    @staticmethod
    def build_model(input_shape: tuple, num_classes: int) -> keras.Model
    
class ModelPredictor:
    def __init__(self, model_path: str = None)
    def predict(preprocessed_image: np.ndarray, top_k: int = 3) -> dict
    def is_demo_mode() -> bool
```

### 4. Streamlit Pages

| Page | File | Description |
|------|------|-------------|
| Home | pages/home.py | Landing page dengan overview dan quick actions |
| Predict | pages/predict.py | Upload/capture gambar dan lihat hasil prediksi |
| Dashboard | pages/dashboard.py | Metrics dan visualisasi performa model |
| Model Management | pages/model_management.py | Version tracking dan comparison |

## Data Models

### PredictionResult
```python
@dataclass
class PredictionResult:
    predicted_class: str
    confidence: float
    percentage: float
    top_predictions: List[dict]  # [{"class": str, "confidence": float, "percentage": float}]
    is_demo: bool
    is_low_confidence: bool  # True if confidence < 0.5
```

### ImageInfo
```python
@dataclass
class ImageInfo:
    width: int
    height: int
    format: str
    size_kb: float
```

### ModelMetrics
```python
@dataclass
class ModelMetrics:
    version: str
    accuracy: float
    loss: float
    f1_score: float
    created_date: str
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: File Validation Correctness
*For any* file with size and extension, the validator SHALL accept files with allowed extensions (.jpg, .jpeg, .png, .bmp) AND size <= 5MB, and reject all others.
**Validates: Requirements 1.1**

### Property 2: Image Info Extraction
*For any* valid image, the info extractor SHALL return correct width, height, and format matching the actual image properties.
**Validates: Requirements 1.3**

### Property 3: Prediction Output Validity
*For any* valid preprocessed image, the predictor SHALL return a class name from the valid CLASS_NAMES list and confidence in range [0, 1].
**Validates: Requirements 2.1**

### Property 4: Top-K Predictions Ordering
*For any* prediction result with top-K predictions, the predictions SHALL be sorted in descending order by confidence, and all confidences SHALL sum to <= 1.
**Validates: Requirements 2.2**

### Property 5: Low Confidence Detection
*For any* prediction with confidence value, the is_low_confidence flag SHALL be True if and only if confidence < 0.5.
**Validates: Requirements 2.3**

### Property 6: Resize Output Dimensions
*For any* input image of any dimensions, after preprocessing the output SHALL have exactly shape (1, 224, 224, 3).
**Validates: Requirements 3.1**

### Property 7: Normalization Range
*For any* preprocessed image array, all pixel values SHALL be in the range [0.0, 1.0].
**Validates: Requirements 3.2**

### Property 8: RGB Channel Count
*For any* input image (grayscale, RGBA, or RGB), after preprocessing the output SHALL have exactly 3 color channels.
**Validates: Requirements 3.3**

## Error Handling

| Error Type | Handling Strategy |
|------------|-------------------|
| File too large | Display error message, reject upload |
| Invalid extension | Display error message, reject upload |
| Model not found | Switch to demo mode, show indicator |
| Prediction error | Display error message, suggest retry |
| Camera unavailable | Show warning, suggest file upload |

## Testing Strategy

### Unit Tests
- Test file validation with various sizes and extensions
- Test image preprocessing with different input formats
- Test prediction output structure and values

### Property-Based Tests
Using **Hypothesis** library for Python property-based testing.

Each property test will:
1. Generate random valid inputs using Hypothesis strategies
2. Execute the function under test
3. Assert the property holds for all generated inputs
4. Run minimum 100 iterations per property

Test annotations format:
```python
# **Feature: atk-classifier-mlops, Property {N}: {property_text}**
# **Validates: Requirements X.Y**
```
