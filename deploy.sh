#!/bin/bash
docker pull saikrithik/iris-api:latest
docker run -d -p 8000:8000 --name iris-api saikrithik/iris-api:latest
echo "App running at http://localhost:8000"
