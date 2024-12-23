#   app/auth/routes.py

import logging

from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit

from app import login_manager

from . import auth_bp
from .models import Usuarios
from .forms import LoginForm, RegistroForm

logger = logging.getLogger(__name__)

@auth_bp.route("/registro/", methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = RegistroForm()
    error = None
    if form.validate_on_submit():
        # Comprobamos que no exista ya un usuario con ese UserName
        usuario = Usuarios.get_by_name(form.name.data)
        if usuario is not None:
            error = f'Ya existe el usuario {form.name.data}'
        else:
            # Comprobamos que no existe ya un usuario con este email
            usuario = Usuarios.get_by_email(form.email.data)
            if usuario is not None:
                error = f'El email {form.email.data} ya está siendo utilizado por otro usuario'
            else:
                # Creamos el usuario y lo guardamos
                usuario = Usuarios(name=form.name.data, email=form.name.data)
                usuario.set_password(str(form.password.data))
                usuario.save()
                # Dejamos al usuario logueado
                login_user(usuario, remember=True)
                next_page = request.args.get('next', None)
                if not next_page or urlsplit(next_page).netloc != '':
                    next_page = url_for('public.index')
                return redirect(next_page)
    return render_template("auth/registro_form.html", form=form, error=error)

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuarios.get_by_name(form.name.data)
        if usuario:
            if usuario.check_password(form.password.data):
                login_user(usuario, remember=form.recuerdame.data)
                next_page = request.args.get('next')
                if not next_page or urlsplit(next_page).netloc != '':
                    next_page = url_for('public.index')
                return redirect(next_page)
    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.get_by_id(user_id)