# Azure Portal Configuration Checklist

## Copy-Paste Ready Configuration

Use this checklist to configure your Azure App Service correctly.

---

## 1. Application Settings (Environment Variables)

**Location:** Azure Portal → Your App Service → **Configuration** → **Application settings**

Click **+ New application setting** for each:

| Name | Value | Notes |
|------|-------|-------|
| `WEBSITES_PORT` | `8000` | Required - tells Azure which port to use |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` | Enables Oryx build system |
| `SECRET_KEY` | `your-secret-key` | Generate new: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| `DEBUG` | `False` | **Important:** Always False in production |
| `DATABASE_URL` | See below ⬇️ | Full PostgreSQL connection string |
| `AZURE_ACCOUNT_NAME` | `promisesmovie` | Your existing storage account |
| `AZURE_ACCOUNT_KEY` | `LPv4wV1ANw45...` | Your existing storage key (from upload_to_azure.py) |
| `PYTHON_VERSION` | `3.9` | Optional but recommended |

### DATABASE_URL Format:
```
postgres://USERNAME:PASSWORD@SERVERNAME.postgres.database.azure.com:5432/DBNAME?sslmode=require
```

**Example:**
```
postgres://dbadmin:MyP@ssw0rd@promises-db.postgres.database.azure.com:5432/promises_db?sslmode=require
```

**Click SAVE after adding all settings!**

---

## 2. General Settings

**Location:** Azure Portal → Your App Service → **Configuration** → **General settings**

### Startup Command:
```
bash startup.sh
```

**OR** if not using startup.sh:
```
gunicorn promises.wsgi:application --bind=0.0.0.0:8000 --timeout 600 --workers 4
```

### Stack Settings:
- **Stack:** Python
- **Major version:** Python 3.9
- **Minor version:** Latest

**Click SAVE!**

---

## 3. Deployment Center

**Location:** Azure Portal → Your App Service → **Deployment Center**

### For GitHub Deployment:
1. **Source:** GitHub
2. **Organization:** Your GitHub account
3. **Repository:** Your repo name
4. **Branch:** main (or master)
5. **Build Provider:** App Service Build Service

**Click SAVE!**

---

## 4. PostgreSQL Database Configuration

**Location:** Azure Portal → Your PostgreSQL Server → **Settings**

### Connection Security / Networking:
- ✅ **Allow access to Azure services** (Enable)
- ✅ Add your IP address (for management)
- ✅ **Require secure connections** (SSL) should be ON

### Connection Strings:
Find your connection string here and copy it to `DATABASE_URL` in App Service settings.

---

## 5. App Service Logs (Enable for Troubleshooting)

**Location:** Azure Portal → Your App Service → **Monitoring** → **App Service logs**

Enable these:
- ✅ **Application Logging (Filesystem):** Verbose
- ✅ **Detailed Error Messages:** On
- ✅ **Failed Request Tracing:** On
- **Retention Period:** 7 days

**Click SAVE!**

---

## 6. CORS (If you have a separate frontend)

**Location:** Azure Portal → Your App Service → **API** → **CORS**

Add allowed origins:
- Your frontend domain
- `http://localhost:3000` (for local dev)

---

## Quick Command Reference

### Get Your Database Connection String:
```bash
az postgres flexible-server show-connection-string \
  --server-name YOUR_SERVER_NAME \
  --database-name promises_db \
  --admin-user YOUR_ADMIN_USER \
  --admin-password YOUR_PASSWORD
```

### Generate Django Secret Key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### View Logs:
```bash
az webapp log tail --name YOUR_APP_NAME --resource-group YOUR_RESOURCE_GROUP
```

### Restart App:
```bash
az webapp restart --name YOUR_APP_NAME --resource-group YOUR_RESOURCE_GROUP
```

---

## Post-Configuration Steps

### 1. Restart the App Service
**Location:** Azure Portal → Your App Service → **Overview**
Click **Restart**

### 2. Check Deployment Logs
**Location:** Azure Portal → Your App Service → **Deployment Center** → **Logs**
- Look for successful build
- Check for any errors

### 3. View Live Logs
**Location:** Azure Portal → Your App Service → **Monitoring** → **Log stream**
- Watch for startup messages
- Look for errors

### 4. Test Your Site
Visit: `https://YOUR_APP_NAME.azurewebsites.net`

### 5. Run Migrations (First Time Only)
**Location:** Azure Portal → Your App Service → **Development Tools** → **SSH** → **Go**

```bash
cd /home/site/wwwroot
python manage.py migrate
python manage.py createsuperuser
```

---

## What Should Happen After Configuration

### Successful Deployment Flow:
1. ✅ You push to GitHub
2. ✅ Azure detects the push
3. ✅ Oryx builds your app (installs requirements)
4. ✅ startup.sh runs migrations and collectstatic
5. ✅ Gunicorn starts your Django app
6. ✅ Site is live at `https://YOUR_APP_NAME.azurewebsites.net`

### Check Status:
- **Deployment Center:** Shows "Success" with green checkmark
- **Log stream:** Shows "Booting worker with pid" and no errors
- **Overview:** Shows "Running" status

---

## Common Mistakes to Avoid

❌ **Don't forget to click SAVE** after changing settings
❌ **Don't forget `?sslmode=require`** in DATABASE_URL
❌ **Don't leave DEBUG=True** in production
❌ **Don't forget to restart** after changing settings
❌ **Don't commit secrets** to GitHub (use Azure settings)

---

## Need Help?

If something isn't working:
1. Check **Log stream** for errors
2. Review **Deployment Center** logs
3. Verify all settings match this checklist
4. Read AZURE_TROUBLESHOOTING.md for specific errors
5. Share error logs and screenshots (hide secrets!)
