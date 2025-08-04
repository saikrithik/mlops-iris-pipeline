# api/main.py
import os
import joblib
import mlflow.pyfunc
from fastapi import FastAPI
from pydantic import BaseModel

# ----------------------------------------------------------------------------------
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
MODEL_NAME          = os.getenv("MODEL_NAME", "iris_xgb_feat")   # adjust to yours
MODEL_STAGE         = os.getenv("MODEL_STAGE", "Production")     # or "Staging"
# ----------------------------------------------------------------------------------

app = FastAPI(title="Iris Classifier API", version="1.0")

class IrisIn(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# load once at startup -------------------------------------------------------------
model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
model     = mlflow.pyfunc.load_model(model_uri,
            tracking_uri=MLFLOW_TRACKING_URI)

@app.get("/")
def root():
    return {"status": "ok", "model": f"{MODEL_NAME}@{MODEL_STAGE}"}

@app.post("/predict")
def predict(inp: IrisIn):
    df = [[
        inp.sepal_length,
        inp.sepal_width,
        inp.petal_length,
        inp.petal_width,
        # engineered features – keep order identical to training:
        inp.petal_length * inp.petal_width,
        inp.sepal_length / inp.petal_length,
    ]]
    pred = model.predict(df)        # returns numpy array
    return {"class": int(pred[0])}
