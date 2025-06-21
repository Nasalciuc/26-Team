#!/bin/bash

# Wait for database to be ready
echo "Waiting for database to be ready..."
python manage.py wait_for_db

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    print('Creating superuser...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Start Django server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 