#   app/admin/routes.py

from datetime import date
import logging

from flask import abort, flash, render_template, request, redirect, url_for
from urllib.parse import urlsplit
from app import db
from app.models import Musicos, Instrumentos, Musicos_Instrumentos
from app.forms import MusicoForm, InstrumentoForm
from app.auth.decorators import admin_required

from . import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route('/admin/instrumentos/')
def lista_instrumentos():
    instrumentos = Instrumentos.get_all()
    return render_template('admin/listado_instrumentos.html', instrumentos=instrumentos)

@admin_bp.route('/admin/musicos/')
def lista_musicos():
    musicos = Musicos.get_all()
    return render_template('admin/listado_musicos.html', musicos=musicos)

@admin_bp.route("/admin/instrumento/", methods=['GET', 'POST'])
def instrumento_form():
    #   Instanciamos un nuevo formulario
    form = InstrumentoForm()
    if form.validate_on_submit():
        instrumento = Instrumentos(form.nombre.data, form.familia.data)
        db.session.add(instrumento)
        db.session.commit()
        #instrumento.auditoria()
        next_page = request.args.get('next', None)
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('admin.lista_instrumentos')
        return redirect(next_page)
    return render_template("admin/instrumento_form.html", form=form)

@admin_bp.route("/admin/instrumento/<int:instrumento_id>/", methods=['GET', 'POST'])
def update_instrumento_form(instrumento_id):
    #   Actualiza Instrumento existente
    instrumento = Instrumentos.get_by_id(instrumento_id)
    if instrumento is None:
        logger.info(f'El instrumento {instrumento_id} NO existe')
        abort(404)
    #   Creamos el formulario inicializando los campos con los valores del instrumento
    form = InstrumentoForm(obj=instrumento)
    if form.validate_on_submit():
        #   Actualizamos los campos del instrumento existente
        instrumento.nombre = form.nombre.data
        instrumento.familia = form.familia.data
        instrumento.esta_modificado = True
        if not instrumento.id:
            db.session.add(instrumento)
        db.session.commit()
        #instrumento.auditoria()
        next_page = request.args.get('next', None)
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('admin.lista_instrumentos')
        return redirect(next_page)
    return render_template("admin/instrumento_form.html", form=form, instrumento=instrumento)


@admin_bp.route("/admin/musico/<int:musico_id>/seleccionar_instrumentos", methods=['GET', 'POST'])
def seleccionar_instrumentos(musico_id):
    musico = Musicos.get_by_id(musico_id)
    if musico is None:
        logger.info(f'El músico {musico_id} NO existe')
        abort(404)
    
    instrumentos = Instrumentos.get_all()
    if request.method == 'POST':
        selected_instrumentos = request.form.getlist('instrumentos')
        Musicos_Instrumentos.query.filter_by(id_musico=musico_id).delete()
        for instrumento_id in selected_instrumentos:
            musico_instrumento = Musicos_Instrumentos(id_musico=musico_id, id_instrumento=instrumento_id)
            db.session.add(musico_instrumento)
        db.session.commit()
        return redirect(url_for('admin.lista_musicos'))
    
    return render_template('admin/seleccionar_instrumentos.html', musico=musico, instrumentos=instrumentos)

@admin_bp.route("/admin/musico/", methods=['GET', 'POST'])
def musico_form():
    form = MusicoForm()
    if form.validate_on_submit():
        musico = Musicos(form.nombre.data, form.apellidos.data, form.fecha_nacimiento.data, form.email.data, form.telefono.data)
        db.session.add(musico)
        db.session.commit()
        selected_instrumentos = form.instrumentos.data
        for instrumento_id in selected_instrumentos:
            es_principal = (instrumento_id == form.instrumento_principal.data)
            musico_instrumento = Musicos_Instrumentos(id_musico=musico.id, id_instrumento=instrumento_id, es_principal=es_principal)
            db.session.add(musico_instrumento)
        db.session.commit()
        next_page = request.args.get('next', None)
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('admin.lista_musicos')
        return redirect(next_page)
    return render_template("admin/musico_form.html", form=form)

@admin_bp.route("/admin/musico/<int:musico_id>/", methods=['GET', 'POST'])
def update_musico_form(musico_id):
    musico = Musicos.query.get_or_404(musico_id)
    form = MusicoForm(obj=musico)
    if request.method == 'POST' and form.validate_on_submit():
        musico.nombre = form.nombre.data
        musico.apellidos = form.apellidos.data
        musico.fecha_nacimiento = form.fecha_nacimiento.data
        musico.email = form.email.data
        musico.telefono = form.telefono.data
        db.session.commit()
        Musicos_Instrumentos.query.filter_by(id_musico=musico_id).delete()
        selected_instrumentos = form.instrumentos.data
        for instrumento_id in selected_instrumentos:
            es_principal = (instrumento_id == form.instrumento_principal.data)
            musico_instrumento = Musicos_Instrumentos(id_musico=musico.id, id_instrumento=instrumento_id, es_principal=es_principal)
            db.session.add(musico_instrumento)
        db.session.commit()
        next_page = request.args.get('next', None)
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('admin.lista_musicos')
        return redirect(next_page)
    else:
        form.instrumentos.data = [mi.id_instrumento for mi in musico.musicos_instrumentos]
        form.instrumento_principal.data = next((mi.id_instrumento for mi in musico.musicos_instrumentos if mi.es_principal), None)
    return render_template("admin/musico_form.html", form=form, musico=musico)