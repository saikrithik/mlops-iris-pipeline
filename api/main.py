from api.db import init_db, log_to_db
from pathlib import Path
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field
import logging
from prometheus_fastapi_instrumentator import Instrumentator
import subprocess

init_db()


# Setup logging
logging.basicConfig(
    filename="logs/predictions.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

app = FastAPI(title="Iris Classifier", version="1.0")


# Prometheus metrics
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

MODEL_FILE = Path(__file__).parent / "model.pkl"
model = joblib.load(MODEL_FILE)


# Input validation
class IrisIn(BaseModel):
    sepal_length: float = Field(..., ge=0.0, le=10.0)
    sepal_width: float = Field(..., ge=0.0, le=10.0)
    petal_length: float = Field(..., ge=0.0, le=10.0)
    petal_width: float = Field(..., ge=0.0, le=10.0)


@app.post("/predict")
def predict(inp: IrisIn):

    x = [[
        inp.sepal_length,
        inp.sepal_width,
        inp.petal_length,
        inp.petal_width,
        inp.petal_length * inp.petal_width,  # engineered feature
        inp.sepal_length / inp.petal_length,  # engineered feature
    ]]

    pred = model.predict(x)
    logging.info(f"Input: {inp.dict()} | Prediction: {pred[0]}")
    log_to_db(inp, pred[0])

    return {"class": int(pred[0])}


# Retrain using src/train.py
@app.post("/retrain")
def retrain():

    result = subprocess.run(["python", "/app/src/train.py"], capture_output=True, text=True)

    if result.returncode != 0:
        return {"status": "failed", "error": result.stderr}

    return {"status": "success", "output": result.stdout}


# Health Check for api
@app.get("/healthz")
def healthz():

    return {"status": "ok"}
