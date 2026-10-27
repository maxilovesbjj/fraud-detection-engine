import time
import json
import joblib
import numpy as np
from src.config import MODEL_PATH, SCALER_PATH, ARTIFACTS_DIR

def run_benchmark(n_iterations: int = 1000):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    with open(ARTIFACTS_DIR / "metadata.json", "r") as f:
        threshold = json.load(f)["optimal_threshold"]

    # Simular payload crudo
    sample_raw = {
        "Time": 150000.0,
        "Amount": 149.62,
        **{f"V{i}": np.random.randn() for i in range(1, 29)}
    }

    latencies = []
    
    # Warmup
    for _ in range(50):
        _ = model.predict_proba(np.zeros((1, 31)))

    seconds_in_day = 86400.0
    for _ in range(n_iterations):
        t0 = time.perf_counter()
        
        # Transformacion
        t_sin = np.sin(2 * np.pi * sample_raw["Time"] / seconds_in_day)
        t_cos = np.cos(2 * np.pi * sample_raw["Time"] / seconds_in_day)
        amt = float(scaler.transform([[sample_raw["Amount"]]])[0][0])
        
        vec = [amt, t_sin, t_cos] + [sample_raw[f"V{i}"] for i in range(1, 29)]
        input_data = np.array([vec], dtype=np.float64)
        
        prob = model.predict_proba(input_data)[0, 1]
        _ = prob >= threshold
        
        latencies.append((time.perf_counter() - t0) * 1000)

    p50 = np.percentile(latencies, 50)
    p95 = np.percentile(latencies, 95)
    p99 = np.percentile(latencies, 99)

    print(f"--- Benchmark de Inferencia ({n_iterations} reqs) ---")
    print(f"Latencia P50: {p50:.3f} ms")
    print(f"Latencia P95: {p95:.3f} ms")
    print(f"Latencia P99: {p99:.3f} ms")

if __name__ == "__main__":
    run_benchmark()
