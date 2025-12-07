# 🛠️ Development Guide

## Setup

```bash
# Clone repository
git clone https://github.com/Hash-SD/cnn-custom-datagambar.git
cd cnn-custom-datagambar

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Download model
python download_model.py
```

## Running Locally

```bash
streamlit run streamlit_app.py
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=models --cov=app
```

## Project Dependencies

- **streamlit**: Web framework
- **tensorflow**: Deep learning
- **pillow**: Image processing
- **numpy/pandas**: Data processing
- **plotly**: Visualization
- **pytest/hypothesis**: Testing

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Keep functions small and focused
