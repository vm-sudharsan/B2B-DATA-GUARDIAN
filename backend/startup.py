"""
Startup script: trains ML models if not already present.
Called automatically before the server starts on Render.
"""
from pathlib import Path

MODELS_DIR = Path(__file__).parent / "models"
REQUIRED_MODELS = [
    "job_title_tfidf.pkl",
    "job_title_classifier.pkl",
    "duplicate_detector.pkl",
    "anomaly_detectors.pkl",
    "correction_sentence_model.pkl",
    "references.pkl",
]

def models_exist() -> bool:
    return all((MODELS_DIR / m).exists() for m in REQUIRED_MODELS)

if __name__ == "__main__":
    if not models_exist():
        print("Models not found. Training now...")
        from ml.enhanced_train import train_all_enhanced_models
        train_all_enhanced_models()
        print("Training complete.")
    else:
        print("Models already exist. Skipping training.")
