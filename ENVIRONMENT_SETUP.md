# Configuration des Environnements

## Variables d'environnement

Créer les fichiers suivants selon votre environnement:

### `.env` (racine du projet)
```bash
# Configuration générale
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Base de données
DATABASE_URL=sqlite:///db.sqlite3
# ou pour PostgreSQL:
# DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Paiement
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-secret
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Storage (optionnel)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=eu-west-1
```

### `cmz/settings/local.py` (développement)
```python
from .base import *
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Email en console pour développement
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Désactiver certaines sécurités en dev
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
```

### `cmz/settings/production.py` (production)
```python
from .base import *
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Base de données depuis URL
DATABASES['default'] = dj_database_url.config(
    default=os.getenv('DATABASE_URL')
)

# Sécurité HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Email production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
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

## Docker Compose pour développement

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - ./media:/app/media
    environment:
      - DEBUG=True
      - SECRET_KEY=dev-secret-key
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: wagtailcms
      POSTGRES_USER: wagtail
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### `docker-compose.prod.yml`
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DJANGO_SETTINGS_MODULE=cmz.settings.production
    env_file:
      - .env
    depends_on:
      - db
      - redis
    volumes:
      - static_volume:/app/static
      - media_volume:/app/media

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/var/www/static
      - media_volume:/var/www/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine

volumes:
  postgres_data:
  static_volume:
  media_volume:
```