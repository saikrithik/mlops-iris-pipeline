#!/bin/bash
set -e

read -p "Enter API image name (e.g., yourname/iris-api:1.0.0): " API_IMAGE
PROMETHEUS_IMAGE="prom/prometheus:latest"
GRAFANA_IMAGE="grafana/grafana:latest"

# Detect entry module
if [ -f "api/main.py" ]; then
    ENTRY_MODULE="api.main"
elif [ -f "main.py" ]; then
    ENTRY_MODULE="main"
else
    echo "ERROR: Could not find main.py"
    exit 1
fi

echo "Using entry module: $ENTRY_MODULE"

# Calculate current hash of requirements.txt (adjust if your deps file is different)
if [ -f "requirements.txt" ]; then
    CURRENT_REQ_HASH=$(sha256sum requirements.txt | awk '{print $1}')
else
    CURRENT_REQ_HASH=""
fi

# File to store last hash
HASH_FILE=".last_requirements_hash"

REBUILD=false

# Check if hash changed or no previous hash recorded
if [ ! -f "$HASH_FILE" ] || [ "$CURRENT_REQ_HASH" != "$(cat $HASH_FILE)" ]; then
    echo "Dependencies changed or first build - will rebuild API image."
    REBUILD=true
else
    echo "No changes in dependencies - skipping API image rebuild."
fi

# Build API image if needed or not found locally
if $REBUILD || ! docker image inspect "$API_IMAGE" >/dev/null 2>&1; then
    echo "Building API image..."
    docker build -t "$API_IMAGE" .
    echo "$CURRENT_REQ_HASH" > "$HASH_FILE"
fi

echo "Pulling monitoring images..."
docker pull $PROMETHEUS_IMAGE
docker pull $GRAFANA_IMAGE

echo "Removing old containers..."
docker rm -f iris-api prometheus grafana || true

echo "Starting iris-api..."
docker run -d --name iris-api -p 8000:8000 "$API_IMAGE" \
    uvicorn "$ENTRY_MODULE:app" --host 0.0.0.0 --port 8000

echo "Starting Prometheus..."
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  $PROMETHEUS_IMAGE

echo "Starting Grafana..."
docker run -d \
  --name grafana \
  -p 3000:3000 \
  $GRAFANA_IMAGE

echo "All services running:"
echo " - Iris API:    http://localhost:8000"
echo " - Iris API docs:    http://localhost:8000/docs"
echo " - Prometheus:  http://localhost:9090"
echo " - Grafana:     http://localhost:3000 (admin/admin)"
echo "=== To stop all services, run: docker stop iris-api prometheus grafana ==="
