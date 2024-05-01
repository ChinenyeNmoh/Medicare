#!/usr/bin/python3
"""Department model"""
from app.models.base import BaseModel
from app import db
from flask_login import UserMixin


class Appointment(db.Model, BaseModel, UserMixin):
    """Appointment model"""
    doctor_id = db.Column(db.String(60), db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.String(60), db.ForeignKey('patient.id'), nullable=False)
    appointment_time = db.Column(db.String(60), nullable=False)
    appointment_date = db.Column(db.String(60), nullable=False)
    appointment_no = db.Column(db.String(60), nullable=False)
    appointment_comment = db.Column(db.String(1000), nullable=True)
    appointment_status = db.Column(db.String(60), nullable=True, default='Booked')
    payment_status = db.Column(db.String(60), nullable=True, default='Pending')
    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))
    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))