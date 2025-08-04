# syntax=docker/dockerfile:1
FROM python:3.12-slim

# 1. System deps (OpenBLAS for numpy/scikit)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git && rm -rf /var/lib/apt/lists/*

# 2. Copy requirements & install
WORKDIR /app
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy source
COPY api/ .

# 4. Expose & launch
ENV UVICORN_PORT=8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
