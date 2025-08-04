# mlops-iris-pipeline
MLOps IRIS Dataset CI/CD Pipeline

# PYTHON VERSION - 3.12.0

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

pip install setuptools

mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 5000


# install docker from 
https://www.docker.com/products/docker-desktop/


# IN powershell - admin mode
 wsl --install
>> dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
>> dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart


# to build docker image
docker build -t iris-api:latest -f Dockerfile .

# to run and host docker image
powershell docker run -d -p 8000:8000  -e MLFLOW_TRACKING_URI=http://host.docker.internal:5000  -e MODEL_NAME=iris_xgb_feat  -e MODEL_STAGE=Production  --name iris-api-demo iris-api:latest

# to check if the image is active
docker ps -a --filter name=iris-api-demo

# to check docker logs
docker logs -f iris-api-demo

# to predict
curl.exe -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"


# NOTE: to delete docker container
docker rm -f iris-api-demo
