#!/usr/bin/python3
"""Department model"""
from app.models.base import BaseModel
from app import db
from flask_login import UserMixin


class Department(db.Model, BaseModel, UserMixin):
    """Department model"""
    title = db.Column(db.String(50),  unique=True, nullable=False)
    image = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(1000))

    def __repr__(self):
        return f"User ID: {self.id} Title: {self.title}"
    