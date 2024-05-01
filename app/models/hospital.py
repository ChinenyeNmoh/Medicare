#!/usr/bin/python3
"""Department model"""
from app.models.base import BaseModel
from app import db
from flask_login import UserMixin


class Hospital(db.Model, BaseModel, UserMixin):
    """Hospital model"""
    name = db.Column(db.String(120), unique=True, nullable=False)
    phone1 = db.Column(db.String(15), nullable=False)
    phone2 = db.Column(db.String(15), nullable=True)
    email1 = db.Column(db.String(120), unique=True, nullable=False)
    email2 = db.Column(db.String(120), unique=True, nullable=True)
    facebook = db.Column(db.String(1000), nullable=True)
    twitter = db.Column(db.String(1000),nullable=True)
    youtube = db.Column(db.String(1000), nullable=True)
    instagram = db.Column(db.String(1000), nullable=True,)
    linkedin= db.Column(db.String(1000), nullable=True)
    location = db.Column(db.String(200), nullable=False)
    domain_name = db.Column(db.String(120), unique=True, nullable=False)
    favicon = db.Column(db.String(20), nullable=True, default='favicon.png')
    logo = db.Column(db.String(20), nullable=True, default='logo.png')