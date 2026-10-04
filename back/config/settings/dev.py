import os

from .base import *

DEBUG = True

if not SECRET_KEY:
    SECRET_KEY = "dev-only-insecure-key"

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME") or "poc_gestao",
        "USER": os.environ.get("DB_USER") or "poc",
        "PASSWORD": os.environ.get("DB_PASSWORD") or "poc",
        "HOST": os.environ.get("DB_HOST") or "127.0.0.1",
        "PORT": os.environ.get("DB_PORT") or "5433",
    }
}
