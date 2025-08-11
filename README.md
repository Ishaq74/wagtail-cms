# CMS E-commerce avec Wagtail

## Vue d'ensemble du projet

Ce projet est un site e-commerce complet développé avec **Wagtail CMS** (basé sur Django 5.0.9) comprenant un système de gestion de contenu, une boutique en ligne, un panier d'achat, un système de commandes et de facturation.

### 🎯 Objectif
Créer une plateforme e-commerce française complète avec:
- Gestion de produits avec variantes et options
- Panier d'achat et système de commande
- Gestion des utilisateurs et comptes
- Blog intégré
- Pages flexibles avec StreamFields
- Gestion des taxes et expéditions
- Système de facturation

## 📁 Architecture du projet

### Applications Django

| Application | Description | Fonctionnalité |
|------------|-------------|----------------|
| **home** | Page d'accueil | Page principale avec blocs de contenu personnalisés |
| **product** | Gestion produits | Modèles de produits avec variantes, catégories, tags |
| **cart** | Panier | Gestion du panier d'achat, items, sessions |
| **checkout** | Commande | Processus de commande et validation |
| **orders** | Commandes | Gestion des commandes finalisées |
| **accounts** | Comptes utilisateur | Authentification, profils personnalisés |
| **factures** | Facturation | Génération et gestion des factures |
| **expeditions** | Expéditions | Gestion des livraisons |
| **taxes** | Taxes | Calcul et gestion des taxes produits |
| **devises** | Devises | Gestion des devises (multi-currency) |
| **blog** | Blog | Articles, catégories, système de blog |
| **businesslocal** | Référencement local | SEO et référencement local |
| **service** | Services | Pages de services |
| **search** | Recherche | Fonctionnalité de recherche globale |
| **streams** | Blocs personnalisés | StreamFields et blocs réutilisables |
| **flex** | Pages flexibles | Pages avec contenu flexible |
| **layout** | Mise en page | Composants de mise en page |
| **site_settings** | Paramètres | Configuration globale du site |
| **smtp** | Email | Configuration et gestion des emails |
| **theme** | Thème | Styles Tailwind CSS |

### 🏗️ Stack technique

- **Framework**: Django 5.0.9
- **CMS**: Wagtail 6.2.2
- **Base de données**: SQLite3 (développement)
- **CSS**: Tailwind CSS 3.8.0
- **Frontend**: Django templates + StreamFields
- **Authentification**: CustomUser model
- **Paiement**: PayPal REST SDK, Stripe
- **Container**: Docker
- **Python**: 3.8.1

## 🚀 Installation et configuration

### Prérequis
- Python 3.8+
- Node.js et npm
- Git

### 1. Cloner le projet
```bash
git clone https://github.com/Ishaq74/wagtail-cms.git
cd wagtail-cms
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de l'environnement
Créer un fichier `cmz/settings/local.py`:
```python
from .base import *

# Configuration locale
DEBUG = True
SECRET_KEY = 'votre-clé-secrète-unique'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### 5. Migrations et données initiales
```bash
python manage.py migrate
python manage.py loaddata db.json  # Données de démonstration
python manage.py createsuperuser
```

### 6. Compilation des assets (Tailwind)
```bash
cd theme
npm install
npm run build
# ou en mode développement
npm run dev
```

### 7. Lancer le serveur
```bash
python manage.py runserver
```

Le site sera accessible sur `http://localhost:8000`
L'administration Wagtail sur `http://localhost:8000/admin/`

## 🚨 PROBLÈMES IDENTIFIÉS

### 🔴 Critiques (Sécurité)

1. **SECRET_KEY exposée** dans `dev.py`
   ```python
   # ❌ PROBLÈME
   SECRET_KEY = "django-insecure-)pp25t1@v0xlvet5dbeoteoyhfnn*l55m160%$jn3!n40s+e2@"
   
   # ✅ SOLUTION
   import os
   SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key-for-dev')
   ```

2. **ALLOWED_HOSTS trop permissif**
   ```python
   # ❌ PROBLÈME
   ALLOWED_HOSTS = ["*"]
   
   # ✅ SOLUTION
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'votre-domaine.com']
   ```

3. **DEBUG=True en production potentiel**
   - Le fichier `production.py` n'a pas de SECRET_KEY ni ALLOWED_HOSTS définis
   - Risque d'exposition d'informations sensibles

### 🟠 Importantes (Fonctionnalité/Performance)

4. **requirements.txt corrompu**
   - Fichier encodé en UTF-16 au lieu d'UTF-8
   - Rend l'installation impossible
   - **CORRIGÉ** dans ce PR

