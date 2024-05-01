#!/usr/bin/python3
"""init file"""
from flask import Blueprint

main = Blueprint('main', __name__)

from app.main.routes.home import *
from app.main.routes.about import *
from app.main.routes.department import *
from app.main.routes.doctors import *
from app.main.routes.appointment import *
from app.main.routes.doc_details import *
from app.main.routes.appointment import *