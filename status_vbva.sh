#!/bin/bash

# VBVA Status Script
# Shows the current status of all VBVA services

echo "📊 VBVA - Video-Based Virtual Assistant Status"
echo "=============================================="

# Function to check service status
check_service() {
    local port=$1
    local service_name=$2
    local url=$3
    
    echo -n "Checking $service_name (port $port)... "
    
    # Check if port is in use
    if lsof -i:$port >/dev/null 2>&1; then
        # Try to connect to the service
        if curl -s "$url" >/dev/null 2>&1; then
            echo "✅ RUNNING"
            return 0
        else
            echo "⚠️ STARTING (port in use but not responding)"
            return 1
        fi
    else
        echo "❌ STOPPED"
        return 2
    fi
}

# Check backend
backend_status=$(check_service 8000 "Backend" "http://localhost:8000/health")
backend_code=$?

# Check frontend
frontend_status=$(check_service 8501 "Frontend" "http://localhost:8501")
frontend_code=$?

echo ""
echo "📋 Summary:"
echo "==========="

if [ $backend_code -eq 0 ] && [ $frontend_code -eq 0 ]; then
    echo "✅ All services are running"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Backend:  http://localhost:8000"
    echo "   Frontend: http://localhost:8501"
    echo "   API Docs: http://localhost:8000/docs"
elif [ $backend_code -eq 2 ] && [ $frontend_code -eq 2 ]; then
    echo "❌ All services are stopped"
    echo ""
    echo "💡 To start services, run: ./start_vbva.sh"
else
    echo "⚠️ Some services are not running properly"
    echo ""
    echo "💡 To restart services, run: ./stop_vbva.sh && ./start_vbva.sh"
fi

echo ""
echo "==============================================" 