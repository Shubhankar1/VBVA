#!/bin/bash

# VBVA Stop Script
# This script gracefully stops the VBVA system

set -e

echo "🛑 Stopping VBVA (Video-Based Virtual Assistant)..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to stop Docker services
stop_services() {
    echo -e "${BLUE}🛑 Stopping Docker services...${NC}"
    
    # Stop and remove containers
    docker-compose down --remove-orphans 2>/dev/null || true
    
    echo -e "${GREEN}✅ Services stopped${NC}"
}

# Function to clean up Docker resources
cleanup_resources() {
    echo -e "${BLUE}🧹 Cleaning up Docker resources...${NC}"
    
    # Remove dangling images
    docker image prune -f 2>/dev/null || true
    
    # Remove unused networks
    docker network prune -f 2>/dev/null || true
    
    # Remove unused volumes (optional - uncomment if needed)
    # docker volume prune -f 2>/dev/null || true
    
    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

# Function to check if services are still running
check_running() {
    echo -e "${BLUE}🔍 Checking if services are still running...${NC}"
    
    local ports=("8001" "8502" "6380" "8080")
    local running=()
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            running+=("$port")
        fi
    done
    
    if [ ${#running[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Services still running on ports: ${running[*]}${NC}"
        echo -e "${YELLOW}You may need to manually stop them${NC}"
        return 1
    else
        echo -e "${GREEN}✅ All services stopped${NC}"
        return 0
    fi
}

# Main execution
main() {
    stop_services
    cleanup_resources
    check_running
    
    echo -e "${GREEN}🎉 VBVA has been stopped successfully!${NC}"
}

# Run main function
main "$@" 