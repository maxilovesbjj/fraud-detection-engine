import requests
import polars as pl
from src.config import DATA_PATH

def test_actual_frauds():
    url = "http://127.0.0.1:8000/v1/score"
    schema_overrides = {"Time": pl.Float64, "Amount": pl.Float64, "Class": pl.Int32}
    
    # Extraer fraudes reales del conjunto de test cronológico
    df_fraud = (
        pl.read_csv(DATA_PATH, schema_overrides=schema_overrides)
        .sort("Time")
        .filter((pl.col("Time") >= 144000.0) & (pl.col("Class") == 1))
    )
    
    print(f"Probando {df_fraud.height} fraudes reales del Test Set contra la API...\n")
    
    caught = 0
    missed = 0
    
    for row in df_fraud.iter_rows(named=True):
        row.pop("Class")
        res = requests.post(url, json=row).json()
        
        prob = res["fraud_probability"]
        is_fraud = res["is_fraud"]
        lat = res["latency_ms"]
        
        if is_fraud:
            caught += 1
            print(f"[CAPTURA EXITOSA] Prob: {prob:.4f} | Umbral: {res['operating_threshold']:.4f} | Latencia: {lat}ms")
        else:
            missed += 1
            print(f"[FRAUDE ESCAPADO] Prob: {prob:.4f} | Umbral: {res['operating_threshold']:.4f} | Latencia: {lat}ms")
            
    print("\n--- Balance en Streaming de Fraudes Reales ---")
    print(f"Total probados: {df_fraud.height}")
    print(f"Capturados:     {caught} ({caught / df_fraud.height * 100:.1f}%)")
    print(f"Escapados:      {missed}")

if __name__ == "__main__":
    test_actual_frauds()
