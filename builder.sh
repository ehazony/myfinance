#!/bin/bash

# Check if Docker service is active and start it if not
#if ! service is-active --quiet docker; then
#  echo "Docker service is not active. Starting Docker..."
#  sudo service start docker
#fi

# Change to myfinance directory
cd /Users/efraimhazony/Desktop/www/myfinance
echo "Changing directory to myfinance..."
docker compose up -d

# Change to grid directory
cd /Users/efraimhazony/PycharmProjects/testGrid
echo "Changing directory to grid..."
docker compose up -d

# Change to efficient directory
cd /Users/efraimhazony/Documents/GitHub/efficient-dashboard
echo "Changing directory to efficient..."
docker compose up -d


echo "Deployment completed!"



