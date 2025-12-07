# 🚀 Quick Start Guide - ATK Classifier

## Langkah Cepat (5 Menit)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Siapkan Dataset

Struktur folder:
```
dataset_alat_tulis/
├── Spidol/
├── Pensil/
├── Pulpen/
└── ... (kelas lainnya)
```

### 3. Train Model

**Pilihan A: Training Cepat (15 menit)**
```bash
python train.py dataset_alat_tulis --epochs 15
```

**Pilihan B: Training Optimal (1-2 jam)**
```bash
python train.py dataset_alat_tulis --tune --epochs 25 --trials 10
```

### 4. Jalankan Aplikasi
```bash
streamlit run app/main.py
```

Buka browser di `http://localhost:8501`

## 🎯 Training via UI

1. Jalankan: `streamlit run app/main.py`
2. Klik "🚀 Training" di sidebar
3. Masukkan path dataset
4. Pilih mode training
5. Klik "Start Training"
6. Tunggu sampai selesai
7. Model otomatis aktif!

## 📊 Hasil yang Diharapkan

| Mode | Waktu | Akurasi | Ukuran Model |
|------|-------|---------|--------------|
| Simple | 10-15 menit | 85-90% | ~85 MB |
| Tuning | 1-2 jam | 90-95% | ~85 MB |

## 🔍 Troubleshooting Cepat

**Error: Dataset not found**
```bash
# Pastikan path benar
ls dataset_alat_tulis/
```

**Error: Out of memory**
```bash
# Kurangi batch size
python train.py dataset_alat_tulis --batch-size 8
```

**Error: Streamlit not found**
```bash
# Install ulang
pip install streamlit
```

**Model tidak load di Streamlit**
```bash
# Cek file model ada
ls models/best_model.h5

# Restart streamlit
# Ctrl+C lalu jalankan ulang
streamlit run app/main.py
```

## 📚 Dokumentasi Lengkap

- **Training Guide**: Lihat `TRAINING_GUIDE.md`
- **Implementation Details**: Lihat `IMPLEMENTATION_SUMMARY.md`
- **Full README**: Lihat `README.md`

## 💡 Tips

1. **GPU Recommended**: Training 10x lebih cepat dengan GPU
2. **Dataset Quality**: Minimal 50-100 gambar per kelas
3. **Hyperparameter Tuning**: Gunakan untuk hasil terbaik
4. **Early Stopping**: Sudah otomatis aktif, tidak perlu khawatir overfitting

## 🎉 Selesai!

Setelah training selesai:
- Model tersimpan di `models/best_model.h5`
- Aplikasi otomatis keluar dari demo mode
- Siap untuk prediksi real-time!

