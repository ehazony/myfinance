#!/bin/bash

# Function to restart the server
function restart_server {
    echo "Restarting server..."
    # You may need to modify this command based on your actual setup
    pkill -f "gunicorn finance.wsgi:application"
    python3 manage.py wait_for_db &&
        gunicorn finance.wsgi:application --bind 0.0.0.0:8000
}

# Watch for changes in the app volume and trigger the restart
echo "Watching for changes in the app volume..."
watchmedo shell-command --patterns="*.py" --recursive --command='restart_server' .
