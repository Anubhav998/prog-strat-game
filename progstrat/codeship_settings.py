import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test',  # Or path to database file if using sqlite3.
        'USER': os.environ.get('MYSQL_USER'),  # Not used with sqlite3.
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),  # Not used with sqlite3.
        'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

DEBUG = True

TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))

ALLOWED_HOSTS = []

MEDIA_ROOT = PROJECT_ROOT + '/media'

MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_ROOT + '/static'

STATIC_URL = '/static/'

# Compressor Settings
COMPRESS_ENABLED = False