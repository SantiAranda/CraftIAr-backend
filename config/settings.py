import os
from pathlib import Path
<<<<<<< HEAD
=======
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env si existe
load_dotenv()
>>>>>>> origin/feature/integracion-rag

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
<<<<<<< HEAD
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "changeme")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

allowed_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(",") if host.strip()]

=======
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-development-only')

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
>>>>>>> origin/feature/integracion-rag

# Application definition

INSTALLED_APPS = [
<<<<<<< HEAD
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "channels",
    "django_celery_results",
    "django_celery_beat",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
=======
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías de terceros
    'rest_framework',
    'django_filters',
    'corsheaders',
    'pgvector',
    
    # Aplicaciones locales
    'users.apps.UsersConfig',
    'catalog.apps.CatalogConfig',
    'orders.apps.OrdersConfig',
    'chatbot',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Debe ir lo más arriba posible
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
>>>>>>> origin/feature/integracion-rag
            ],
        },
    },
]

<<<<<<< HEAD
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

postgres_host = os.environ.get("POSTGRES_HOST")
if postgres_host:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "ecommercedb"),
            "USER": os.environ.get("POSTGRES_USER", "ecommerceuser"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "ecommercepass"),
            "HOST": postgres_host,
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        },
        "rag": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("RAG_DB_NAME", "ragdb"),
            "USER": os.environ.get("POSTGRES_USER", "raguser"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "ragpass"),
            "HOST": os.environ.get("RAG_DB_HOST", "db"),
            "PORT": os.environ.get("RAG_DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_LOCATION = "static"
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / STATIC_LOCATION

MEDIA_LOCATION = "media"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / MEDIA_LOCATION

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/1"
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get("REDIS_URL", "redis://localhost:6379/0")],
        },
    }
}

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
=======
WSGI_APPLICATION = 'config.wsgi.application'

# Configuración de Base de Datos
# Soporta PostgreSQL con pgvector si está configurado en .env, si no, usa SQLite como fallback de desarrollo
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG
        )
    }
    print("Base de datos: Conectado a PostgreSQL externo.")
else:
    # Usar SQLite como fallback de desarrollo.
    # NOTA: pgvector requiere PostgreSQL. Para desarrollo local sin Postgres, las búsquedas vectoriales fallarán.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("Base de datos: Usando SQLite local (fallback de desarrollo).")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-ar' # Configurado para español de Argentina
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración de Rest Framework y JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS Configuración
CORS_ALLOW_ALL_ORIGINS = True # Cambiar a orígenes específicos en producción
CORS_ALLOW_CREDENTIALS = True

# Celery Configurations (Usando Redis como Broker en MVP)
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER = os.environ.get('CELERY_TASK_ALWAYS_EAGER', str(DEBUG)).lower() == 'true'

# Configuración de Autenticación de Google (OAuth 2.0)
GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID', '')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET', '')

# Configuración de APIs externas para IA (Google Gemini, Groq y Hugging Face)
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]
>>>>>>> origin/feature/integracion-rag
