import os
import joblib
import mlflow
from mlflow.tracking import MlflowClient

from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

from data_loader import load_data

# --------------------------------------------------------------------------
#  MLflow config
# --------------------------------------------------------------------------
mlflow.set_tracking_uri("http://127.0.0.1:5000")   # your running server
mlflow.set_experiment("iris_experiments")
client = MlflowClient()

# local directory to save joblib copies
os.makedirs("models", exist_ok=True)

# --------------------------------------------------------------------------


def make_model(tag: str):

    if tag == "logreg":
        return LogisticRegression(max_iter=200, n_jobs=-1), {"max_iter": 200}
    if tag == "rf":
        return RandomForestClassifier(
            n_estimators=100, max_depth=3, random_state=42, n_jobs=-1
        ), {"n_estimators": 100, "max_depth": 3}
    if tag == "dt":
        return DecisionTreeClassifier(max_depth=3, random_state=42), {"max_depth": 3}
    if tag == "lgbm":
        return LGBMClassifier(
            n_estimators=50, learning_rate=0.1, random_state=42, n_jobs=-1, verbose=0
        ), {"n_estimators": 50, "learning_rate": 0.1, "verbose": 0}
    if tag == "xgb":
        return XGBClassifier(
            n_estimators=50,
            learning_rate=0.1,
            max_depth=3,
            objective="multi:softprob",
            num_class=3,
            subsample=0.9,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
        ), {
            "n_estimators": 50,
            "learning_rate": 0.1,
            "max_depth": 3,
            "subsample": 0.9,
            "colsample_bytree": 0.8,
        }
    raise ValueError(f"Unknown model tag: {tag}")

# --------------------------------------------------------------------------


def run(tag: str, feats: bool):

    X_train, X_test, y_train, y_test = load_data(add_features=feats)
    model, params = make_model(tag)

    run_name = f"{tag}_{'feat' if feats else 'base'}"
    with mlflow.start_run(run_name=run_name) as active:
        run_id = active.info.run_id
        mlflow.log_params(params)
        mlflow.log_param("add_features", feats)

        # train and evaluate
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
        mlflow.log_metric("accuracy", acc)

        # 1️⃣  save locally
        local_path = f"models/{run_name}.pkl"
        joblib.dump(model, local_path)

        # 2️⃣  log to MLflow
        mlflow.sklearn.log_model(model, artifact_path="model")

        # 3️⃣  register to Model Registry
        model_uri = f"runs:/{run_id}/model"
        registry_name = f"iris_{tag}{'_feat' if feats else ''}"
        try:
            mv = mlflow.register_model(model_uri, name=registry_name)
            print(f"→ Registered as {registry_name} v{mv.version}")
        except mlflow.exceptions.MlflowException:
            # model already exists; create new version
            mv = client.create_model_version(
                name=registry_name, source=model_uri, run_id=run_id
            )
            print(f"→ New version {mv.version} for {registry_name}")

        print(f"{run_name:<15} | acc={acc:.4f} | saved → {local_path}")


# --------------------------------------------------------------------------
if __name__ == "__main__":
    for tag in ["logreg", "rf", "dt", "lgbm", "xgb"]:
        run(tag, feats=False)   # baseline
        run(tag, feats=True)    # engineered-features
