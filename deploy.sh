#!/bin/bash

# VBVA Production Deployment Script
set -e

echo "🚀 Deploying VBVA Production System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create one with your API keys."
    echo "Example .env file:"
    echo "OPENAI_API_KEY=your_openai_key"
    echo "ELEVENLABS_API_KEY=your_elevenlabs_key"
    echo "SECRET_KEY=your_secret_key"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads cache logs

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    docker-compose logs backend
    exit 1
fi

if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
    docker-compose logs frontend
    exit 1
fi

echo "🎉 VBVA Production System is deployed!"
echo ""
echo "📊 Service URLs:"
echo "   Frontend: http://localhost:8501"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Update services: docker-compose pull && docker-compose up -d" 