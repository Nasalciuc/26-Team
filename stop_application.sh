#!/bin/bash

# Stop script for the integrated Tinkerbell application

set -e  # Exit on error

echo "================================================"
echo "  Stopping Integrated Tinkerbell Application   "
echo "================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Stop Docker containers
print_info "Stopping Docker containers..."
docker compose down
print_success "Docker containers stopped"

# Stop Tinkerbell frontend server
print_info "Stopping Tinkerbell frontend server..."
if lsof -Pi :8081 -sTCP:LISTEN -t >/dev/null 2>&1; then
    kill $(lsof -t -i:8081) 2>/dev/null || true
    print_success "Tinkerbell frontend server stopped"
else
    print_info "Tinkerbell frontend server was not running"
fi

echo ""
echo "================================================"
echo "  All Services Stopped Successfully! 🛑"
echo "================================================"
echo ""
