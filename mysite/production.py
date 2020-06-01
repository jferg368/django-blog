from .settings import *
from mysite import app_utils

db = app_utils.DatabaseCreds()

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'djangodb',
            'USER': db.user,
            'PASSWORD': db.password,
            'HOST': db.host,
            'PORT': db.port
        }
    }

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = app_utils.get_allowed_hosts()
STATIC_ROOT = os.path.join(BASE_DIR, "static")

key = app_utils.SecretKey()
SECRET_KEY = key.secret_key
