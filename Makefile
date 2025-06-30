# VBVA Makefile
# Easy management commands for the Video-Based Virtual Assistant

.PHONY: help start stop status logs clean build test

# Default target
help:
	@echo "VBVA - Video-Based Virtual Assistant"
	@echo ""
	@echo "Available commands:"
	@echo "  make start    - Start the VBVA system"
	@echo "  make stop     - Stop the VBVA system"
	@echo "  make status   - Check system status"
	@echo "  make logs     - View service logs"
	@echo "  make clean    - Clean up Docker resources"
	@echo "  make build    - Build Docker images"
	@echo "  make test     - Run system tests"
	@echo "  make help     - Show this help message"

# Start the system
start:
	@echo "🚀 Starting VBVA system..."
	@./start.sh

# Stop the system
stop:
	@echo "🛑 Stopping VBVA system..."
	@./stop.sh

# Check system status
status:
	@echo "📊 Checking VBVA system status..."
	@./status.sh

# View service logs
logs:
	@echo "📋 Showing service logs..."
	@docker-compose logs -f

# Clean up Docker resources
clean:
	@echo "🧹 Cleaning up Docker resources..."
	@docker system prune -f
	@docker-compose down --remove-orphans --volumes

# Build Docker images
build:
	@echo "🔨 Building Docker images..."
	@docker-compose build --no-cache

# Run system tests
test:
	@echo "🧪 Running system tests..."
	@docker-compose exec backend python -m pytest tests/ -v

# Restart the system
restart: stop start

# Quick health check
health:
	@echo "🏥 Quick health check..."
	@curl -s http://localhost:8001/health || echo "Backend not responding"
	@curl -s http://localhost:8502/_stcore/health || echo "Frontend not responding"

# Show access URLs
urls:
	@echo "🌐 VBVA Access URLs:"
	@echo "  Backend API:     http://localhost:8001"
	@echo "  Frontend UI:     http://localhost:8502"
	@echo "  API Docs:        http://localhost:8001/docs"
	@echo "  Health Check:    http://localhost:8001/health"
	@echo "  Nginx Proxy:     http://localhost:8080" 