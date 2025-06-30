#!/usr/bin/env bash
# Robust VBVA Startup Script
# Kills any process using port 8000, then starts backend and frontend

PORT=8000

# Kill any process using port 8000
PID=$(lsof -ti tcp:$PORT)
if [ ! -z "$PID" ]; then
  echo "Killing process on port $PORT (PID: $PID)"
  kill -9 $PID
fi

# Start backend with nohup
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug > backend.log 2>&1 &
echo "Backend started on port $PORT. Logs: backend.log"

# Optionally start frontend (uncomment if needed)
# nohup streamlit run frontend/app.py > frontend.log 2>&1 &
# echo "Frontend started. Logs: frontend.log" 