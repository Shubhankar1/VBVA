#!/bin/bash

# VBVA Development Script
# Watches for code changes and automatically rebuilds containers

set -e

echo "🔧 VBVA Development Mode"
echo "========================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[DEV]${NC} $1"
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

# Check if fswatch is installed (for file watching)
check_fswatch() {
    if ! command -v fswatch &> /dev/null; then
        print_warning "fswatch not found. Installing..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            brew install fswatch
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            sudo apt-get update && sudo apt-get install -y fswatch
        else
            print_error "fswatch not available for this OS. Please install manually."
            exit 1
        fi
    fi
}

# Function to rebuild specific service
rebuild_service() {
    local service=$1
    print_status "Rebuilding $service..."
    
    docker-compose build --no-cache $service
    docker-compose restart $service
    
    print_success "$service rebuilt and restarted"
}

# Function to watch for changes
watch_changes() {
    print_status "Watching for code changes..."
    print_status "Press Ctrl+C to stop watching"
    
    # Watch backend files
    fswatch -o backend/ api/ models/ services/ agents/ config/ | while read f; do
        print_status "Backend files changed, rebuilding backend..."
        rebuild_service backend
    done &
    
    # Watch frontend files
    fswatch -o frontend/ | while read f; do
        print_status "Frontend files changed, rebuilding frontend..."
        rebuild_service frontend
    done &
    
    # Watch requirements and docker files
    fswatch -o requirements.txt Dockerfile Dockerfile.frontend docker-compose.yml | while read f; do
        print_status "Build files changed, rebuilding all services..."
        docker-compose build --no-cache
        docker-compose restart
    done &
    
    # Wait for all background processes
    wait
}

# Function to start development mode
start_dev() {
    print_status "Starting development mode..."
    
    # Initial build
    print_status "Performing initial build..."
    docker-compose build --no-cache
    docker-compose up -d
    
    # Wait for services to be ready
    sleep 10
    
    # Show status
    print_success "Development environment ready!"
    echo
    echo "📱 Frontend: http://localhost:8502"
    echo "🔧 Backend API: http://localhost:8001"
    echo "📚 API Docs: http://localhost:8001/docs"
    echo
    echo "🔄 Watching for changes..."
    echo "   - Backend changes will auto-rebuild backend"
    echo "   - Frontend changes will auto-rebuild frontend"
    echo "   - Build file changes will rebuild everything"
    echo
    echo "Press Ctrl+C to stop watching"
    
    # Start watching
    watch_changes
}

# Function to show logs
show_logs() {
    print_status "Showing logs (Ctrl+C to stop)..."
    docker-compose logs -f
}

# Function to show help
show_help() {
    echo "VBVA Development Script"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  start     Start development mode with file watching"
    echo "  logs      Show logs from all services"
    echo "  rebuild   Rebuild all services"
    echo "  backend   Rebuild only backend"
    echo "  frontend  Rebuild only frontend"
    echo "  help      Show this help message"
    echo
}

# Main execution
case "${1:-start}" in
    "start")
        check_fswatch
        start_dev
        ;;
    "logs")
        show_logs
        ;;
    "rebuild")
        print_status "Rebuilding all services..."
        docker-compose build --no-cache
        docker-compose restart
        print_success "All services rebuilt"
        ;;
    "backend")
        rebuild_service backend
        ;;
    "frontend")
        rebuild_service frontend
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac 