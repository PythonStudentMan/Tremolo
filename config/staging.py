# config/staging.py

from .default import *

# Parámetros para activación del modo Debug
TESTING = True
DEBUG = True

APP_ENV = APP_ENV_TESTING

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Administrator:Ecnlsnd?2024.@localhost:3306/tremolo'