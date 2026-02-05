# Azure Deployment Troubleshooting

## Most Common Issues When App Won't Go Live

### 1. Missing or Incorrect Startup Command

**Problem:** App Service doesn't know how to start your Django app.

**Solution:**
1. Go to Azure Portal → Your App Service → **Configuration** → **General settings**
2. Set **Startup Command** to: `bash startup.sh`
3. Click **Save**
4. Restart the app

### 2. Missing Environment Variables

**Problem:** App can't connect to database or crashes due to missing settings.

**Check Required Variables:**
Go to Azure Portal → Your App Service → **Configuration** → **Application settings**

Ensure these are set:

```
WEBSITES_PORT = 8000
SCM_DO_BUILD_DURING_DEPLOYMENT = true
SECRET_KEY = your-django-secret-key
DEBUG = False
DATABASE_URL = postgres://user:password@server.postgres.database.azure.com:5432/dbname?sslmode=require
AZURE_ACCOUNT_NAME = promisesmovie
AZURE_ACCOUNT_KEY = your-storage-account-key
```

### 3. Database Connection Errors

**Problem:** Can't connect to PostgreSQL database.

**Solutions:**
1. **Check Connection String Format:**
   ```
   postgres://username:password@hostname.postgres.database.azure.com:5432/database?sslmode=require
   ```

2. **Verify Firewall Rules:**
   - Azure Portal → PostgreSQL Server → **Connection security**
   - Enable "Allow access to Azure services"
   - Add your IP if testing locally

3. **Test Database Connection:**
   ```bash
   # From Azure SSH console
   python manage.py dbshell
   ```

### 4. Static Files Not Loading

**Problem:** CSS/JS not working, site looks broken.

**Solutions:**
1. **Verify WhiteNoise is installed:**
   ```bash
   pip list | grep whitenoise
   ```

2. **Check settings.py middleware order:**
   WhiteNoise must be right after SecurityMiddleware:
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be here
       # ... rest
   ]
   ```

3. **Run collectstatic:**
   ```bash
   python manage.py collectstatic --noinput
   ```

### 5. Port Configuration Issues

**Problem:** App fails to bind to correct port.

**Solution:**
Ensure `WEBSITES_PORT=8000` is set in Application Settings and Gunicorn binds to it:
```bash
gunicorn promises.wsgi:application --bind=0.0.0.0:8000
```

### 6. Logs Show "No module named 'promises'"

**Problem:** Python can't find your Django project.

**Solutions:**
1. Check `PYTHONPATH` in Application Settings
2. Verify folder structure in deployment
3. Check `wsgi.py` path in startup command

### 7. 500 Internal Server Error

**Problem:** Generic server error.

**How to Debug:**
1. **Enable detailed logging:**
   - Azure Portal → App Service → **Monitoring** → **App Service logs**
   - Enable **Application Logging (Filesystem)** → Level: **Verbose**
   - Enable **Detailed error messages**
   - Enable **Failed request tracing**

2. **View real-time logs:**
   ```bash
   # Using Azure CLI
   az webapp log tail --name YOUR_APP_NAME --resource-group YOUR_RESOURCE_GROUP
   ```

3. **Check log stream in Portal:**
   - Azure Portal → App Service → **Monitoring** → **Log stream**

4. **Temporary debug mode:**
   - Set `DEBUG=True` in Application Settings (temporarily!)
   - Check browser for detailed error
   - **Remember to set it back to False!**

### 8. Build Fails During Deployment

**Problem:** Deployment succeeds but app doesn't build.

**Solutions:**
1. **Check Oryx build logs:**
   - Azure Portal → Deployment Center → Logs
   - Look for Python version detection
   - Check if requirements.txt was found

2. **Verify Python version:**
   Add to Application Settings:
   ```
   PYTHON_VERSION = 3.9
   ```

3. **Manual build test:**
   ```bash
   # In Azure SSH console
   pip install -r requirements.txt
   ```

### 9. Database Migrations Not Running

**Problem:** Database schema is outdated.

**Solutions:**
1. **SSH into container:**
   - Azure Portal → App Service → **Development Tools** → **SSH** → **Go**

2. **Run migrations manually:**
   ```bash
   cd /home/site/wwwroot
   python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

### 10. GitHub Deployment Not Triggering

**Problem:** Push to GitHub but Azure doesn't redeploy.

**Solutions:**
1. **Check Deployment Center:**
   - Azure Portal → Deployment Center
   - Verify GitHub is connected
   - Check branch is correct

2. **Manual sync:**
   - Click **Sync** button in Deployment Center

3. **Re-authorize GitHub:**
   - Disconnect and reconnect GitHub integration

## How to View Logs

### Method 1: Azure Portal
1. Go to **Monitoring** → **Log stream**
2. View live logs in browser

### Method 2: Azure CLI
```bash
# Install Azure CLI first
az login
az webapp log tail --name your-app-name --resource-group your-resource-group
```

### Method 3: Download Logs
```bash
az webapp log download --name your-app-name --resource-group your-resource-group
```

### Method 4: SSH Console
1. Azure Portal → App Service → SSH
2. Run:
   ```bash
   cat /home/LogFiles/application.log
   ```

## Quick Diagnosis Commands

### From Azure SSH Console:

```bash
# Check Python version
python --version

# Check if Django is installed
python -c "import django; print(django.VERSION)"

# List installed packages
pip list

# Test database connection
python manage.py dbshell

# Check migrations status
python manage.py showmigrations

# Test collectstatic
python manage.py collectstatic --dry-run

# Check environment variables
env | grep -E 'DATABASE|SECRET|AZURE|DEBUG'
```

## Still Not Working?

### Share This Info:
1. **Error message** from logs
2. **Screenshot** of Application Settings (hide secrets!)
3. **Deployment Center** status
4. **Log output** from log stream
5. **Database** connection string format (hide password!)

### Checklist Before Asking for Help:
- [ ] Startup command is set
- [ ] All environment variables are configured
- [ ] Database firewall allows Azure services
- [ ] requirements.txt includes all production dependencies
- [ ] Logs show what error is occurring
- [ ] Static files are collected
- [ ] Port 8000 is configured

## Pro Tips

1. **Always check logs first** - 90% of issues are visible in logs
2. **Test locally with production settings** before deploying
3. **Use environment variables** for all secrets
4. **Keep DEBUG=False** in production
5. **Enable Application Insights** for better monitoring
6. **Set up health check endpoint** for App Service monitoring

## Contact Points

- Azure Status: https://status.azure.com/
- Azure Support: Azure Portal → Help + support
- Stack Overflow tag: `azure-web-app-service` + `django`
