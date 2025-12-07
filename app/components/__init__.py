"""
Components package for ATK Classifier application.
"""
from app.components.image_uploader import ImageUploader, UploadResult
from app.components.predictor import PredictionEngine, display_results, display_results_compact
from app.components.visualizer import (
    ModelMetrics,
    create_class_distribution_chart,
    create_metrics_gauge,
    create_confusion_matrix_chart,
    create_training_history_chart,
    display_model_metrics,
    display_class_distribution,
    get_demo_metrics,
    get_demo_class_distribution
)

__all__ = [
    "ImageUploader",
    "UploadResult",
    "PredictionEngine",
    "display_results",
    "display_results_compact",
    "ModelMetrics",
    "create_class_distribution_chart",
    "create_metrics_gauge",
    "create_confusion_matrix_chart",
    "create_training_history_chart",
    "display_model_metrics",
    "display_class_distribution",
    "get_demo_metrics",
    "get_demo_class_distribution"
]
