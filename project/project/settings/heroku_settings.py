from .base import *
import django_heroku

MIDDLEWARE = MIDDLEWARE + ['whitenoise.middleware.WhiteNoiseMiddleware',]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '679(fv75xk@2!7x-6kln0=0=8^9xroui01mzsr4s=w(3pdrum+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST          = 'mail.ideamakr.com'
EMAIL_HOST_USER     = 'donotreply@ideamakr.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL  = 'donotreply@ideamakr.com'
EMAIL_PORT          = 2525
EMAIL_USE_TLS       = False
SERVER_EMAIL        = 'donotreply@ideamakr.com'

django_heroku.settings(locals())
