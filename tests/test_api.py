from fastapi.testclient import TestClient
from infrastructure.api_fastapi import app

client = TestClient(app)


def test_servir_pantalla_web():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sistemas Inteligentes" in response.text


def test_endpoint_evaluar_asistente():
    payload = {
        "nombre": "Sofia Rincon",
        "edad": 22,
        "asistencias_previas": 4,
        "gusta_reggaeton": True,
        "hora_llegada_pm": 2.0
    }

    response = client.post("/api/v1/evaluar", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "resultado" in data
    assert data["resultado"]["asistente"] == "Sofia Rincon"
    assert "puntaje_mlp" in data["resultado"]
    assert "estado" in data["resultado"]