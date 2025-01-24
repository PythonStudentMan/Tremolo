#   app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, DateField, BooleanField, SubmitField, SelectField, SearchField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Email, Length, Optional
from datetime import date
from .models import Instrumentos

class MusicoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=80)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(max=80)])
    fecha_nacimiento = DateField('Fecha Nacimiento', validators=[DataRequired()])
    es_menor = BooleanField('Es Menor de Edad', render_kw={'disabled': True})
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=256)])
    telefono = StringField('Telefono', validators=[DataRequired(), Length(max=9)])
    instrumentos = SelectMultipleField('Instrumentos', choices=[], coerce=int)
    instrumento_principal = RadioField('Instrumento Principal', choices=[], coerce=int)
    submit = SubmitField('Registrar')

def __init__(self, *args, **kwargs):
        super(MusicoForm, self).__init__(*args, **kwargs)
        self.instrumentos.choices = [(i.id, i.nombre) for i in Instrumentos.get_all()]
        self.instrumento_principal.choices = self.instrumentos.choices


class InstrumentoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=80)])
    familia = StringField('Familia', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Registrar')