#   app/admin/routes.py

import logging

from flask import render_template, redirect, url_for, current_app
from flask_login import login_required, current_user

from app.auth.models import Usuarios
from app.auth.decorators import admin_required

from . import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route('/admin/usuarios/')
def lista_usuarios():
    usuarios = Usuarios.get_all()
    return render_template('listado_usuarios.html', usuarios=usuarios)