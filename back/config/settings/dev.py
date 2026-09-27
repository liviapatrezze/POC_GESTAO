from .base import *

DEBUG = True

if not SECRET_KEY:
    SECRET_KEY = "dev-only-insecure-key"

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
