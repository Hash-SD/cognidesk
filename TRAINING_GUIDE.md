# ATK Classifier Training Guide

Panduan lengkap untuk melatih model ATK Classifier dari notebook Anda.

## 📋 Prerequisites

1. Python 3.8 atau lebih tinggi
2. Dataset gambar ATK yang sudah diorganisir per kelas
3. GPU (opsional, tapi sangat direkomendasikan untuk training lebih cepat)

## 🎯 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Dataset

Struktur dataset harus seperti ini:
```
dataset_alat_tulis/
├── Spidol/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Pensil/
│   └── ...
├── Pulpen/
│   └── ...
└── ... (kelas lainnya)
```

### 3. Train Model

#### Simple Training (Cepat)
```bash
python train.py dataset_alat_tulis --epochs 15
```

#### With Hyperparameter Tuning (Hasil Terbaik)
```bash
python train.py dataset_alat_tulis --tune --epochs 25 --trials 10
```

## 🔧 Training Options

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `dataset_dir` | Path ke folder dataset | Required |
| `--tune` | Aktifkan hyperparameter tuning | False |
| `--epochs` | Jumlah epoch training | 15 |
| `--trials` | Jumlah trial untuk tuning | 10 |
| `--img-size` | Ukuran input gambar (224 atau 300) | 300 |
| `--batch-size` | Batch size untuk training | 15 |
| `--output` | Path output model | models/best_model.h5 |

### Examples

```bash
# Training sederhana dengan 20 epochs
python train.py dataset_alat_tulis --epochs 20

# Training dengan tuning, 25 epochs, 15 trials
python train.py dataset_alat_tulis --tune --epochs 25 --trials 15

# Custom image size dan batch size
python train.py dataset_alat_tulis --img-size 224 --batch-size 32

# Save ke file berbeda
python train.py dataset_alat_tulis --output models/model_v2.h5
```

## 📊 Model Architecture

Model menggunakan Custom CNN dengan arsitektur:

### Simple Model
```
Input (300x300x3)
    ↓
Rescaling (1./255)
    ↓
Conv2D (32 filters, 3x3) + ReLU
    ↓
MaxPooling2D
    ↓
Conv2D (64 filters, 3x3) + ReLU
    ↓
MaxPooling2D
    ↓
Conv2D (128 filters, 3x3) + ReLU
    ↓
MaxPooling2D
    ↓
Flatten
    ↓
Dense (128 units) + ReLU
    ↓
Dropout (0.5)
    ↓
Dense (num_classes) + Softmax
```

### Tunable Hyperparameters

Saat menggunakan `--tune`, parameter berikut akan dioptimasi:

- **Conv Layer 1 Filters**: 32, 64, 96, 128
- **Conv Layer 2 Filters**: 32, 64, 96, 128
- **Dense Units**: 32, 64, 96, 128, 160, 192, 224, 256
- **Dropout Rate**: 0.2, 0.3, 0.4, 0.5
- **Learning Rate**: 0.01, 0.001, 0.0001

## 🎨 Training via Streamlit UI

1. Jalankan aplikasi:
```bash
streamlit run app/main.py
```

2. Navigasi ke halaman "🚀 Training"

3. Konfigurasi parameter:
   - Dataset path
   - Training mode (Simple / With Tuning)
   - Epochs
   - Image size
   - Batch size
   - Validation split

4. Klik "Start Training"

5. Monitor progress dan hasil training secara real-time

## 📈 Understanding Training Output

### Training Metrics

- **Training Accuracy**: Akurasi pada data training
- **Validation Accuracy**: Akurasi pada data validation (indikator performa sebenarnya)
- **Training Loss**: Loss pada data training
- **Validation Loss**: Loss pada data validation

### Good Training Signs

✅ Validation accuracy meningkat seiring epochs
✅ Gap antara training dan validation accuracy tidak terlalu besar (<10%)
✅ Loss menurun secara konsisten

### Warning Signs

⚠️ Validation accuracy stagnan atau menurun (overfitting)
⚠️ Gap besar antara training dan validation accuracy (overfitting)
⚠️ Loss tidak menurun (learning rate terlalu tinggi/rendah)

## 💾 Model Files

Setelah training selesai, akan dibuat 2 file:

1. **best_model.h5**: File model TensorFlow
2. **best_model.h5_info.json**: Metadata training (accuracy, hyperparameters, history)

## 🚀 Using Trained Model

Setelah model selesai di-train:

1. Model otomatis tersimpan di `models/best_model.h5`
2. Jalankan aplikasi: `streamlit run app/main.py`
3. Aplikasi akan otomatis load model dan keluar dari demo mode
4. Navigasi ke "🔮 Predict" untuk mulai klasifikasi

## 🔍 Troubleshooting

### Out of Memory Error

Solusi:
- Kurangi batch size: `--batch-size 8`
- Kurangi image size: `--img-size 224`
- Tutup aplikasi lain yang menggunakan GPU/RAM

### Training Too Slow

Solusi:
- Pastikan menggunakan GPU (cek dengan `nvidia-smi`)
- Kurangi jumlah trials: `--trials 5`
- Gunakan simple training tanpa tuning

### Low Accuracy

Solusi:
- Tambah jumlah data per kelas (minimal 50-100 gambar)
- Gunakan hyperparameter tuning: `--tune`
- Tambah epochs: `--epochs 30`
- Pastikan kualitas gambar dataset bagus

### Model Not Loading in Streamlit

Solusi:
- Pastikan file `models/best_model.h5` ada
- Cek path di `app/config.py`
- Restart aplikasi Streamlit

## 📚 Advanced Topics

### Custom Model Architecture

Edit `models/train_model.py` untuk mengubah arsitektur:

```python
def build_model_simple(self, num_classes):
    model = models.Sequential([
        # Tambah/ubah layers di sini
    ])
    return model
```

### Data Augmentation

Tambahkan augmentation di `prepare_dataset()`:

```python
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])
```

### Transfer Learning

Gunakan pre-trained model seperti MobileNetV2 atau EfficientNet untuk hasil lebih baik dengan data lebih sedikit.

## 📞 Support

Jika ada pertanyaan atau masalah, silakan buka issue di repository GitHub.

