from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_transaccion_normal():
    response = client.post("/predict", json={
        "V1": 0.1, "V2": 0.1, "V3": 0.1, "V4": 0.1, 
        "V10": 0.1, "V12": 0.1, "V14": 0.1, "V16": 0.1,
        "Amount": 15.50, 
        "hour_of_day": 14, 
        "rolling_avg_amount_50": 15.0, 
        "amount_diff_from_avg": 0.50
    })
    assert response.status_code == 200
    assert response.json()["alerta_fraude"] == False
    assert "variables_clave" in response.json()

def test_transaccion_fraude():
    response = client.post("/predict", json={
        "V1": -5.0, "V2": 4.0, "V3": -7.0, "V4": 6.0, 
        "V10": -6.0, "V12": -8.0, "V14": -9.0, "V16": -5.0,
        "Amount": 999.99, 
        "hour_of_day": 3, 
        "rolling_avg_amount_50": 20.0, 
        "amount_diff_from_avg": 979.99
    })
    assert response.status_code == 200
    assert response.json()["alerta_fraude"] == True
    assert "variables_clave" in response.json()
