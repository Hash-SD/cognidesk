# 🏷️ ATK Classifier - Smart Office Supply Recognition

> Klasifikasi cerdas Alat Tulis Kantor menggunakan AI dan Deep Learning

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://atk-classifier-ai.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange.svg)](https://tensorflow.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Tentang Aplikasi

ATK Classifier adalah aplikasi berbasis AI yang menggunakan Convolutional Neural Network (CNN) untuk mengidentifikasi dan mengklasifikasi jenis-jenis Alat Tulis Kantor secara otomatis. Aplikasi ini dirancang untuk membantu inventarisasi, kategorisasi, dan manajemen stok ATK dengan cepat dan akurat.

## � Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🎥 **Prediksi Real-time** | Upload atau capture gambar ATK untuk klasifikasi instan |
| 📊 **Dashboard Analytics** | Monitor performa model dengan visualisasi interaktif |
| � **Moodel Management** | Kelola versi model dan bandingkan performa |
| 📈 **Confidence Score** | Lihat tingkat kepercayaan prediksi untuk setiap klasifikasi |
| 🌐 **Web Interface** | Antarmuka user-friendly yang responsif |

## 🏷️ Kategori ATK yang Didukung

Model dapat mengidentifikasi **3 jenis Alat Tulis Kantor**:

| Kategori | Deskripsi | Emoji |
|----------|-----------|-------|
| **Eraser** | Penghapus pensil/papan tulis | 🧹 |
| **Kertas** | Kertas HVS, folio, dan sejenisnya | 📄 |
| **Pensil** | Pensil kayu, mekanik, dan sejenisnya | ✏️ |

## 🚀 Quick Start

### Akses Online
Langsung gunakan aplikasi tanpa instalasi:
```
https://atk-classifier-ai.streamlit.app
```

### Instalasi Lokal

**Requirements:**
- Python 3.9 atau lebih tinggi
- pip package manager
- ~300MB disk space untuk model

**Langkah-langkah:**

```bash
# 1. Clone repository
git clone https://github.com/Hash-SD/cnn-custom-datagambar.git
cd cnn-custom-datagambar

# 2. Buat virtual environment (opsional tapi recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download model (first time only)
python download_model.py

# 5. Jalankan aplikasi
streamlit run streamlit_app.py
```

Aplikasi akan terbuka di browser: `http://localhost:8501`

**Note:** Model akan otomatis didownload saat pertama kali menjalankan aplikasi jika belum ada.

## 📖 Cara Penggunaan

### 1️⃣ Halaman Home
- Lihat overview aplikasi
- Pelajari kategori ATK yang didukung
- Akses quick actions ke fitur lain

### 2️⃣ Prediksi (Predict)
```
1. Pilih metode input:
   - Upload File: Pilih gambar dari device
   - Camera Capture: Ambil foto langsung

2. Tunggu proses prediksi
3. Lihat hasil:
   - Kelas yang diprediksi
   - Confidence score (%)
   - Top-3 predictions
```

### 3️⃣ Dashboard
- Lihat metrics model (Accuracy, Loss, F1 Score)
- Visualisasi distribusi kelas
- Informasi arsitektur model

### 4️⃣ Model Management
- Lihat versi model yang tersedia
- Bandingkan performa antar versi
- Informasi model metadata

## 🧠 Arsitektur Model

```
Input (300x300x3)
    ↓
Rescaling Layer (0-1 normalization)
    ↓
Conv2D (32 filters) → MaxPool → BatchNorm
    ↓
Conv2D (64 filters) → MaxPool → BatchNorm
    ↓
Conv2D (128 filters) → MaxPool → BatchNorm
    ↓
Flatten
    ↓
Dense (512) → Dropout (0.5)
    ↓
Dense (256) → Dropout (0.3)
    ↓
Dense (3, softmax) → Output
```

**Model Metrics:**
- Training Accuracy: **88.1%**
- Validation Accuracy: **70.0%**
- Input Size: **300×300 pixels**
- Output Classes: **3**