5. **Version Python obsolète**
   ```dockerfile
   # ❌ PROBLÈME - Dockerfile ligne 2
   FROM python:3.8.1-slim-buster
   
   # ✅ SOLUTION
   FROM python:3.11-slim-bullseye
   ```

6. **Path NPM Windows spécifique**
   ```python
   # ❌ PROBLÈME - base.py ligne 80
   NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
   
   # ✅ SOLUTION
   NPM_BIN_PATH = shutil.which("npm")
   ```

7. **Base de données SQLite en production**
   - Non adapté pour la production
   - Recommandation: PostgreSQL ou MySQL

### 🟡 Améliorations suggérées

8. **Manque de tests**
   - Seulement 12 fichiers de test trouvés
   - Couverture insuffisante pour un e-commerce

9. **Gestion des erreurs**
   - Pas de pages d'erreur personnalisées (404, 500)
   - Manque de logging configuré

10. **Configuration email incomplète**
    - Seulement `console.EmailBackend` en développement
    - Pas de configuration SMTP pour production

11. **Sécurité supplémentaire manquante**
    - Pas de HTTPS forcing
    - Pas de Content Security Policy (CSP)
    - Pas de rate limiting

## 🛠️ CORRECTIONS URGENTES À APPLIQUER

### 1. Sécurité immédiate
```python
# cmz/settings/base.py - Ajouter
SECURE_SSL_REDIRECT = True  # En production
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

### 2. Variables d'environnement
Créer un fichier `.env`:
```bash
SECRET_KEY=votre-clé-ultra-secrète
DEBUG=False
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre-email
EMAIL_HOST_PASSWORD=votre-mot-de-passe
```

### 3. Configuration production
```python
# cmz/settings/production.py - Compléter
import dj_database_url
import os

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database from URL
DATABASES['default'] = dj_database_url.config(
    default=os.environ.get('DATABASE_URL')
)
```

## 📈 AMÉLIORATIONS RECOMMANDÉES

### Performance
1. **Cache Redis/Memcached**
2. **CDN pour assets statiques**
3. **Optimisation images automatique**
4. **Lazy loading des produits**

### UX/UI
1. **Interface mobile-first**
2. **PWA (Progressive Web App)**
3. **Recherche avancée avec filtres**
4. **Recommandations produits**

### Développement
1. **Tests automatisés complets**
2. **CI/CD avec GitHub Actions**
3. **Monitoring et alertes**
4. **Documentation API**

### E-commerce
1. **Système d'avis clients**
2. **Programme de fidélité**
3. **Codes promotionnels**
4. **Gestion stock temps réel**
5. **Analytics e-commerce**

## 🚀 Déploiement

### Docker (Recommandé)
```bash
docker build -t wagtail-cms .
docker run -p 8000:8000 wagtail-cms
```

### Heroku
```bash
# Procfile
web: gunicorn cmz.wsgi:application --port $PORT
release: python manage.py migrate

# Configuration
heroku config:set SECRET_KEY=votre-clé
heroku config:set DEBUG=False
```

### VPS/Serveur dédié
1. **Nginx** comme proxy inverse
2. **Gunicorn** comme serveur WSGI
3. **PostgreSQL** comme base de données
4. **Redis** pour le cache
5. **Let's Encrypt** pour SSL

## 🔧 Scripts utiles

### Développement
```bash
# Lancer en mode développement
python manage.py runserver

# Créer migrations
python manage.py makemigrations

# Appliquer migrations
python manage.py migrate

# Créer superutilisateur
python manage.py createsuperuser

# Collecter fichiers statiques
python manage.py collectstatic

# Compilation Tailwind
cd theme && npm run dev
```

### Production
```bash
# Backup base de données
python manage.py dumpdata > backup.json

# Optimiser base de données
python manage.py optimize_db

# Vérification sécurité
python manage.py check --deploy
```

## 📚 Documentation supplémentaire

- [Documentation Wagtail](https://wagtail.org/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [Guide sécurité Django](https://docs.djangoproject.com/en/stable/topics/security/)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amélioration`)
3. Commit (`git commit -am 'Ajout fonctionnalité'`)
4. Push (`git push origin feature/amélioration`)
5. Pull Request

## 📄 License

Ce projet est sous licence [à définir].

---

## 🆘 Support

Pour toute question ou problème:
1. Vérifier cette documentation
2. Consulter les issues GitHub existantes
3. Créer une nouvelle issue avec détails complets

**⚠️ ATTENTION**: Ce projet contient des vulnérabilités de sécurité qui DOIVENT être corrigées avant toute mise en production !