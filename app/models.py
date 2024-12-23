#   app/admin/models.py

import logging

from flask_login import current_user
from datetime import datetime, timezone
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