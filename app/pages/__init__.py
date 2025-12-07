# Streamlit Pages Package
"""
Streamlit pages for ATK Classifier application.
"""
from app.pages import home
from app.pages import predict
from app.pages import dashboard
from app.pages import model_management

__all__ = ["home", "predict", "dashboard", "model_management"]
