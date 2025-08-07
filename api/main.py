# api/main.py  (no MLflow!)
from pathlib import Path
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Iris Classifier", version="1.0")
Instrumentator().instrument(app).expose(app)

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
    return {"class": int(pred[0])}
