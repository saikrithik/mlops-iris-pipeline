# tests/test_api.py

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post("/predict", json={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 200
    assert "class" in response.json()
