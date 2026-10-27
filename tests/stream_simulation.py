import time
import requests
import polars as pl
from src.config import DATA_PATH

def simulate_realtime_stream(n_events: int = 100):
    url = "http://127.0.0.1:8000/v1/score"
    
    schema_overrides = {
        "Time": pl.Float64,
        "Amount": pl.Float64,
        "Class": pl.Int32
    }
    
    df_test = (
        pl.read_csv(DATA_PATH, schema_overrides=schema_overrides)
        .sort("Time")
        .filter(pl.col("Time") >= 144000.0)
    )
    
    print(f"Iniciando emision de {n_events} eventos hacia {url}...\n")
    
    total_latency = 0.0
    frauds_detected = 0
    
    for row in df_test.head(n_events).iter_rows(named=True):
        actual_label = row.pop("Class")
        
        t0 = time.perf_counter()
        response = requests.post(url, json=row)
        network_latency = (time.perf_counter() - t0) * 1000.0
        
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            continue
            
        data = response.json()
        total_latency += network_latency
        
        is_fraud = data["is_fraud"]
        prob = data["fraud_probability"]
        engine_lat = data["latency_ms"]
        
        status = "[ALERTA FRAUDE]" if is_fraud else "[OK]"
        if is_fraud:
            frauds_detected += 1
            
        print(f"{status} Prob: {prob:.4f} | Real: {actual_label} | Engine: {engine_lat}ms | HTTP Total: {network_latency:.1f}ms")
            
        time.sleep(0.03)
        
    print("\n--- Resumen de Streaming ---")
    print(f"Eventos procesados: {n_events}")
    print(f"Fraudes alertados: {frauds_detected}")
    print(f"Latencia HTTP promedio: {total_latency / n_events:.2f} ms")

if __name__ == "__main__":
    simulate_realtime_stream()
