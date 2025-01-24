#   app/admin/models.py

import logging

from flask_login import current_user
from datetime import date, datetime, timezone
from app import db

logger = logging.getLogger(__name__)

class Auditorias(db.Model):
    
    __tablename__ = 'auditorias'

    id = db.Column(db.Integer, primary_key = True)
    objeto_name = db.Column(db.String(30), nullable=False)
    registro_id = db.Column(db.Integer, nullable=False)
    creado_el = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), default=lambda: current_user.id if current_user.is_authenticated else None)
    editado_el = db.Column(db.DateTime,)
    editado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def __init__(self, objeto_name, registro_id):
        self.objeto_name = objeto_name
        self.registro_id = registro_id
        
    def __repr__(self):
        return f'<Auditoria del Registro {self.registro_id} de la Tabla {self.objeto_name}>'
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        logger.info(f'Guardado el registro {self.registro_id} del objeto {self.objeto_name}>')

    @staticmethod
    def get_one(objeto,registro):
        return Auditorias.query.filter_by(objeto_name=objeto, registro_id=registro).first()
    

class Instrumentos(db.Model):

    __tablename__ = 'instrumentos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    familia = db.Column(db.String(80), nullable=False)

    esta_activo = db.Column(db.Boolean, default=True)
    esta_borrado = db.Column(db.Boolean, default=False)
    esta_modificado = db.Column(db.Boolean, default=False)
    #   Relación
    musicos = db.relationship('Musicos', secondary='musicos_instrumentos',back_populates='instrumentos')

    def __init__(self, nombre, familia):
        self.nombre = nombre
        self.familia = familia

    def __repr__ (self):
        return f'<Instrumento {self.nombre}>'
                        
    def auditoria(self):
        #   Comprobamos si el registro ya existía en Auditoría y ha sido modificado o si es un registro nuevo
        audit = Auditorias.get_one(self.__tablename__, self.id)
        if audit and self.esta_modificado:
            audit.editado_el = datetime.now(tz=timezone.utc)
            audit.editado_por = current_user.id
        else:
            audit = Auditorias(self.__tablename__, self.id)
            audit.creado_por = self.id
            audit.save()

    @staticmethod
    def get_by_id(id):
        return Instrumentos.query.get(id)
    
    @staticmethod
    def get_by_nombre(nombre):
        return Instrumentos.query.filter_by(nombre=nombre).first()

    @staticmethod
    def get_by_familia(familia):
        return Instrumentos.query.filter_by(familia=familia).all()
    
    @staticmethod
    def get_all():
        return Instrumentos.query.all()


class Musicos(db.Model):

    __tablename__ = 'musicos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    telefono = db.Column(db.String(9), nullable=False)

    esta_activo = db.Column(db.Boolean, default = True)
    esta_borrado = db.Column(db.Boolean, default = False)
    esta_modificado = db.Column(db.Boolean, default = False)
    
    # Relación con Musicos_Instrumentos
    musicos_instrumentos = db.relationship('Musicos_Instrumentos', backref='musico', lazy=True)

    
    def __init__(self, nombre, apellidos, fecha_nacimiento, email, telefono):
        self.nombre = nombre
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.email = email
        self.telefono = telefono
    
    def __repr__ (self):
        return f'<Músico {self.nombre_completo}>'     
                
    def auditoria(self):
            #   Comprobamos si el registro ya existía en Auditoría y ha sido modificado o si es un registro nuevo
            audit = Auditorias.get_one(self.__tablename__, self.id)
            if audit and self.esta_modificado:
                audit.editado_el = datetime.now(tz=timezone.utc)
                audit.editado_por = current_user.id
            else:
                audit = Auditorias(self.__tablename__, self.id)
                audit.creado_por = self.id
                audit.save()

    @property
    def nombre_completo(self):
        """ Propiedad que devuelve el nombre completo del músico """
        return self.nombre + " " + self.apellidos 

    @property
    def es_menor(self):
        """ Propiedad que calcula si el músico es menor de edad """
        if self.fecha_nacimiento:
            hoy = date.today()
            edad = hoy.year - self.fecha_nacimiento.year - (
                (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
            return edad < 18
        return False

    @staticmethod
    def get_by_id(id):
        return Musicos.query.get(id)
    
    @staticmethod
    def get_by_nombrecompleto(nombre, apellidos):
        return Musicos.query.filter_by(nombre=nombre,apellidos=apellidos).first()

    @staticmethod
    def get_by_email(email):
        return Musicos.query.filter_by(email=email).first()
    
    @staticmethod
    def get_all():
        return Musicos.query.all()
    
    @staticmethod
    def get_activos():
        return Musicos.query.filter_by(esta_activo=True).all()
    
    
class Musicos_Instrumentos(db.Model):
    __tablename__ = 'musicos_instrumentos'

    id_musico = db.Column(db.Integer, db.ForeignKey('musicos.id'), primary_key=True)
    id_instrumento = db.Column(db.Integer, db.ForeignKey('instrumentos.id'), primary_key=True)
    es_principal = db.Column(db.Boolean, default=False)

