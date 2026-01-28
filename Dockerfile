# Pull base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn whitenoise

# Copy project
COPY . /app/

# Collect static files (requires standard settings to be flexible, or dummy secret key)
# Note: For production build, typically secrets are injected. 
# Here we can run collectstatic effectively if settings allow it without DB.
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Run command
CMD exec gunicorn promises.wsgi:application --bind 0.0.0.0:8080 --workers 2
