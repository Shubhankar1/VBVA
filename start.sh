#!/bin/bash

# VBVA Robust Startup Script
# Ensures latest code is always used and handles automatic rebuilding

set -e  # Exit on any error

echo "🚀 Starting VBVA - Video-Based Virtual Assistant"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_status "Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Check for port conflicts
check_ports() {
    print_status "Checking for port conflicts..."
    
    local ports=("8001" "8502" "8080" "6380")
    local conflicts=()
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            conflicts+=($port)
        fi
    done
    
    if [ ${#conflicts[@]} -ne 0 ]; then
        print_warning "Port conflicts detected on: ${conflicts[*]}"
        read -p "Do you want to kill processes using these ports? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            for port in "${conflicts[@]}"; do
                print_status "Killing process on port $port..."
                lsof -ti:$port | xargs kill -9 2>/dev/null || true
            done
            print_success "Port conflicts resolved"
        else
            print_error "Cannot proceed with port conflicts. Please free up the ports manually."
            exit 1
        fi
    else
        print_success "No port conflicts detected"
    fi
}

# Clean up old containers and images
cleanup() {
    print_status "Cleaning up old containers and images..."
    
    # Stop and remove containers
    docker-compose down -v 2>/dev/null || true
    
    # Remove old images
    docker image prune -f 2>/dev/null || true
    
    print_success "Cleanup completed"
}

# Build containers with latest code
build_containers() {
    print_status "Building containers with latest code..."
    
    # Build backend
    print_status "Building backend..."
    docker-compose build --no-cache backend
    
    # Build frontend
    print_status "Building frontend..."
    docker-compose build --no-cache frontend
    
    print_success "All containers built successfully"
}

# Start services
start_services() {
    print_status "Starting services..."
    
    # Start all services
    docker-compose up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10
    
    print_success "All services started"
}

# Health check
health_check() {
    print_status "Performing health checks..."
    
    # Check backend
    if curl -f http://localhost:8001/health > /dev/null 2>&1; then
        print_success "Backend is healthy"
    else
        print_error "Backend health check failed"
        return 1
    fi
    
    # Check frontend
    if curl -f http://localhost:8502 > /dev/null 2>&1; then
        print_success "Frontend is healthy"
    else
        print_error "Frontend health check failed"
        return 1
    fi
    
    # Test API endpoint
    if curl -f -X POST "http://localhost:8001/api/v1/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "test", "session_id": "test", "agent_type": "general"}' > /dev/null 2>&1; then
        print_success "API endpoint is working"
    else
        print_error "API endpoint test failed"
        return 1
    fi
    
    print_success "All health checks passed"
}

# Display service information
show_info() {
    echo
    echo "🎉 VBVA is now running!"
    echo "======================="
    echo
    echo "📱 Frontend: http://localhost:8502"
    echo "🔧 Backend API: http://localhost:8001"
    echo "📚 API Docs: http://localhost:8001/docs"
    echo "🌐 Nginx Proxy: http://localhost:8080"
    echo
    echo "📊 Service Status:"
    docker-compose ps
    echo
    echo "📋 Useful Commands:"
    echo "  View logs:     docker-compose logs -f"
    echo "  Stop services: ./stop.sh"
    echo "  Check status:  ./status.sh"
    echo
}

# Main execution
main() {
    echo "Starting VBVA with robust initialization..."
    
    check_docker
    check_ports
    cleanup
    build_containers
    start_services
    health_check
    show_info
    
    print_success "VBVA startup completed successfully!"
}

# Run main function
main "$@" 