# tests/test_api.py
import os
import time
import json
import pytest
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
PREDICT_URL = f"{API_URL}/predict"

# --- helpers -----------------------------------------------------------------
def _wait_for_api(url: str, timeout: float = 20.0, interval: float = 0.5) -> bool:
    """Ping the /predict endpoint with a tiny valid payload until it responds or times out."""
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.post(url, json=payload, timeout=2)
            if r.status_code in (200, 422, 405):  # any response means server is up
                return True
        except requests.RequestException:
            pass
        time.sleep(interval)
    return False

@pytest.fixture(scope="session", autouse=True)
def _ensure_api_running():
    """Skip the whole test session if the API isn't reachable."""
    if not _wait_for_api(PREDICT_URL):
        pytest.skip(
            f"API not reachable at {PREDICT_URL}. "
            "Start the container first, e.g.: "
            "`docker run -d -p 8000:8000 --name iris-api YOUR_DH_USER/iris-api:latest`"
        )

# --- tests -------------------------------------------------------------------
@pytest.mark.parametrize(
    "sample",
    [
        # a classic setosa-ish sample
        {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
        # a virginica-ish sample
        {"sepal_length": 6.3, "sepal_width": 2.9, "petal_length": 5.6, "petal_width": 1.8},
        # a versicolor-ish sample
        {"sepal_length": 5.9, "sepal_width": 3.0, "petal_length": 4.2, "petal_width": 1.5},
    ],
)
def test_predict_returns_class_int_in_range(sample):
    r = requests.post(PREDICT_URL, json=sample, timeout=5)
    assert r.status_code == 200, f"Unexpected status: {r.status_code}, body={r.text}"
    data = r.json()
    assert "class" in data, f"Missing 'class' in response: {data}"
    assert isinstance(data["class"], int), f"'class' must be int, got {type(data['class'])}"
    assert data["class"] in {0, 1, 2}, f"class out of range: {data['class']}"

def test_predict_bad_payload_returns_422():
    # Missing required field -> FastAPI/pydantic should 422
    bad = {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4}
    r = requests.post(PREDICT_URL, json=bad, timeout=5)
    assert r.status_code == 422
