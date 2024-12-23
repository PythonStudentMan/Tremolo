#   app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    name = StringField('Nombre Usuario', validators=[DataRequired(), Length(max=80)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    recuerdame = BooleanField('Recuérdame')
    submit = SubmitField('Entrar')

class RegistroForm(FlaskForm):
    name = StringField('Nombre Usuario', validators=[DataRequired(), Length(max=80)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=256)])
    submit = SubmitField('Registrar')