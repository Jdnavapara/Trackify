# Deployment Guide

This guide covers deploying Trackify to production environments.

## Prerequisites

- Server with Python 3.8+ support
- Web server (Nginx recommended)
- Database (PostgreSQL recommended for production)
- SSL certificate
- Domain name

## Production Checklist

### Security
- [ ] Change `DEBUG = False` in settings
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS/SSL
- [ ] Configure secure headers
- [ ] Set up database backups

### Performance
- [ ] Use PostgreSQL database
- [ ] Configure static file serving
- [ ] Set up caching
- [ ] Configure logging
- [ ] Set up monitoring

### Environment
- [ ] Set environment variables
- [ ] Configure email backend
- [ ] Set up file storage
- [ ] Configure API keys

## Environment Setup

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv postgresql nginx -y

# Install certbot for SSL
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Database Setup

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE trackify_db;
CREATE USER trackify_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE trackify_db TO trackify_user;
\q
```

### 3. Application Setup

```bash
# Clone repository
git clone <repository-url>
cd trackify

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 4. Environment Configuration

Create `.env` file:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_URL=postgresql://trackify_user:password@localhost/trackify_db

OPENAI_API_KEY=your-openai-key
OPEN_EXCHANGE_RATES_API_KEY=your-exchange-rates-key

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Django Configuration

Update `budgetlens/settings.py` for production:

```python
# Production settings
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 6. Database Migration

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Web Server Configuration

### Nginx Configuration

Create `/etc/nginx/sites-available/trackify`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/trackify /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Gunicorn Configuration

Create `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=your-user
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock budgetlens.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start Gunicorn:

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## SSL Configuration

### Let's Encrypt SSL

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Manual SSL

If you have your own SSL certificate:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # ... rest of configuration
}
```

## Monitoring and Logging

### Log Configuration

Update `budgetlens/settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/trackify/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop -y

# Check application status
sudo systemctl status gunicorn
sudo systemctl status nginx

# Monitor logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/trackify/django.log
```

## Backup Strategy

### Database Backup

```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/var/backups/trackify"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

pg_dump -U trackify_user -h localhost trackify_db > $BACKUP_DIR/trackify_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "trackify_*.sql" -mtime +7 -delete
```

### File Backup

```bash
# Backup media files
tar -czf /var/backups/trackify/media_$DATE.tar.gz /path/to/project/media/
```

### Automated Backups

```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /path/to/backup/script.sh
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes
CREATE INDEX CONCURRENTLY idx_expense_user_date ON core_expense(user_id, expense_date);
CREATE INDEX CONCURRENTLY idx_expense_category ON core_expense(category);
CREATE INDEX CONCURRENTLY idx_income_user_date ON core_income(user_id, income_date);
```

### Caching

Install Redis and configure Django caching:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Static Files Optimization

```python
# settings.py
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
```

## Troubleshooting

### Common Issues

#### 1. 502 Bad Gateway

```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# Check socket file
ls -la /run/gunicorn.sock

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

#### 2. Database Connection Issues

```bash
# Test database connection
python manage.py dbshell

# Check PostgreSQL status
sudo systemctl status postgresql
```

#### 3. Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# Check permissions
ls -la /path/to/project/staticfiles/
```

#### 4. Memory Issues

```bash
# Monitor memory usage
htop

# Adjust Gunicorn workers
# In gunicorn.service file
--workers 2  # Reduce if memory is limited
```

## Scaling

### Horizontal Scaling

1. **Load Balancer**: Use Nginx or HAProxy
2. **Multiple Application Servers**: Run multiple Gunicorn instances
3. **Database Replication**: Set up PostgreSQL replication
4. **Redis Cluster**: For caching and sessions

### Vertical Scaling

1. **Increase Server Resources**: More CPU, RAM
2. **Database Optimization**: Query optimization, indexing
3. **CDN**: Use CloudFlare or AWS CloudFront for static files

## Maintenance

### Regular Tasks

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Clear cache
python manage.py clear_cache

# Backup database
./backup.sh
```

### Security Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python packages
pip install --upgrade -r requirements.txt

# Rotate logs
sudo logrotate /etc/logrotate.d/trackify
```

## Support

For deployment issues:
- Check application logs: `/var/log/trackify/django.log`
- Check Nginx logs: `/var/log/nginx/`
- Monitor system resources: `htop`, `iotop`
- Test database connectivity
- Verify SSL certificates
