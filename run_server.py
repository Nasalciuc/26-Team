#!/usr/bin/env python
import os
import sys

# Set the working directory
os.chdir(r'C:\Users\user\Tinkerbell\26-Team')

# Add current directory to Python path
sys.path.insert(0, '.')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

# Import and run Django
try:
    from django.core.management import execute_from_command_line
    print("Starting Django server...")
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc