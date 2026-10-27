from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "creditcard.csv"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
SCALER_PATH = ARTIFACTS_DIR / "scaler.joblib"
MODEL_PATH = ARTIFACTS_DIR / "fraud_model.joblib"

RANDOM_STATE = 42
TARGET_RECALL = 0.80

PCA_FEATURES = [f"V{i}" for i in range(1, 29)]
ENGINEERED_FEATURES = ["Amount", "time_sin", "time_cos"]
ALL_FEATURES = ENGINEERED_FEATURES + PCA_FEATURES
TARGET = "Class"
