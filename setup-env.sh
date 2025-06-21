#!/bin/bash

# Setup environment file
echo "Setting up environment file..."

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file"
        exit 0
    fi
fi

# Copy env.example to .env
cp env.example .env

echo "✅ .env file created successfully!"
echo ""
echo "📋 Environment variables configured:"
echo "   • PostgreSQL Database: ${POSTGRES_DB:-django_db}"
echo "   • PostgreSQL User: ${POSTGRES_USER:-django_user}"
echo "   • PostgreSQL Password: ${POSTGRES_PASSWORD:-django_pass}"
echo "   • Django Debug: ${DJANGO_DEBUG:-True}"
echo "   • Admin Username: ${ADMIN_USERNAME:-admin}"
echo "   • Admin Password: ${ADMIN_PASSWORD:-admin123}"
echo ""
echo "🚀 You can now run: docker-compose up --build" 