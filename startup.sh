#!/bin/bash

# Wait for database to be ready
echo "Waiting for database to be ready..."
python manage.py wait_for_db --settings=web.settings

# Run migrations
echo "Running migrations..."
python manage.py migrate --settings=web.settings

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell --settings=web.settings -c "
from django.contrib.auth.models import User
import os

admin_username = os.getenv('ADMIN_USERNAME', 'admin')
admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')

if not User.objects.filter(is_superuser=True).exists():
    print(f'Creating superuser: {admin_username}')
    User.objects.create_superuser(admin_username, admin_email, admin_password)
    print(f'Superuser created: {admin_username}/{admin_password}')
else:
    print('Superuser already exists')
"

# Start Django server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 --settings=web.settings