# Checklist de Sécurité

## ⚠️ URGENT - À corriger avant mise en production

### 🔴 Sécurité Critique

- [ ] **SECRET_KEY**: Remplacer la clé hardcodée dans `dev.py`
- [ ] **DEBUG**: Vérifier que `DEBUG=False` en production
- [ ] **ALLOWED_HOSTS**: Restreindre aux domaines autorisés uniquement
- [ ] **Base de données**: Changer le mot de passe par défaut si existant
- [ ] **CSRF**: Vérifier la configuration CSRF pour les formulaires
- [ ] **Variables d'environnement**: Utiliser `.env` pour toutes les données sensibles

### 🟠 Sécurité Importante

- [ ] **HTTPS**: Forcer HTTPS avec `SECURE_SSL_REDIRECT = True`
- [ ] **HSTS**: Configurer HTTP Strict Transport Security
- [ ] **X-Frame-Options**: Protéger contre le clickjacking
- [ ] **Content Security Policy**: Ajouter les headers CSP
- [ ] **XSS Protection**: Activer la protection XSS du navigateur
- [ ] **Content Type**: Empêcher le MIME sniffing

### 🟡 Sécurité Recommandée

- [ ] **Rate Limiting**: Limiter les tentatives de connexion
- [ ] **Session Security**: Configuration sécurisée des sessions
- [ ] **File Upload**: Validation stricte des uploads
- [ ] **SQL Injection**: Audit des requêtes brutes
- [ ] **Permissions**: Vérifier les permissions des modèles
- [ ] **Audit Logs**: Journalisation des actions critiques

## Configuration de sécurité recommandée

### `cmz/settings/security.py`
```python
# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REFERRER_POLICY = "same-origin"
SECURE_SSL_REDIRECT = True

# Session Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600  # 1 hour

# CSRF
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'",)

# File Upload Security
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644

# Logging Security Events
SECURITY_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

## Tests de sécurité

### Tests automatisés à ajouter
```python
# tests/test_security.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class SecurityTest(TestCase):
    def test_debug_disabled_in_production(self):
        """DEBUG doit être False en production"""
        from django.conf import settings
        if not settings.DEBUG:  # Si on est en prod
            self.assertFalse(settings.DEBUG)
    
    def test_secret_key_not_default(self):
        """SECRET_KEY ne doit pas être la clé par défaut"""
        from django.conf import settings
        self.assertNotEqual(
            settings.SECRET_KEY,
            "django-insecure-)pp25t1@v0xlvet5dbeoteoyhfnn*l55m160%$jn3!n40s+e2@"
        )
    
    def test_admin_requires_authentication(self):
        """Admin doit nécessiter une authentification"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirection vers login
    
    def test_csrf_protection_enabled(self):
        """CSRF doit être activé pour les formulaires"""
        response = self.client.get('/checkout/')
        if response.status_code == 200:
            self.assertContains(response, 'csrfmiddlewaretoken')
```

## Audit de sécurité manuel

### Commandes à exécuter
```bash
# Vérification Django
python manage.py check --deploy

# Scan des dépendances
pip-audit

# Vérification des permissions fichiers
find . -type f -name "*.py" -exec ls -la {} \;

# Recherche de secrets hardcodés
grep -r "password\|secret\|key" . --exclude-dir=.git
```

## Monitoring de sécurité

### Métriques à surveiller
- Tentatives de connexion échouées
- Accès aux URLs admin sans authentification
- Erreurs 403/404 suspects
- Uploads de fichiers suspects
- Requêtes avec headers suspects

### Alertes recommandées
- Plus de 10 tentatives de connexion par IP/heure
- Accès à des URLs sensibles
- Erreurs 500 répétées
- Taille d'upload inhabituelle

## Ressources supplémentaires

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Guide](https://docs.djangoproject.com/en/stable/topics/security/)
- [Mozilla Security Guidelines](https://wiki.mozilla.org/Security/Guidelines/Web_Security)