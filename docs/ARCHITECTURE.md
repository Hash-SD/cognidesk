# 🏗️ Architecture Documentation

## Model Architecture

```
Input (300x300x3)
    ↓
Rescaling Layer (0-1 normalization)
    ↓
Conv2D (32 filters, 3x3) → ReLU → MaxPool
    ↓
Conv2D (64 filters, 3x3) → ReLU → MaxPool
    ↓
Conv2D (128 filters, 3x3) → ReLU → MaxPool
    ↓
Flatten
    ↓
Dense (128) → ReLU → Dropout (0.5)
    ↓
Dense (3, softmax) → Output
```

## Project Structure

```
├── app/                    # Streamlit application
│   ├── main.py            # Main entry point
│   ├── config.py          # Configuration
│   └── components/        # UI components
│       ├── predictor.py   # Prediction engine
│       └── image_uploader.py
├── models/                 # ML models
│   ├── cnn_model.py       # CNN architecture
│   ├── inference.py       # Inference pipeline
│   └── preprocessing.py   # Image preprocessing
├── tests/                  # Unit tests
├── samples/               # Sample images
├── docs/                  # Documentation
└── streamlit_app.py       # Cloud entry point
```

## Data Flow

1. **Input**: User uploads image via Streamlit
2. **Preprocessing**: Image resized to 300x300, converted to RGB
3. **Inference**: Model predicts class probabilities
4. **Output**: Top-K predictions with confidence scores

## Classes

| Class | Description |
|-------|-------------|
| eraser | Penghapus |
| kertas | Paper |
| pensil | Pencil |
