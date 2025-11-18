#!/bin/bash

# Launch script for the integrated Tinkerbell application
# This script launches both the Django backend and Tinkerbell frontend

set -e  # Exit on error

echo "================================================"
echo "  Launching Integrated Tinkerbell Application  "
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

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_info "Creating .env file from env.example..."
    cp env.example .env
    print_success ".env file created"
else
    print_success ".env file already exists"
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi
print_success "Docker is running"

# Stop any existing containers
print_info "Stopping any existing containers..."
docker compose down > /dev/null 2>&1 || true

# Start Docker containers (Django + PostgreSQL)
print_info "Starting Docker containers (Django backend + PostgreSQL)..."
docker compose up -d --build

# Wait for Django to be ready
print_info "Waiting for Django backend to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ > /dev/null 2>&1; then
        print_success "Django backend is ready on port 8000"
        break
    fi
    attempt=$((attempt + 1))
    if [ $attempt -eq $max_attempts ]; then
        print_error "Django backend failed to start after $max_attempts attempts"
        docker compose logs web | tail -50
        exit 1
    fi
    sleep 2
done

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js and try again."
    exit 1
fi
print_success "Node.js is installed (version $(node --version))"

# Check if Tinkerbell frontend server is already running
if lsof -Pi :8081 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_info "Port 8081 is already in use. Stopping existing process..."
    kill $(lsof -t -i:8081) 2>/dev/null || true
    sleep 2
fi

# Start Tinkerbell frontend server
print_info "Starting Tinkerbell frontend server..."
cd tinkerbell-frontend
nohup node server.js > /tmp/tinkerbell-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to be ready
print_info "Waiting for Tinkerbell frontend to be ready..."
sleep 3
max_attempts=10
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/ > /dev/null 2>&1; then
        print_success "Tinkerbell frontend is ready on port 8081"
        break
    fi
    attempt=$((attempt + 1))
    if [ $attempt -eq $max_attempts ]; then
        print_error "Tinkerbell frontend failed to start after $max_attempts attempts"
        cat /tmp/tinkerbell-frontend.log
        exit 1
    fi
    sleep 2
done

echo ""
echo "================================================"
echo "  Application Launched Successfully! 🎉"
echo "================================================"
echo ""
print_success "Backend (Django):     http://localhost:8000"
print_success "Frontend (Tinkerbell): http://localhost:8081"
echo ""
print_info "Admin Credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
print_info "To view Django logs:       docker compose logs -f web"
print_info "To view Frontend logs:     tail -f /tmp/tinkerbell-frontend.log"
print_info "To stop all services:      docker compose down && kill $FRONTEND_PID"
echo ""
print_info "Frontend process PID: $FRONTEND_PID"
echo ""
