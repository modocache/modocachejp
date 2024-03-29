import os
import djcelery


djcelery.setup_loader()


HEROKU_NECESSARY_ENVKEYS = [
    'DJANGO_DEBUG_TRUE',
    'DJANGO_SECRET_KEY',
    'AWS_ACCESS_KEY_ID_MODOCACHEJP',
    'AWS_SECRET_ACCESS_KEY_MODOCACHEJP',
    'AWS_STORAGE_BUCKET_NAME_MODOCACHEJP',
    'AWS_STATIC_URL_MODOCACHEJP',
]
DEVELOPMENT_NECESSARY_ENVKEYS = HEROKU_NECESSARY_ENVKEYS + [
    'DJANGO_POSTGRESQL_USERNAME',
]


DEBUG = os.environ.has_key('DJANGO_DEBUG_TRUE')
TEMPLATE_DEBUG = STATIC_DEBUG = DEBUG

if os.environ.has_key('DJANGO_SECRET_KEY'):
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
else:
    SECRET_KEY = '6^=-_@l(1tcxx!fc!_9=6b*x8vhl!@6keucf-h9@y0@lw7(-lx'

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('modocache', 'modocache@gmail.com'),
)
MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'modocachejp',
        'USER':     os.environ.get('DJANGO_POSTGRESQL_USERNAME'),
        'PASSWORD': '',
        'HOST':     '',
        'PORT':     '',
    }
}
CACHES = {
    'default': {
        'BACKEND':  'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    },
}
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ''


TIME_ZONE = 'Atlantic/Reykjavik' # UTC+00
BLOGS_DEFAULT_TIME_ZONE = 'Asia/Tokyo'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
SITE_NAME = 'mjp'
if DEBUG:
    SITE_DOMAIN = 'localhost:8000'
else:
    SITE_DOMAIN = 'modocache.jp'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID_MODOCACHEJP')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY_MODOCACHEJP')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME_MODOCACHEJP')
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = os.environ.get('AWS_STATIC_URL_MODOCACHEJP', '/static/')
if STATIC_DEBUG:
    STATIC_URL = '/static/'
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'modocachejp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'modocachejp.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'modocachejp.context_processors.site_details',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'gunicorn',
    'djcelery',
    'kombu.transport.django',
    'storages',
    'south',
    'compressor',
    'memcache_status',

    'blogs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


BROKER_BACKEND = 'kombu.transport.django.Transport'
CELERY_RESULT_DBURI = DATABASES['default']


# django_compressor
COMPRESS_ENABLED = True
COMPRESS_ROOT = os.path.join(PROJECT_DIR, 'static')
COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
