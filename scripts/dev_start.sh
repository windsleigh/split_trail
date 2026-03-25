#!/bin/bash

echo "Starting SplitTrail dev environment..."

# Start MySQL container
echo "Starting MySQL container..."
sudo docker-compose up -d

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
sleep 5

# Activate venv and start FastAPI
echo "Starting FastAPI server..."
cd backend
source ../venv/bin/activate
uvicorn app.main:app --reload --port 8001

