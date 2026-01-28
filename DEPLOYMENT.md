# Deploying Promises to Google Cloud Platform (GCP)

The recommended architecture for deploying this Django application on GCP is using **Cloud Run** (for the application) and **Cloud SQL** (for the database). This provides a scalable, serverless environment that handles traffic spikes automatically.

## Architecture Overview

1.  **Compute:** [Google Cloud Run](https://cloud.google.com/run)
    -   Host the Django application as a stateless container.
    -   Auto-scales from 0 to N instances.
    -   Cost-effective (pay only for request time).

2.  **Database:** [Cloud SQL for PostgreSQL](https://cloud.google.com/sql)
    -   Managed PostgreSQL service.
    -   Secure connection via Cloud Run Auth Proxy.

3.  **Static Files:** [WhiteNoise](http://whitenoise.evans.io/en/stable/)
    -   Serve static CSS/JS/Images directly from the application container.
    -   *Alternative:* Use `django-storages` with Google Cloud Storage (GCS) if static files are very large.

4.  **Media Files:** Azure Blob Storage
    -   **Recommendation:** Keep using the existing Azure setup since the code (`VideoLink` model) is already configured for it.
    -   *Migration Option:* If you prefer all-GCP, migrate blobs to a GCS bucket and update `VideoLink` logic.

## Deployment Steps

### 0. Prerequisites
- Google Cloud Project created.
- `gcloud` CLI installed.
- APIs enabled: `Cloud Run API`, `Cloud SQL Admin API`, `Container Registry API`.

### 1. Requirements Update
Ensure `gunicorn` (production server) and `whitenoise` are in `requirements.txt`:
```text
gunicorn==20.1.0
whitenoise==6.4.0
psycopg2-binary>=2.9.9
```

### 2. Prepare Settings (`settings.py`)
Update `promises/settings.py` for production:

```python
# Helper to read env vars
import os
import io
import environ  # Recommended: django-environ

# Security
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = ["*"]  # Or your specific Cloud Run URL

# Database (Cloud SQL)
# Use django-environ or parse DATABASE_URL
DATABASES = {
    'default': env.db()  # automatically parses the Cloud SQL socket path if set
}

# Static Files (WhiteNoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add this after SecurityMiddleware
    # ...
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 3. Create Dockerfile
Create a `Dockerfile` in the project root:

```dockerfile
# Use official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD exec gunicorn promises.wsgi:application --bind 0.0.0.0:$PORT
```

### 4. Build and Deploy

**Build the image:**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/promises-app
```

**Deploy to Cloud Run:**
```bash
gcloud run deploy promises-app \
  --image gcr.io/YOUR_PROJECT_ID/promises-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "DJANGO_SETTINGS_MODULE=promises.settings,SECRET_KEY=your-secret-key" \
  --add-cloudsql-instances YOUR_PROJECT_ID:REGION:INSTANCE_NAME
```

### 5. Run Migrations
You can run migrations via a one-off Cloud Run job or by connecting remotely:
```bash
gcloud run jobs create migrate \
  --image gcr.io/YOUR_PROJECT_ID/promises-app \
  --command python manage.py migrate

---

# Option B: Deploying to Microsoft Azure

Since this project already uses **Azure Blob Storage**, deploying the app to Azure creates a unified environment. The recommended path is **Azure App Service** (Web App for Containers) and **Azure Database for PostgreSQL**.

## Architecture Overview

1.  **Compute:** [Azure App Service](https://azure.microsoft.com/en-us/services/app-service/)
    -   Host the containerized Django app.
    -   Integrated with Azure Container Registry (ACR).

2.  **Database:** [Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/services/postgresql/)
    -   Managed PostgreSQL service.

3.  **Storage:** Azure Blob Storage
    -   *Already Configured!* No migration needed.

## Deployment Steps

### 1. Prerequisites
- Azure CLI (`az`) installed.
- Azure Container Registry (ACR) created.

### 2. Build and Push to ACR
```bash
# Login
az acr login --name YOUR_REGISTRY

# Build and Push
docker build -t YOUR_REGISTRY.azurecr.io/promises-app:latest .
docker push YOUR_REGISTRY.azurecr.io/promises-app:latest
```

### 3. Create Resources
```bash
# Create Resource Group
az group create --name promises-rg --location eastus

# Create PostgreSQL Server
az postgres flexible-server create --resource-group promises-rg --name promises-db --admin-user myadmin --admin-password mypassword

# Create App Service Plan (Linux)
az appservice plan create --name promises-plan --resource-group promises-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group promises-rg --plan promises-plan --name promises-app --deployment-container-image-name YOUR_REGISTRY.azurecr.io/promises-app:latest
```

### 4. Configure Environment Variables
Set these in the Azure Portal > App Service > Configuration:
- `DJANGO_SETTINGS_MODULE`: `promises.settings`
- `SECRET_KEY`: `your-secret-key`
- `DATABASE_URL`: `postgres://myadmin:mypassword@promises-db.postgres.database.azure.com:5432/postgres`
- `AZURE_ACCOUNT_NAME`: (Your existing storage config)
- `AZURE_ACCOUNT_KEY`: (Your existing storage config)

### 5. Run Migrations
You can run migrations via SSH in the Azure Portal (Console):
```bash
python manage.py migrate
```

