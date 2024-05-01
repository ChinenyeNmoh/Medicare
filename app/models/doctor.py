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

class Education(db.Model, BaseModel, UserMixin):
    """Education model"""
    doctor_id = db.Column(db.String(60), db.ForeignKey('doctor.id'), nullable=False)
    date_started = db.Column(db.String(4), nullable=False)
    date_ended = db.Column(db.String(4), nullable=False)
    course_of_study = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    certificate_type = db.Column(db.String(50), nullable=False)

class WorkExperience(db.Model, BaseModel, UserMixin):
    """WorkExperience model"""
    doctor_id = db.Column(db.String(60), db.ForeignKey('doctor.id'), nullable=False)
    start_date = db.Column(db.String(4), nullable=False)
    end_date = db.Column(db.String(4), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)


class WorkSchedule(db.Model, BaseModel, UserMixin):
    """WorkSchedule model"""
    doctor_id = db.Column(db.String(60), db.ForeignKey('doctor.id'), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)



class Doctor(db.Model, BaseModel, UserMixin):
    """Doctor model"""
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    contact_address = db.Column(db.String(200), nullable=False)
    is_email_verified = db.Column(db.Boolean(), nullable=True, default=True)
    consultation_fee=db.Column(db.Integer, nullable=False)
    is_banned = db.Column(db.Boolean(), nullable=True, default=False)
    is_active = db.Column(db.Boolean(), nullable=True, default=True)
    role = db.Column(db.Enum(UserRole), default=UserRole.DOCTOR)
    designation = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.String(1000), nullable=False)
    facebook = db.Column(db.String(1000), nullable=True)
    twitter = db.Column(db.String(1000),nullable=True)
    youtube = db.Column(db.String(1000), nullable=True)
    instagram = db.Column(db.String(1000), nullable=True,)
    linkedin= db.Column(db.String(1000), nullable=True,)
    picture = db.Column(db.String(20), nullable=True, default='img2.png')
    department = db.Column(db.String(200), nullable=False)
    educations = db.relationship('Education', backref='doctor', lazy=True)
    experiences = db.relationship('WorkExperience', backref='doctor', lazy=True)

    def __repr__(self):
        return f"User ID: {self.id} Email: {self.email} Name: {self.first_name} {self.last_name}"

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password.encode()).decode('utf-8')