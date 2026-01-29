import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from pathlib import Path

# Paths
DATA_PATH = Path("data/metrics.csv")
MODEL_PATH = Path("models/isolation_forest.pkl")

def train():
    if not DATA_PATH.exists():
        print(f"❌ Error: Data file not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "cpu_usage_percent",
        "memory_usage_percent",
        "disk_usage_percent",
    ]

    if not all(col in df.columns for col in required_columns):
        print(f"❌ Error: Missing columns. Expected {required_columns}, found {df.columns.tolist()}")
        return

    features = df[required_columns]

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    model.fit(features)

    # Ensure models directory exists
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save model
    joblib.dump(model, MODEL_PATH)

    print("✅ Isolation Forest model trained and saved successfully.")

if __name__ == "__main__":
    train()
