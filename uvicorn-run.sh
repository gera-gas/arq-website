#!/bin/bash

# Check VENV on activation status
if [ -z "$VIRTUAL_ENV" ]; then
  echo "VENV activate..."
  source .venv/bin/activate
else
  echo "VENV already started."
fi

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir .
