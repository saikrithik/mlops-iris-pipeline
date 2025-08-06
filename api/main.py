# api/main.py  (no MLflow!)
from db import init_db, log_to_db
from pathlib import Path
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import logging
from prometheus_fastapi_instrumentator import Instrumentator

init_db()

# Setup logging
logging.basicConfig(
    filename="logs/predictions.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


app = FastAPI(title="Iris Classifier", version="1.0")


instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


MODEL_FILE = Path(__file__).parent / "model.pkl"


model = joblib.load(MODEL_FILE)


class IrisIn(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.post("/predict")
def predict(inp: IrisIn):
    x = [[
        inp.sepal_length,
        inp.sepal_width,
        inp.petal_length,
        inp.petal_width,
        # engineered features (must match training order)
        inp.petal_length * inp.petal_width,
        inp.sepal_length / inp.petal_length,
    ]]
    pred = model.predict(x)
    # Log input and output
    logging.info(f"Input: {inp.dict()} | Prediction: {pred[0]}")
    log_to_db(inp, pred[0])
    return {"class": int(pred[0])}