## 📁 Struktur Project

```
cnn-custom-datagambar/
├── app/
│   ├── components/
│   │   ├── image_uploader.py      # Upload & validasi gambar
│   │   ├── predictor.py           # Engine prediksi
│   │   └── visualizer.py          # Chart & visualisasi
│   ├── pages/
│   │   ├── home.py                # Halaman utama
│   │   ├── predict.py             # Halaman prediksi
│   │   ├── dashboard.py           # Dashboard metrics
│   │   └── model_management.py    # Manajemen model
│   ├── config.py                  # Konfigurasi aplikasi
│   └── main.py                    # Entry point aplikasi
├── models/
│   ├── best_model.keras           # Model terlatih
│   ├── best_model.json            # Metadata model
│   ├── cnn_model.py               # Arsitektur CNN
│   ├── inference.py               # Pipeline inferensi
│   ├── preprocessing.py           # Preprocessing gambar
│   └── train_model.py             # Script training
├── tests/
│   ├── test_cnn_model.py          # Unit tests model
│   └── test_preprocessing.py      # Unit tests preprocessing
├── streamlit_app.py               # Entry point Streamlit Cloud
├── requirements.txt               # Dependencies
└── README.md                      # Dokumentasi
```

## 🛠️ Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| **Frontend** | Streamlit 1.28+ |
| **Deep Learning** | TensorFlow/Keras 2.13+ |
| **Image Processing** | Pillow 10.0+ |
| **Data Processing** | NumPy, Pandas |
| **Visualization** | Plotly 5.17+ |
| **Testing** | Pytest, Hypothesis |

## 📊 Performance

- **Inference Time**: ~500ms per gambar
- **Model Size**: ~15MB
- **Memory Usage**: ~500MB (dengan model loaded)
- **Supported Formats**: JPG, JPEG, PNG, BMP
- **Max File Size**: 5MB

## 🔒 Keamanan & Privacy

- ✅ Semua prediksi dilakukan lokal (tidak ada upload ke server eksternal)
- ✅ Gambar tidak disimpan setelah prediksi
- ✅ Model berjalan di Streamlit Cloud infrastructure
- ✅ Tidak ada tracking atau analytics data collection

## 🧪 Testing

Jalankan unit tests:

```bash
# Semua tests
pytest tests/ -v

# Test spesifik
pytest tests/test_cnn_model.py -v
pytest tests/test_preprocessing.py -v

# Dengan coverage report
pytest tests/ --cov=models --cov=app
```

**Test Coverage:**
- ✅ Model prediction validity
- ✅ Top-K predictions ordering
- ✅ Low confidence detection
- ✅ Image preprocessing
- ✅ File validation
- ✅ Image info extraction

## 📝 Contoh Penggunaan

### Python Script
```python
from models.inference import InferencePipeline
from PIL import Image

# Initialize pipeline
pipeline = InferencePipeline(
    model_path="models/best_model.keras",
    class_names=["eraser", "kertas", "pensil"]
)

# Load dan prediksi gambar
image = Image.open("sample_pencil.jpg")
result = pipeline.predict(image, top_k=3)

# Hasil
print(f"Predicted: {result.predicted_class}")
print(f"Confidence: {result.percentage:.1f}%")
print(f"Top predictions: {result.top_predictions}")
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

## 📄 License

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 👨‍💻 Author

**Hash-SD**
- GitHub: [@Hash-SD](https://github.com/Hash-SD)
- Repository: [cnn-custom-datagambar](https://github.com/Hash-SD/cnn-custom-datagambar)

## 🙏 Acknowledgments

- TensorFlow & Keras team untuk framework deep learning
- Streamlit untuk platform web app yang amazing
- Community open source yang terus berkontribusi

## 📞 Support

Jika ada pertanyaan atau issue:
- 📧 Buka GitHub Issues
- 💬 Diskusi di GitHub Discussions
- 🐛 Report bugs dengan detail lengkap

---

**Made with ❤️ using AI & Deep Learning**

*Last Updated: December 2025*
