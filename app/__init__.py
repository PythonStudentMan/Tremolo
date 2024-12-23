#   app/__init__.py

import logging

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from logging.handlers import SMTPHandler

from app.common.filters import format_datetime

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app(settings_module='config.dev'):

    app = Flask(__name__, instance_relative_config=True)

    # Cargamos los parámetros de configuración según el entorno
    app.config.from_object(settings_module)

    # Cargamos la configuración del directorio Instance (parámetros que no forman parte del historial de veriones)
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)

    configure_logging(app)

    login_manager.init_app(app)
    login_manager.login_view='auth.login'

    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)

    # Registro de los Filtros
    register_filters(app)

    #   Registramos los Blueprints
    from .auth import auth_bp   
    app.register_blueprint(auth_bp)  
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    from .public import public_bp
    app.register_blueprint(public_bp)

    # Manejadores de errores personalizados
    register_error_handlers(app)
    
    with app.app_context():
        db.create_all()
        
    return app


# Función para realizar filtros en formato de fecha personalizado
def register_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime

# Función para registrar los manejadores de errores de la aplicación
def register_error_handlers(app):

    @app.errorhandler(500)
    def error_500_handler(e):
        return render_template('500.html'), 500
    
    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(401)
    def error_401_handler(e):
        return render_template('401.html'), 401
    
# Modificando la configuración del logger por defecto de Flask
def configure_logging(app):
    # Eliminamos los posibles manejadores que puedan existir del logger por defecto
    del app.logger.handlers[:]

    # Añadimos el logger por defecto a la lista de loggers
    loggers = [app.logger, ]
    handlers = []
    
    # Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())
    
    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.DEBUG)   
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)
        # Enviamos correo al Administrador
        mail_handler = SMTPHandler((app.config['MAIL_SERVER'],
                                   app.config['MAIL_PORT']),    
                                   app.config['DONT_REPLY_FROM_EMAIL'],
                                   app.config['ADMINS'],
                                   '[Error][{}] La aplicación falló'.format(app.config['APP_ENV']),
                                   (app.config['MAIL_USERNAME'],
                                    app.config['MAIL_PASSWORD']),
                                    ())
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)
    # Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

# Formateador de Mensajes de Log por Consola
def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

# Formateador de Mensajes de Log por Email al Admin
def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d
            Message:
            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )
