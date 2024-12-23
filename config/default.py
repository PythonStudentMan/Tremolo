# config/default.py

from os.path import abspath, dirname, join

# Definimos el directorio de la aplicación
BASE_DIR = dirname(dirname(abspath(__file__)))

# Definimos el directorio de medios
MEDIA_DIR = join(BASE_DIR, 'media')
POSTS_IMAGES_DIR = join(MEDIA_DIR, 'posts')

# Configuraciones de acceso a Base de Datos
SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Entornos App
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'dev'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'prod'
APP_ENV = ''

# Parámetros para envíos de email (correos dirigidos al Administrador del Sistema - Logs y similares)
#MAIL_SERVER = 'mi servidor SMTP'
#MAIL_PORT = 587
#MAIL_USER = 'mi correo'
#MAIL_PASSWORD = 'mi contraseña'
#DONT_REPLY_FROM_EMAIL = '(Pablo, pjmunozcorella@gmail.com)'
#ADMINS = ('pjmunozcorella@gmail.com', )
#MAIL_USE_TLS = True
#MAIL_DEBUG = False

# Parámetros de paginación de listas
#ITEMS_PER_PAGE = 3