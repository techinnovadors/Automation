#!/bin/bash

# Navigate to the directory where the script is located
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  source "venv/bin/activate"
fi

# Run the FastAPI application in the background
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > fastapi_app.log 2>&1 &

echo "FastAPI application started in the background."
echo "Check fastapi_app.log for logs." 