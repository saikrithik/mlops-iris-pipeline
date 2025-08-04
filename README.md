# mlops-iris-pipeline
MLOps IRIS Dataset CI/CD Pipeline

# PYTHON VERSION - 3.12.0

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

pip install setuptools

mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 5000


install https://www.docker.com/products/docker-desktop/


# IN powershell - admin mode
 wsl --install
>> dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
>> dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart