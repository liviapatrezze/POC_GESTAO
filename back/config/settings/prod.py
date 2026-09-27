from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False

if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY é obrigatória em produção")

if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS é obrigatório em produção")
