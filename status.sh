#!/bin/bash

# VBVA Status Monitoring Script

echo "🔍 VBVA System Status Check"
echo "=========================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

# Check if services are running
echo ""
echo "📊 Service Status:"
if docker-compose ps | grep -q "Up"; then
    docker-compose ps
else
    echo "❌ No services are running"
    echo "   Run: docker-compose up -d"
    exit 1
fi

# Check backend health
echo ""
echo "🔧 Backend Health:"
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy (http://localhost:8000)"
else
    echo "❌ Backend is not responding"
fi

# Check frontend health
echo ""
echo "🌐 Frontend Health:"
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "✅ Frontend is healthy (http://localhost:8501)"
else
    echo "❌ Frontend is not responding"
fi

# Check Redis (if running)
echo ""
echo "🗄️  Redis Status:"
if docker-compose ps redis | grep -q "Up"; then
    if docker-compose exec redis redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis is healthy"
    else
        echo "❌ Redis is not responding"
    fi
else
    echo "⚠️  Redis is not running"
fi

# Check disk space for video outputs
echo ""
echo "💾 Storage Status:"
if [ -d "/tmp/wav2lip_outputs" ]; then
    OUTPUT_SIZE=$(du -sh /tmp/wav2lip_outputs 2>/dev/null | cut -f1)
    OUTPUT_COUNT=$(find /tmp/wav2lip_outputs -name "*.mp4" 2>/dev/null | wc -l)
    echo "📁 Video outputs: $OUTPUT_COUNT files ($OUTPUT_SIZE)"
else
    echo "⚠️  Video output directory not found"
fi

# Check recent logs
echo ""
echo "📝 Recent Logs (last 5 lines):"
echo "Backend:"
docker-compose logs --tail=5 backend 2>/dev/null || echo "   No logs available"

echo ""
echo "Frontend:"
docker-compose logs --tail=5 frontend 2>/dev/null || echo "   No logs available"

echo ""
echo "🎯 Quick Actions:"
echo "   View all logs: docker-compose logs -f"
echo "   Restart services: docker-compose restart"
echo "   Stop services: docker-compose down"
echo "   Rebuild: docker-compose up --build -d" 