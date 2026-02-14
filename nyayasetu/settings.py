from pathlib import Path

# ---------------------------------
# Base Directory
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------
# Security Settings
# ---------------------------------
SECRET_KEY = 'django-insecure-your-secret-key'  # keep your existing one
DEBUG = True
ALLOWED_HOSTS = []

# ---------------------------------
# Installed Apps
# ---------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # your app
]

# ---------------------------------
# Middleware
# ---------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------
# URL Configuration
# ---------------------------------
ROOT_URLCONF = 'nyayasetu.urls'

# ---------------------------------
# Templates
# ---------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # optional project-level templates
        'APP_DIRS': True,  # enable loading templates inside app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------------------------
# WSGI Application
# ---------------------------------
WSGI_APPLICATION = 'nyayasetu.wsgi.application'

# ---------------------------------
# Database (SQLite)
# ---------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------
# Password Validators
# ---------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------
# Internationalization
# ---------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ---------------------------------
# Static Files (CSS, JS, Images)
# ---------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # project-level static folder

# For production: optional static root
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------------------------
# Default Primary Key Field Type
# ---------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os

GOOGLE_API_KEY = "AIzaSyDhbQKXE04BBcnO62XqitihpkNJYlPyMyE"


