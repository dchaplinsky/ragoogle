"""
Django settings for edrdr project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "tg=jh69mhw%*rd)o93^e5d8gu6+2v!)y5dy+$o$o&qt_io*#)c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []
LANGUAGE_CODE = "uk"
SITE_ID = 1
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "pipeline",
    "ckeditor",
    "ckeditor_uploader",
    "abstract",

    # Here goes data sources
    "smida.apps.SmidaConfig",
    "posipaky_info.apps.PosipakyInfoConfig",
    "posipaky_2_info.apps.Posipaky2InfoConfig",
    "edrdr.apps.EDRDRConfig",
    "garnahata_in_ua.apps.GarnahataInUaConfig",
    "vkks.apps.VKKSConfig",
    "nacp_declarations.apps.NACPDeclarationsConfig",
    "paper_declarations.apps.PaperDeclarationsConfig",
    "cvk_2015.apps.CVK2015Config",
    "smida_reports.apps.SmidaReportConfig",
    "dabi_licenses.apps.DabiLicensesConfig",
    "dabi_registry.apps.DabiRegistryConfig",

    # Generalized search
    "search",
    "raven.contrib.django.raven_compat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ragoogle.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [os.path.join(BASE_DIR, "jinja2")],
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "jinja2_env.environment",
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "extensions": [
                "pipeline.jinja2.PipelineExtension",
                "jinja2.ext.i18n",
                "jinja2.ext.with_",
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

STATICFILES_STORAGE = "pipeline.storage.PipelineCachedStorage"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'pipeline.finders.CachedFileFinder',
    "pipeline.finders.PipelineFinder",
)

PIPELINE = {
    'COMPILERS': ('pipeline.compilers.sass.SASSCompiler',),
    'SASS_ARGUMENTS': '-q',
    'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CssminCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    'STYLESHEETS': {
        'css_all': {
            'source_filenames': (
                'scss/main.scss',
            ),
            'output_filename': 'css/merged.css',
            'extra_context': {},
        }
    },
    'JAVASCRIPT': {
        'js_all': {
            'source_filenames': (
                "js/core/jquery.min.js",
                "js/core/bootstrap.bundle.min.js",
                "js/core/jquery.slimscroll.min.js",
                "js/core/jquery.scrollLock.min.js",
                "js/core/jquery.appear.min.js",
                "js/core/jquery.countTo.min.js",
                "js/core/js.cookie.min.js",
                "js/core/bootstrap3-typeahead.js",
                "js/bihus.js",
                "js/main.js",
                "js/common.js",
                "js/autocomplete.js",
            ),
            'output_filename': 'js/merged.js',
        }
    }
}

STATIC_URL = '/static/'
WSGI_APPLICATION = "ragoogle.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        # Strictly PostgreSQL
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ragoogle",
        "USER": "ragoogle",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "uk"

gettext = lambda s: s
LANGUAGES = (("uk", gettext("Ukrainian")),)


TIME_ZONE = "Europe/Kiev"
USE_I18N = False
USE_L10N = True
USE_TZ = True

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"

PROXY = None

NUM_THREADS = 8
CATALOG_PER_PAGE = 24

# Setup Elasticsearch default connection
ELASTICSEARCH_CONNECTIONS = {"default": {"hosts": "localhost", "timeout": 30}}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'importer': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    },
}

try:
    from .local_settings import *
except ImportError:
    pass


# # Init Elasticsearch connections
from elasticsearch_dsl import connections

connections.connections.configure(**ELASTICSEARCH_CONNECTIONS)

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]

    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    INTERNAL_IPS = ["127.0.0.1"]
