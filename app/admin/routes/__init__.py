#!/usr/bin/python3
"""init file"""
from flask import Blueprint

admin = Blueprint('admin', __name__)

from app.admin.routes.admin_dashboard import *
from app.admin.routes.features import *