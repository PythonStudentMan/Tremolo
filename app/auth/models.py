#   app/auth/models.py

import logging

from flask_login import UserMixin, current_user
from datetime import datetime, timezone
from app import db
from app.models import Auditorias

logger = logging.getLogger(__name__)

class Roles(db.Model):
    
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    padre_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    esta_modificado = db.Column(db.Boolean, default=False)
    esta_borrado = db.Column(db.Boolean, default=False)
    #   Relación jerárquica hijos-padre
    hijos = db.relationship('Roles', backref='padre', remote_side=[id])
    #   Relación Usuarios
    usuarios = db.relationship('Usuarios', back_populates='rol', cascade='all, delete-orphan')
       
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        logger.info(f'<Rol {self.name} guardado>')        
        #   Comprobamos si el registro ya existía en Auditoría y ha sido modificado o si es un registro nuevo
        audit = Auditorias.get_one(self.__tablename__, self.id)
        if audit and self.esta_modificado:
            audit.editado_el = datetime.now(tz=timezone.utc)
            audit.editado_por = current_user.id
        else:
            audit = Auditorias(self.__tablename__, self.id)
            audit.creado_por = self.id
            audit.save()

    def delete(self):
        self.esta_borrado = True
        self.save()

    @staticmethod
    def get_all():
        return Roles.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Roles.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Roles.query.filter_by(name=name).first()
    
        

class Usuarios(db.Model, UserMixin):

    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    esta_activo = db.Column(db.Boolean, default = True)
    esta_borrado = db.Column(db.Boolean, default = False)
    esta_modificado = db.Column(db.Boolean, default = False)
    es_administrador = db.Column(db.Boolean, default = False)
    #   Clave foránea
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #   Relación
    rol = db.relationship('Roles', back_populates='usuarios', uselist=False, single_parent=True) 
   
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def __repr__ (self):
        return f'<Usuario {self.name}>'
    
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
    def get_all():
        return Usuarios.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Usuarios.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Usuarios.query.filter_by(name=name).first()
    
    @staticmethod
    def get_by_email(email):
        return Usuarios.query.filter_by(email=email).first()

    @staticmethod
    def get_activos():
        return Usuarios.query.filter_by(esta_activo=True).all()

    @staticmethod
    def get_inactivos():
        return Usuarios.query.filter_by(esta_activo=False).all()    
    
    @staticmethod
    def get_administradores():
        return Usuarios.query.filter_by(es_administrador=True).all()
