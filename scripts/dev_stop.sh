#!/bin/bash

echo "Stopping SplitTrail dev environment..."

# Stop FastAPI (kill uvicorn)
pkill -f "uvicorn app.main:app" && echo "FastAPI stopped" || echo "FastAPI was not running"

# Stop MySQL container
sudo docker-compose down && echo "MySQL container stopped"

