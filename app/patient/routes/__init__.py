#!/usr/bin/python3
"""init file"""
from flask import Blueprint

patient = Blueprint('patient', __name__)


from app.patient.routes.patient_register import *
from app.patient.routes.login import *
from app.patient.routes.patient_dashboard import *
from app.patient.routes.confirm_email import *
from app.patient.routes.reset_password import *
