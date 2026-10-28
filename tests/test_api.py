import requests
import json

url = "http://127.0.0.1:8000/predict"

def probar_api():
    print("Iniciando pruebas de estrés sobre la API de Detección...\n")

    # 1. Transacción de Control (Flujo Normal)
    # Valores neutros y un monto cercano al promedio histórico del usuario.
    tx_normal = {
        "V1": 0.1, "V2": 0.1, "V3": 0.1, "V4": 0.1, 
        "V10": 0.1, "V12": 0.1, "V14": 0.1, "V16": 0.1,
        "Amount": 15.50, 
        "hour_of_day": 14, 
        "rolling_avg_amount_50": 15.0, 
        "amount_diff_from_avg": 0.50
    }

    # 2. Transacción Anómala (Simulación de Fraude)
    # Atacamos las variables de mayor impacto (V14 fuertemente negativa, V4 positiva) según SHAP.
    # Disparamos el monto muy por encima de la media histórica.
    tx_fraude = {
        "V1": -5.0, "V2": 4.0, "V3": -7.0, "V4": 6.0, 
        "V10": -6.0, "V12": -8.0, "V14": -9.0, "V16": -5.0,
        "Amount": 999.99, 
        "hour_of_day": 3, 
        "rolling_avg_amount_50": 20.0, 
        "amount_diff_from_avg": 979.99
    }

    try:
        print("=== 🧪 TEST 1: Transacción Normal ===")
        respuesta_normal = requests.post(url, json=tx_normal)
        print(json.dumps(respuesta_normal.json(), indent=2))
        
        print("\n=== 🚨 TEST 2: Transacción Sospechosa ===")
        respuesta_fraude = requests.post(url, json=tx_fraude)
        print(json.dumps(respuesta_fraude.json(), indent=2))
        
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API. ¿Está Uvicorn corriendo en el puerto 8000?")

if __name__ == "__main__":
    probar_api()
