# mlops-iris-pipeline
MLOps IRIS Dataset CI/CD Pipeline

# PYTHON VERSION - 3.12.0

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

pip install setuptools

```
mlflow server `
>>   --backend-store-uri sqlite:///mlflow.db `
>>   --default-artifact-root file:/mlruns `
>>   --host 0.0.0.0 --port 5000
```

# install docker from 
https://www.docker.com/products/docker-desktop/


# IN powershell - admin mode
 wsl --install
>> dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
>> dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart


# to build docker image
    # for first time:
    docker build -t iris-api:latest -f Dockerfile .

    # for second time:
    docker build -t iris-api:latest .

    # if want with env change no cache
    docker build --no-cache -t iris-api:latest -f Dockerfile .


# to run and host docker image
docker run -d --name iris-api-demo -p 8000:8000 iris-api:latest

# to check if the image is active
docker ps -a --filter name=iris-api-demo

# to check docker logs
docker logs -f iris-api-demo

# to predict
$body = @{sepal_length=5.1; sepal_width=3.5; petal_length=1.4; petal_width=0.2} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/predict -Method Post -ContentType application/json -Body $body

# NOTE: to delete docker container
docker rm -f iris-api-demo 2>$null
