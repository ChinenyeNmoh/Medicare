#!/usr/bin/python3
"""user model"""
from app.models.base import BaseModel
from app import db, bcrypt
from flask_login import UserMixin
from enum import Enum

class UserRole(Enum):
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    PATIENT = 'patient'



class Patient(db.Model, BaseModel, UserMixin):
    """patient model"""
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_email_verified = db.Column(db.Boolean, nullable=False, default=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.PATIENT)
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    contact_address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User ID: {self.id} Email: {self.email}"
    
    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password.encode()).decode('utf-8')




    