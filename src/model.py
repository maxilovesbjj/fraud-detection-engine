import json
import joblib
import numpy as np
import polars as pl
from lightgbm import LGBMClassifier
from sklearn.metrics import (
    average_precision_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    confusion_matrix
)
from src.config import MODEL_PATH, ARTIFACTS_DIR, ALL_FEATURES, TARGET, RANDOM_STATE, TARGET_RECALL
from src.transform import prepare_datasets

def train_and_evaluate():
    train, val, test = prepare_datasets()

    X_train = train.select(ALL_FEATURES).to_numpy()
    y_train = train.select(TARGET).to_numpy().ravel()

    X_val = val.select(ALL_FEATURES).to_numpy()
    y_val = val.select(TARGET).to_numpy().ravel()

    X_test = test.select(ALL_FEATURES).to_numpy()
    y_test = test.select(TARGET).to_numpy().ravel()

    # scale_pos_weight controlado para evitar saturación de falsos positivos
    model = LGBMClassifier(
        n_estimators=200,
        learning_rate=0.03,
        num_leaves=31,
        max_depth=6,
        scale_pos_weight=10.0,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=-1
    )
    print("Entrenando LightGBM con features ciclicas...")
    model.fit(X_train, y_train)

    # 1. Calibracion de umbral en VALIDACION
    val_probs = model.predict_proba(X_val)[:, 1]
    val_ap = average_precision_score(y_val, val_probs)
    precisions, recalls, thresholds = precision_recall_curve(y_val, val_probs)

    # Buscar umbral que cumpla TARGET_RECALL maximizando Precision
    valid_idx = np.where(recalls[:-1] >= TARGET_RECALL)[0]
    if len(valid_idx) == 0:
        # Fallback al punto de maximo F1 si no alcanza 80% recall
        f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-9)
        optimal_threshold = float(thresholds[np.argmax(f1_scores)])
    else:
        best_precision_idx = valid_idx[np.argmax(precisions[valid_idx])]
        optimal_threshold = float(thresholds[best_precision_idx])

    print("\n--- Metricas en Validacion ---")
    print(f"AUPRC (Average Precision): {val_ap:.4f}")
    print(f"Umbral operativo calibrado: {optimal_threshold:.4f}")

    # 2. Evaluacion en TEST intacto
    test_probs = model.predict_proba(X_test)[:, 1]
    test_ap = average_precision_score(y_test, test_probs)
    test_preds = (test_probs >= optimal_threshold).astype(int)

    test_prec = precision_score(y_test, test_preds, zero_division=0)
    test_rec = recall_score(y_test, test_preds, zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_test, test_preds, labels=[0, 1]).ravel()

    print("\n--- Evaluacion en Test Set (Futuro) ---")
    print(f"AUPRC:     {test_ap:.4f}")
    print(f"Precision: {test_prec:.4f}")
    print(f"Recall:    {test_rec:.4f}")
    print(f"Matriz:    TP={tp} | FN={fn} | FP={fp} | TN={tn}")

    # 3. Guardado
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metadata = {
        "optimal_threshold": optimal_threshold,
        "features": ALL_FEATURES,
        "val_auprc": val_ap,
        "test_auprc": test_ap,
        "test_recall": test_rec,
        "test_precision": test_prec
    }
    with open(ARTIFACTS_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

if __name__ == "__main__":
    train_and_evaluate()
