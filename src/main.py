from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fraud Detection Engine API", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    modelo = joblib.load(BASE_DIR / 'models' / 'xgboost_fraud_engine.pkl')
    explainer = joblib.load(BASE_DIR / 'models' / 'shap_explainer.pkl')
    logger.info("Modelos cargados correctamente.")
except Exception as e:
    logger.critical(f"Error crítico al cargar modelos: {e}")
    raise

class Transaccion(BaseModel):
    V1: float; V2: float; V3: float; V4: float; V10: float; V12: float; V14: float; V16: float
    Amount: float
    hour_of_day: int
    rolling_avg_amount_50: float
    amount_diff_from_avg: float

@app.post("/predict")
def predecir_fraude(trx: Transaccion):
    input_data = pd.DataFrame([trx.model_dump()])
    
    for col in [f"V{i}" for i in range(1, 29) if f"V{i}" not in input_data.columns]:
        input_data[col] = 0.0
        
    columnas_ordenadas = [f"V{i}" for i in range(1, 29)] + ['Amount', 'hour_of_day', 'rolling_avg_amount_50', 'amount_diff_from_avg']
    input_data = input_data[columnas_ordenadas]
    
    try:
        prediccion = int(modelo.predict(input_data)[0])
        probabilidad = float(modelo.predict_proba(input_data)[0][1])
        
        shap_values = explainer.shap_values(input_data)
        top_features = pd.Series(
            shap_values[0], index=input_data.columns
        ).abs().nlargest(3).to_dict()
        
        return {
            "alerta_fraude": bool(prediccion == 1),
            "probabilidad_fraude": f"{probabilidad:.2%}",
            "accion_recomendada": "Revisión Manual" if prediccion == 1 else "Aprobar",
            "variables_clave": top_features
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
