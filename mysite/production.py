import os

import dj_database_url

from .settings import *
from mysite import app_utils

# db = app_utils.DatabaseCreds()

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
    )
}

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = app_utils.get_allowed_hosts()
STATIC_ROOT = os.path.join(BASE_DIR, "static")

key = app_utils.SecretKey()
SECRET_KEY = key.secret_key
