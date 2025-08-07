# tests/test_api.py
import fastapi
from fastapi.testclient import TestClient, WSGITransport
from api.main import app

client = TestClient(transport=WSGITransport(app=app))

def test_predict_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Iris Prediction API"}
