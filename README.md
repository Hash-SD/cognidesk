# ATK Classifier MLOps

Aplikasi Streamlit untuk klasifikasi gambar Alat Tulis Kantor (ATK) menggunakan Custom CNN dengan fitur MLOps sederhana.

## Features

- Klasifikasi 8 jenis ATK: Spidol, Pensil, Pulpen, Penggaris, Penghapus, Correction Tape, Pensil Mekanik, Tipe X
- Upload gambar atau capture dari kamera
- Dashboard untuk monitoring performa model
- Model version management
- Demo mode untuk testing tanpa model

## Installation

1. Clone repository:
```bash
git clone <repository-url>
cd atk-classifier-mlops
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Training a Model

Before using the application in production mode, you need to train a model:

#### Option 1: Command Line Training (Recommended)

```bash
# Simple training (faster, ~15 minutes)
python train.py dataset_alat_tulis --epochs 15

# With hyperparameter tuning (better results, ~1-2 hours)
python train.py dataset_alat_tulis --tune --epochs 25 --trials 10

# Custom configuration
python train.py dataset_alat_tulis --epochs 20 --img-size 300 --batch-size 15 --output models/my_model.h5
```

**Training Options:**
- `--tune`: Enable hyperparameter tuning (searches for best model architecture)
- `--epochs`: Number of training epochs (default: 15)
- `--trials`: Number of tuning trials when using --tune (default: 10)
- `--img-size`: Input image size, 224 or 300 (default: 300)
- `--batch-size`: Batch size for training (default: 15)
- `--output`: Output path for model file (default: models/best_model.h5)

#### Option 2: Streamlit UI Training

1. Run the app: `streamlit run app/main.py`
2. Navigate to "🚀 Training" page
3. Configure dataset path and training parameters
4. Click "Start Training" and monitor progress

### Dataset Structure

Organize your dataset as follows:
```
dataset_alat_tulis/
├── Spidol/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Pensil/
│   ├── image1.jpg
│   └── ...
├── Pulpen/
│   └── ...
└── ... (other ATK classes)
```

### Running the Application

```bash
streamlit run app/main.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
atk-classifier-mlops/
├── app/
│   ├── __init__.py
│   ├── config.py           # Application configuration
│   ├── main.py             # Main Streamlit entry point
│   ├── components/         # Reusable UI components
│   │   ├── __init__.py
│   │   ├── image_uploader.py
│   │   ├── predictor.py
│   │   └── visualizer.py
│   └── pages/              # Streamlit pages
│       ├── __init__.py
│       ├── home.py
│       ├── predict.py
│       ├── training.py
│       ├── dashboard.py
│       └── model_management.py
├── models/
│   ├── __init__.py
│   ├── preprocessing.py    # Image preprocessing
│   ├── cnn_model.py        # CNN model architecture
│   ├── inference.py        # Inference pipeline
│   └── train_model.py      # Model training with hyperparameter tuning
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py
│   └── test_cnn_model.py
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── train.py                # Standalone training script
├── requirements.txt
├── .gitignore
└── README.md
```

## Demo Mode

If no trained model is available at `models/best_model.h5`, the application runs in demo mode with simulated predictions.

## Deployment

Deploy to Streamlit Cloud:
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Set main file path to `app/main.py`

## License

MIT License
