from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         'TEST': {
#             'NAME': 'test_scaffold',
#         },
#     }
# }

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'scaffold_ci',
        'USER':     'ci_user',
        'PASSWORD': 'ci_user',
        'HOST':     'localhost',
        'PORT':     '5432',
    }
}

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST          = 'mail.ideamakr.com'
EMAIL_HOST_USER     = 'donotreply@ideamakr.com'
DEFAULT_FROM_EMAIL  = 'donotreply@ideamakr.com'
EMAIL_PORT          = 2525
EMAIL_USE_TLS       = False
SERVER_EMAIL        = 'donotreply@ideamakr.com'
EMAIL_HOST_PASSWORD = ''

STRIPE_LIVE_MODE = False


STRIPE_TEST_PUBLIC_KEY = os.environ['STRIPE_TEST_PUBLIC_KEY']
STRIPE_TEST_SECRET_KEY = os.environ['STRIPE_TEST_SECRET_KEY']
STRIPE_TEST_CLIENT_ID = os.environ['STRIPE_TEST_CLIENT_ID']

DJSTRIPE_WEBHOOK_VALIDATION = os.environ['DJSTRIPE_WEBHOOK_VALIDATION']
DJSTRIPE_WEBHOOK_SECRET = os.environ['DJSTRIPE_WEBHOOK_SECRET']
#DJSTRIPE_WEBHOOK_EVENT_CALLBACK = 'project.celery.webhook_event_callback'

STRIPE_PUBLIC_KEY = STRIPE_TEST_PUBLIC_KEY
STRIPE_SECRET_KEY = STRIPE_TEST_SECRET_KEY
STRIPE_CLIENT_ID = STRIPE_TEST_CLIENT_ID