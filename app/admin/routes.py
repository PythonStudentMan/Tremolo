#   app/admin/routes.py

import logging

from flask import render_template

from app.auth.models import Usuarios
from app.auth.decorators import admin_required

from . import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route('/admin/usuarios/')
@admin_required
def lista_usuarios():
    usuarios = Usuarios.get_all()
    return render_template('listado_usuarios.html', usuarios=usuarios)