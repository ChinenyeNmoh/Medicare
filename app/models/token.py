#!/usr/bin/python3
"""Token model"""
from app.models.base import BaseModel
from app import db
from flask_login import UserMixin


class Token(db.Model, BaseModel, UserMixin):
    """Token model"""
    user_email = db.Column(db.String(50), db.ForeignKey('patient.email'), unique=True, nullable=False)
    email_token = db.Column(db.String(100))
    password_token = db.Column(db.String(100))
    patient = db.relationship('Patient', foreign_keys=[user_email], backref='patient_tokens')

    def __repr__(self):
        return f"User ID: {self.id} Email: {self.user_email} emailToken: {self.email_token} passwordToken: {self.password_token}"
    