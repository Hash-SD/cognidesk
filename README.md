# ✏️ ATK Classifier

Klasifikasi Alat Tulis Kantor dengan AI - Powered by Deep Learning

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://atk-classifier-ai.streamlit.app)

## 🎯 Fitur

Upload atau foto gambar ATK, langsung dapat hasil klasifikasi:

| Kategori | Deskripsi |
|----------|-----------|
| 🧹 **Eraser** | Penghapus |
| 📄 **Kertas** | Paper |
| ✏️ **Pensil** | Pencil |

## 🚀 Demo Online

Langsung coba: **[atk-classifier-ai.streamlit.app](https://atk-classifier-ai.streamlit.app)**

## 💻 Jalankan Lokal

```bash
# Clone
git clone https://github.com/Hash-SD/cnn-custom-datagambar.git
cd cnn-custom-datagambar

# Install
pip install -r requirements.txt

# Download model (first time)
python download_model.py

# Run
streamlit run streamlit_app.py
```

## 🧠 Model

- **Arsitektur**: CNN (3 Conv layers)
- **Input**: 300×300 pixels
- **Accuracy**: ~88%

## 📁 Struktur

```
├── app/
│   ├── main.py              # Main app
│   ├── config.py            # Config
│   └── components/          # UI components
├── models/
│   ├── best_model.keras     # Trained model
│   ├── cnn_model.py         # Model architecture
│   └── inference.py         # Prediction pipeline
├── streamlit_app.py         # Entry point
└── requirements.txt
```

## 🛠️ Tech Stack

- Streamlit
- TensorFlow/Keras
- Pillow
- Plotly

## 📄 License

MIT

---

**Made with ❤️ by Hash-SD**
