# Azure Deployment Guide for Promises Django App

## Prerequisites
Your Azure Resources should include:
1. **App Service** (Web App for Containers or Web App)
2. **Azure Database for PostgreSQL** (Flexible Server recommended)
3. **Azure Blob Storage** (Already configured: promisesmovie)

## Step-by-Step Deployment

### 1. Update Settings for Production

The `settings.py` file needs environment-based configuration. Add this to your settings:

```python
import os

# Production settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', 'rnq^-bt#k%r93jyp!5i7bugftjiba^3)x3shre4$q9ni-cycx9')
ALLOWED_HOSTS = ['*']  # Update with your actual domain

# Database - Use environment variable for Azure PostgreSQL
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ['DATABASE_URL'],
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Local development database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'promises_db',
            'USER': 'promises_user',
            'PASSWORD': '123456',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }

# Azure Blob Storage (already using this)
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME', 'promisesmovie')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY', '')
AZURE_CONTAINER = 'media'

# WhiteNoise for static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. Update requirements.txt

Add these production dependencies:

```
gunicorn==20.1.0
whitenoise==6.4.0
dj-database-url==2.1.0
azure-storage-blob==12.19.0
django-storages==1.14.2
```

### 3. Azure Portal Configuration

#### A. App Service Settings

Go to **Azure Portal → Your App Service → Configuration → Application Settings**

Add these environment variables:

| Name | Value |
|------|-------|
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` |
| `WEBSITES_PORT` | `8000` |
| `SECRET_KEY` | `your-secret-key-here` |
| `DEBUG` | `False` |
| `DATABASE_URL` | `postgres://username:password@your-server.postgres.database.azure.com:5432/dbname?sslmode=require` |
| `AZURE_ACCOUNT_NAME` | `promisesmovie` |
| `AZURE_ACCOUNT_KEY` | `your-azure-storage-key` |

#### B. Set Startup Command

Go to **Azure Portal → Your App Service → Configuration → General settings**

Set **Startup Command** to:
```
bash startup.sh
```

Or if using the Dockerfile approach:
```
gunicorn promises.wsgi:application --bind=0.0.0.0:8000 --timeout 600 --workers 4
```

#### C. Configure Deployment

**Option 1: GitHub Deployment (Recommended)**
1. Go to **Azure Portal → Your App Service → Deployment Center**
2. Select **GitHub** as source
3. Authenticate and select your repository
4. Select the **main** branch
5. Azure will automatically deploy on push

**Option 2: Container Deployment**
1. Build and push Docker image to Azure Container Registry
2. Configure App Service to pull from ACR

### 4. Database Setup

#### Create Azure PostgreSQL Database:

```bash
# Using Azure CLI
az postgres flexible-server create \
  --resource-group your-resource-group \
  --name promises-db-server \
  --location eastus \
  --admin-user dbadmin \
  --admin-password YourPassword123! \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 14

# Create database
az postgres flexible-server db create \
  --resource-group your-resource-group \
  --server-name promises-db-server \
  --database-name promises_db
```

#### Configure Firewall:
- Allow Azure services access
- Add your IP for management

#### Get Connection String:
```
postgres://dbadmin:YourPassword123!@promises-db-server.postgres.database.azure.com:5432/promises_db?sslmode=require
```

### 5. Common Issues & Solutions

#### Issue: "Application Error" or 500 Error
**Solution:**
- Check logs: `az webapp log tail --name your-app-name --resource-group your-rg`
- Enable logging in Azure Portal → Monitoring → App Service logs
- Set DEBUG=True temporarily to see error details

#### Issue: Static files not loading
**Solution:**
- Ensure `whitenoise` is installed and configured
- Run `python manage.py collectstatic` (done in startup.sh)
- Check STATIC_ROOT and STATIC_URL settings

#### Issue: Database connection fails
**Solution:**
- Verify DATABASE_URL is correct
- Check PostgreSQL firewall allows Azure services
- Ensure SSL mode is set to `require`

#### Issue: Container fails to start
**Solution:**
- Check Dockerfile builds locally: `docker build -t test .`
- Verify startup command is correct
- Check if port 8000 is exposed

### 6. Verify Deployment

After deployment:
1. Visit `https://your-app-name.azurewebsites.net`
2. Check Application Logs for errors
3. Verify database connection
4. Test media file uploads

### 7. Post-Deployment

#### Run Django Commands:
SSH into the container via Azure Portal → Development Tools → SSH

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## Quick Checklist

- [ ] `startup.sh` created and executable
- [ ] `requirements.txt` updated with production dependencies
- [ ] Environment variables configured in Azure Portal
- [ ] Startup command set in App Service configuration
- [ ] Database created and connection string added
- [ ] GitHub deployment configured (or container pushed)
- [ ] Firewall rules configured for database
- [ ] SSL certificates configured (auto-provided by Azure for *.azurewebsites.net)
- [ ] Application logs enabled
- [ ] Static files working
- [ ] Media files working via Azure Blob Storage

## Monitoring

Enable Application Insights for monitoring:
- Azure Portal → Your App Service → Application Insights → Enable
- View metrics, traces, and errors in real-time
