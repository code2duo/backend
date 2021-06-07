"""
Django settings for code2duo project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import io
import os
import sys
from pathlib import Path
import environ

import google.auth
from django.contrib.admin import AdminSite
from google.cloud import secretmanager as sm

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "very-secret"

# Environment Stage Mapping
stageEnv = "STAGE"
devStage = "dev"
dockerStage = "docker"
prodStage = "prod"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

if (
    stageEnv not in os.environ
    or os.environ[stageEnv] == devStage
    or os.environ[stageEnv] == dockerStage
):
    # For Developer Local Environments
    ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost",
        "0.0.0.0",
        "http://localhost:3000",
    ]

    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ORIGIN_WHITELIST = [
        "http://localhost:3000",
    ]
    DEBUG = True

elif os.environ[stageEnv] == prodStage:
    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ORIGIN_WHITELIST = [
        "https://app.code2duo.co",
        "http://localhost:3000",
    ]

    # Pull django-environ settings file, stored in Secret Manager
    SETTINGS_NAME = "code2duo_settings"
    _, project = google.auth.default()
    client = sm.SecretManagerServiceClient()
    name = f"projects/{project}/secrets/{SETTINGS_NAME}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env = environ.Env()
    env.read_env(io.StringIO(payload))
    SECRET_KEY = env("SECRET_KEY")
    ALLOWED_HOSTS = [
        "code2duo-2bn4xipkxa-uc.a.run.app",
        "api.code2duo.co",
    ]
    # Default false. True allows default landing pages to be visible
    DEBUG = False

# Application definition

DJANGO_CORE_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "drf_yasg",
    "channels",
]

PROJECT_APPS = [
    "authentication",
    "core",
]

INSTALLED_APPS = DJANGO_CORE_APPS + THIRD_PARTY_APPS + PROJECT_APPS

AUTH_USER_MODEL = "authentication.User"

if stageEnv not in os.environ or os.environ[stageEnv] == devStage:
    pass
elif os.environ[stageEnv] == prodStage:
    INSTALLED_APPS += ["storages"]  # for django-storages
    if "code2duo" not in INSTALLED_APPS:
        INSTALLED_APPS += ["code2duo"]  # for custom data migration

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "authentication.middleware.FirebaseAuthentication",
    ],
    "DEFAULT_RENDERER_CLASS": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # third-party
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "code2duo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "build")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "code2duo.wsgi.application"
ASGI_APPLICATION = "code2duo.asgi.application"

if stageEnv not in os.environ or os.environ[stageEnv] == devStage:
    pass
elif os.environ[stageEnv] == dockerStage or os.environ[stageEnv] == prodStage:
    # setting logging for dev environment
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s] %(levelname)s [%(module)s:%(funcName)s:%(lineno)s] %(message)s",
                "datefmt": "%d/%b/%Y %H:%M:%S",
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "verbose",
            }
        },
        "loggers": {
            "django.utils.autoreload": {
                "level": "INFO",
                "handler": ["console"],
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],  # Quiet by default!
                "propagate": False,
                "level": "DEBUG",
            },
            "django.template": {
                "level": "INFO",
                "handler": ["console"],
                "propagate": False,
            },
            "django": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "null": {
                "class": "logging.NullHandler",
            },
            "": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if (
    stageEnv not in os.environ
    or os.environ[stageEnv] == devStage
    or os.environ[stageEnv] == dockerStage
):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
elif os.environ[stageEnv] == prodStage:
    # Set this value from django-environ
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": f"/cloudsql/{env('DATABASE_CONNECTION_NAME')}",
            "USER": f"{env('DATABASE_USER_NAME')}",
            "PASSWORD": f"{env('DATABASE_PASSWORD')}",
            "NAME": f"{env('DATABASE_NAME')}",
        }
    }

# REDIS DATASTORE
if (
    stageEnv not in os.environ
    or os.environ[stageEnv] == devStage
    or os.environ[stageEnv] == dockerStage
):
    redis_host = os.environ.get("REDIS_HOST", "127.0.0.1")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
elif os.environ[stageEnv] == prodStage:
    redis_host = env("REDIS_HOST")
    redis_port = int(env("REDIS_PORT"))

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, redis_port)],
        },
    },
}

# FIREBASE CONFIG
if (
    stageEnv not in os.environ
    or os.environ[stageEnv] == devStage
    or os.environ[stageEnv] == dockerStage
):
    project_id = os.environ.get("FIREBASE_PROJECT_ID")
    private_key_id = os.environ.get("FIREBASE_PRIVATE_KEY_ID")
    private_key = os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n")
    client_email = os.environ.get("FIREBASE_CLIENT_EMAIL")
    client_id = os.environ.get("FIREBASE_CLIENT_ID")
    client_x509_cert_url = os.environ.get("FIREBASE_CLIENT_CERT_URL")

    FIREBASE_CONFIG = {
        "type": "service_account",
        "project_id": project_id,
        "private_key_id": private_key_id,
        "private_key": private_key,
        "client_email": client_email,
        "client_id": client_id,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": client_x509_cert_url,
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

if stageEnv not in os.environ or os.environ[stageEnv] == devStage:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.1/howto/static-files/
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
elif os.environ[stageEnv] == prodStage:
    # Define static storage via django-storages[google]
    DEFAULT_FILE_STORAGE = "code2duo.gcloud.GoogleCloudMediaFileStorage"
    STATICFILES_STORAGE = "code2duo.gcloud.GoogleCloudStaticFileStorage"

    GS_PROJECT_ID = env("GS_PROJECT_ID")
    GS_STATIC_BUCKET_NAME = env("GS_STATIC_BUCKET_NAME")
    GS_MEDIA_BUCKET_NAME = env("GS_MEDIA_BUCKET_NAME")

    STATIC_URL = "https://storage.googleapis.com/{}/".format(GS_STATIC_BUCKET_NAME)
    STATIC_ROOT = "static/"

    MEDIA_URL = "https://storage.googleapis.com/{}/".format(GS_MEDIA_BUCKET_NAME)
    MEDIA_ROOT = "media/"

    UPLOAD_ROOT = "media/uploads/"

    DOWNLOAD_ROOT = os.path.join(PROJECT_ROOT, "static/media/downloads")
    DOWNLOAD_URL = STATIC_URL + "media/downloads"

    STATICFILES_DIRS = []
    GS_DEFAULT_ACL = "publicRead"

AdminSite.site_header = "Code2Duo Administration"
