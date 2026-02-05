#!/bin/bash
# Azure App Service startup script for Django

echo "Starting Django application..."

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn promises.wsgi:application --bind=0.0.0.0:8000 --timeout 600 --workers 4
