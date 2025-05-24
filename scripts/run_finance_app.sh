#!/bin/bash
# This script runs both the Django backend and the frontend concurrently.
# It starts Django only if port 8000 is not already in use.

# Function to check if port 8000 is in use
is_port_in_use() {
  lsof -i :8000 -sTCP:LISTEN -t >/dev/null
}

# Attempt to start Django only if port 8000 is free
if is_port_in_use; then
  echo "Port 8000 is in use. Assuming Django is already running in debug mode."
  DJANGO_PID=""
else
  echo "Port 8000 is free. Starting Django server..."
  /Users/efraimhazony/code/finance/venv/bin/python /Users/efraimhazony/code/finance/manage.py runserver 8000 &
  DJANGO_PID=$!
fi

# Function to clean up background processes on exit
cleanup() {
  echo "Shutting down servers..."
  if [ -n "$DJANGO_PID" ]; then
    kill $DJANGO_PID
  fi
  exit 0
}

# Trap termination signals (Ctrl+C, etc.)
trap cleanup SIGINT SIGTERM

# Change directory to the frontend and start it in the foreground
echo "Starting frontend..."
cd /Users/efraimhazony/code/efficient-dashboard || { echo "Directory not found"; exit 1; }
npm start

# Wait for any background processes (if any)
wait