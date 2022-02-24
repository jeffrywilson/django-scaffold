from .base import *
import environ

env = environ.Env()
environ.Env.read_env()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }

DATABASES = {
    'default': {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": env("POSTGRES_DB", default="d.sqlite3"),
        "USER": env("POSTGRES_USER", default="user"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="password"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}

#change 
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mysite.com']

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend") 

ANYMAIL = {
    "SENDGRID_API_KEY": env("SENDGRID_API_KEY", default=""),
}

EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com") 
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="xxxx@gmail.com") 
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="xxxx@gmail.com")
EMAIL_PORT = 587 
EMAIL_USE_TLS = bool(env("EMAIL_USE_TLS", default=True))
SERVER_EMAIL = env("SERVER_EMAIL", default="xxxx@gmail.com")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="mypassword")

STRIPE_LIVE_MODE = bool(env("STRIPE_LIVE_MODE", default=False))

if STRIPE_LIVE_MODE:
    STRIPE_PUBLIC_KEY = env("STRIPE_LIVE_PUBLIC_KEY", default="pk_live_")
    STRIPE_SECRET_KEY = env("STRIPE_LIVE_SECRET_KEY", default="sk_live_")
    STRIPE_CLIENT_ID  = env("STRIPE_LIVE_CLIENT_ID", default="ca_live_")
else:
    STRIPE_PUBLIC_KEY = env("STRIPE_TEST_PUBLIC_KEY", default="pk_live_")
    STRIPE_SECRET_KEY = env("STRIPE_TEST_SECRET_KEY", default="sk_live_")
    STRIPE_CLIENT_ID = env("STRIPE_TEST_CLIENT_ID", default="ca_live_")

DJSTRIPE_WEBHOOK_SECRET = env("DJSTRIPE_WEBHOOK_SECRET", default="whsec_")

DJSTRIPE_WEBHOOK_VALIDATION = env("DJSTRIPE_WEBHOOK_VALIDATION", default="retrieve_event")
DJSTRIPE_WEBHOOK_EVENT_CALLBACK = env("DJSTRIPE_WEBHOOK_EVENT_CALLBACK", default="None")

# Google tag manager id
GOOGLE_TAG_MANAGER_ID = env("GOOGLE_TAG_MANAGER_ID", default='')
#Use this var to identify commit info at the top of the app - Don't use this in Production Environment
REPO_DIR = env("REPO_DIR", default='')

CUSTOMER_SERVICE=env("CUSTOMER_SERVICE", default="")

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',#env("LOG_LEVEL", default="DEBUG"),
#             'class': 'logging.FileHandler',
#             'filename': './'#env("LOG_PATH", default="/path/to/django/debug.log"),
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': env("", default="DEBUG"),
#             'propagate': True,
#         },
#     },
# }