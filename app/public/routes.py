#   app/public/routes.py

import logging

from flask import render_template, redirect, url_for, current_app, request
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit

from app import login_manager

from .templates import public_bp

logger = logging.getLogger(__name__)

@public_bp.route('/')
def index():
    return render_template('public/index.html')