#!/usr/bin/python3
"""init file"""
from flask import Blueprint

doctor = Blueprint('doctor', __name__)

from app.doctor.routes.doc_dashboard import *
from app.doctor.routes.update_personal_info import *