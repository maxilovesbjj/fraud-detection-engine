from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn

app = FastAPI(title="Fraud Detection Engine API", version="1.0.0")

try:
    modelo = joblib.load('../models/xgboost_fraud_engine.pkl')
except Exception as e:
    modelo = None

class Transaccion(BaseModel):
    V1: float; V2: float; V3: float; V4: float; V10: float; V12: float; V14: float; V16: float
    Amount: float
    hour_of_day: int
    rolling_avg_amount_50: float
    amount_diff_from_avg: float

@app.post("/predict")
def predecir_fraude(trx: Transaccion):
    if modelo is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado.")
    
    input_data = pd.DataFrame([trx.dict()])
    
    for col in [f"V{i}" for i in range(1, 29) if f"V{i}" not in input_data.columns]:
        input_data[col] = 0.0
        
    # Forzar el orden exacto que espera XGBoost
    columnas_ordenadas = [f"V{i}" for i in range(1, 29)] + ['Amount', 'hour_of_day', 'rolling_avg_amount_50', 'amount_diff_from_avg']
    input_data = input_data[columnas_ordenadas]
    
    try:
        prediccion = int(modelo.predict(input_data)[0])
        probabilidad = float(modelo.predict_proba(input_data)[0][1])
        return {
            "alerta_fraude": bool(prediccion == 1),
            "probabilidad_fraude": f"{probabilidad:.2%}",
            "accion_recomendada": "Revisión Manual" if prediccion == 1 else "Aprobar"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
