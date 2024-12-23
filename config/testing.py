# app/config/testing.py

from .default import *

# Parámetros para activar el modo Debug
TESTING = True
DEBUG = True

APP_ENV = APP_ENV_TESTING

WTF_CSRF_ENABLED = False