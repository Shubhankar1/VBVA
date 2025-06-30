#!/bin/bash

# VBVA Stop Script
# Cleanly shuts down all VBVA services

echo "🛑 Stopping VBVA - Video-Based Virtual Assistant"
echo "================================================"

# Function to kill processes by port
kill_process_on_port() {
    local port=$1
    local process_name=$2
    
    echo "Stopping $process_name on port $port..."
    
    # Find processes using the port
    local pids=$(lsof -ti:$port 2>/dev/null)
    
    if [ -n "$pids" ]; then
        for pid in $pids; do
            echo "Killing process $pid on port $port"
            kill -TERM $pid 2>/dev/null
            
            # Wait a bit for graceful shutdown
            sleep 2
            
            # Force kill if still running
            if kill -0 $pid 2>/dev/null; then
                echo "Force killing process $pid"
                kill -KILL $pid 2>/dev/null
            fi
        done
        echo "✅ $process_name stopped"
    else
        echo "ℹ️ No $process_name process found on port $port"
    fi
}

# Stop backend (port 8000)
kill_process_on_port 8000 "Backend"

# Stop frontend (port 8501)
kill_process_on_port 8501 "Frontend"

# Kill any remaining Python processes related to VBVA
echo "Cleaning up any remaining VBVA processes..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "streamlit.*app.py" 2>/dev/null

echo "✅ VBVA services stopped"
echo "================================================" 