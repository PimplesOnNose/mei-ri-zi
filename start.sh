#!/bin/bash
# Start a simple HTTP server for 每日字 development
# Serves on port 8080 by default
PORT=${1:-8080}
echo "Starting 每日字 server on http://localhost:$PORT"
cd "$(dirname "$0")"
python3 -m http.server "$PORT"
