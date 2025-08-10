## 🏃‍♂️ Run the pre-built Docker image (skip local build)

```bash
# pull image
docker pull saikrithik/iris-api:latest          # ≈ 150 MB download

# start container on port 8000
docker run -d --name iris-api -p 8000:8000 saikrithik/iris-api:latest

# test
$body = @{sepal_length=5.1; sepal_width=3.5; petal_length=1.4; petal_width=0.2} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/predict -Method Post -ContentType application/json -Body $body
# → {"class":2}
