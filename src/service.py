import time
import json
import joblib
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.config import MODEL_PATH, SCALER_PATH, ARTIFACTS_DIR, ALL_FEATURES

# Cache en memoria de artefactos
artifacts = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MODEL_PATH.exists() or not SCALER_PATH.exists():
        raise RuntimeError("Artefactos no encontrados. Ejecuta src.model primero.")
    
    artifacts["model"] = joblib.load(MODEL_PATH)
    artifacts["scaler"] = joblib.load(SCALER_PATH)
    
    with open(ARTIFACTS_DIR / "metadata.json", "r") as f:
        artifacts["metadata"] = json.load(f)
        
    print("Artefactos cargados en memoria. Motor listo para scoring.")
    yield
    artifacts.clear()

app = FastAPI(title="Real-Time Fraud Engine", lifespan=lifespan)

class TransactionPayload(BaseModel):
    Time: float = Field(..., description="Segundos transcurridos")
    Amount: float = Field(..., ge=0.0, description="Monto de la transaccion")
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

@app.post("/v1/score")
def score_transaction(payload: TransactionPayload):
    start_t = time.perf_counter()
    
    # 1. Transformacion de features continuas en memoria (sin pasar por Polars/Pandas)
    seconds_in_day = 86400.0
    time_sin = np.sin(2 * np.pi * payload.Time / seconds_in_day)
    time_cos = np.cos(2 * np.pi * payload.Time / seconds_in_day)
    
    # Escalado de Amount usando el RobustScaler persistido
    amount_scaled = float(artifacts["scaler"].transform([[payload.Amount]])[0][0])
    
    # 2. Vectorizacion en el orden estricto de ALL_FEATURES
    data_dict = payload.model_dump()
    feature_vector = [amount_scaled, time_sin, time_cos]
    for i in range(1, 29):
        feature_vector.append(data_dict[f"V{i}"])
        
    input_array = np.array([feature_vector], dtype=np.float64)
    
    # 3. Inferencia de probabilidad
    prob_fraud = float(artifacts["model"].predict_proba(input_array)[0, 1])
    threshold = artifacts["metadata"]["optimal_threshold"]
    is_fraud = prob_fraud >= threshold
    
    latency_ms = (time.perf_counter() - start_t) * 1000.0
    
    return {
        "is_fraud": is_fraud,
        "fraud_probability": round(prob_fraud, 6),
        "operating_threshold": threshold,
        "latency_ms": round(latency_ms, 3)
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
