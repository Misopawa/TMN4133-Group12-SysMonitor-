import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)
_model = None
_model_path = None

def _get_model(config):
    global _model, _model_path
    path = Path(config.get("model_path", "models/isolation_forest.pkl")) if config else Path("models/isolation_forest.pkl")
    if _model is not None and _model_path == path:
        return _model
    logger.info(f"Loading AI model from {path}")
    _model = joblib.load(path)
    _model_path = path
    return _model

def detect_anomaly(metrics: dict, config: dict | None = None):
    model = _get_model(config or {})
    data = {
        "cpu_usage_percent": float(metrics.get("cpu_usage_percent", 0.0)),
        "memory_usage_percent": float(metrics.get("memory_usage_percent", 0.0)),
        "disk_usage_percent": float(metrics.get("disk_usage_percent", 0.0)),
    }
    X = pd.DataFrame([data], columns=["cpu_usage_percent", "memory_usage_percent", "disk_usage_percent"])
    pred = model.predict(X)[0]
    score = model.score_samples(X)[0]
    is_anomaly = pred == -1
    if is_anomaly:
        logger.warning(f"AI anomaly detected (score={score:.4f})")
    return {
        "anomaly": bool(is_anomaly),
        "score": float(score),
        "raw_prediction": int(pred),
    }
