#!/usr/bin/python3
"""Message model"""
from app.models.base import BaseModel
from app import db
from flask_login import UserMixin


class Message(db.Model, BaseModel, UserMixin):
    """message model"""
    name = db.Column(db.String(120),  nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.String(1000), nullable=False)
    message_status = db.Column(db.String(30), nullable=False, default='Submitted')