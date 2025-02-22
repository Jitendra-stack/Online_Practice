from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-fallback-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

# ✅ Fixed ALLOWED_HOSTS Handling
DEFAULT_ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Ensure local development hosts are included when running locally
if DEBUG:  
    ALLOWED_HOSTS.extend(DEFAULT_ALLOWED_HOSTS)

ALLOWED_HOSTS.append(".onrender.com")  # Ensure Render subdomains are included
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))  # Remove duplicates

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'submit',
    'home',
    'solveproblems',
    'whitenoise.runserver_nostatic',  # ✅ Ensure Whitenoise is installed
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.Users'

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Added for static files
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'codeverse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'codeverse.wsgi.application'

# ✅ Fixed Database Handling
IS_LOCAL = DEBUG  # Using DEBUG to determine local/production

if IS_LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("DB_NAME", "default_db"),
            'USER': os.getenv("DB_USER", "default_user"),
            'PASSWORD': os.getenv("DB_PASSWORD", "default_password"),
            'HOST': os.getenv("DB_HOST", "localhost"),  # ✅ DB_HOST fixed
            'PORT': os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,  # Optimize DB connections
            ssl_require=True  # Ensure secure connection
        )
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static Files Fixes
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # ✅ Required for Whitenoise

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging for debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_errors.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': True,
        },
    },
}
