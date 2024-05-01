from flask import url_for
from app import db, bcrypt, mail
from app.models.patient import Patient
from flask_mail import Message
import secrets
import os
import secrets
from PIL import Image


def save_picture(form_picture):
    from app import app
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    print("Root path:", app.root_path)
    picture_path = os.path.join(app.root_path, 'static/images/team', picture_fn)
    try:
        output_size = (800, 800)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        print("Image saved successfully")
    except Exception as e:
        print("Error saving image:", e)
    return picture_fn

def save_favicon(form_picture):
    from app import app
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    print("Root path:", app.root_path)
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    try:
        output_size = (16, 16)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        print("favicon saved successfully")
    except Exception as e:
        print("Error saving image:", e)
    return picture_fn


def save_logo(form_picture):
    from app import app
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    print("Root path:", app.root_path)
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    try:
        output_size = (170, 40)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        print("logo saved successfully")
    except Exception as e:
        print("Error saving image:", e)
    return picture_fn


def sendMail(email, link, name):
    # Send the confirmation email
    msg = Message('Confirm Email', recipients=[email])
    msg.html = f"""
    <h3>Hello {name}</h3>
    <p>Thank you for creating an account with MediCare.</p>
    <p>Please click the link below to verify your account within 24 hours:</p>
    <br/>
    <a href="{link}">Click Here</a><br/>
    <br/>
    <p>If the button above isn't working, paste the link below into your browser:</p>
    <br/>
    <p>{link}</p>
    <br/>
    <br/>
    <p>If you did not create an account with MediCare, just ignore this message.</p>
    <br/>
    <p>Thank you for choosing MediCare.</p>
    """
    mail.send(msg)

def sendResetMail(email, link, name):
    # Send the confirmation email
    msg = Message('Reset Password', recipients=[email])
    msg.html = f"""
    <h3>Hello {name}</h3>
    <p>There was recently a request to change the password on your account.<br/> 
    If you requested this password change, 
    please click the link below to set a new password within 24 hours:</p>
    <br/>
    <a href="{link}">Click Here</a><br/>
    <br/>
    <p>If the button above isn't working, paste the link below into your browser:</p>
    <br/>
    <p>{link}</p>
    <br/>
    <br/>
    <p>If you did not request password change, just ignore this message.</p>
    <br/>
    <p>Thank you for choosing MediCare.</p>
    """
    mail.send(msg)


def sendAppointmentMail(email, **kwargs):
    # Send the confirmation email
    msg = Message('Your Healthcare Appointment Confirmation', recipients=[email])
    msg.html = f"""
    <h5>Dear {kwargs.get('first_name', '')} {kwargs.get('last_name', '')}</h5>
    <p>Thank you for booking your appointment with MediCare. We are pleased to confirm your appointment as follows:</p>
    <br/>
    <p>Appointment Number: {kwargs.get('appointment_number', '')} </p><br/>
    <p>Date: {kwargs.get('date', '')} </p><br/>
    <p>Time: {kwargs.get('time', '')} </p><br/>
    <p>Doctor: {kwargs.get('doc_first_name', '')} {kwargs.get('doc_last_name', '')}</p><br/>
    <p>Department: {kwargs.get('department', '')} </p><br/>
    <p>Designation: {kwargs.get('designation', '')} </p><br/>
    <p>Consultation Fee: N{kwargs.get('consultation_fee', '')} </p><br/>
    <p>Payment Status: {kwargs.get('payment_status', '')} </p><br/>
    <p>Appointment Status: {kwargs.get('appointment_status', '')} </p><br/>
    <p>Location: {kwargs.get('location', '')} </p><br/>
    <p>Please arrive 15 minutes prior to your scheduled appointment time to complete any necessary paperwork. 
    Remember to bring your insurance card and a valid photo ID.</p>
    <br/>
    <p>If you have any questions or need to reschedule, 
    please contact us at {kwargs.get('clinic_phone1', '')} or email {kwargs.get('clinic_email1', '')}.</p>
    <br/>
    <br/>
    <p>We look forward to seeing you soon!</p>
    <br/>
    <p>Thank you for choosing MediCare.</p>
    """
    mail.send(msg)

def sendCancelAppointmentMail(email, **kwargs):
    # Send the cancellation confirmation email
    msg = Message('Your Healthcare Appointment Cancellation Confirmation', recipients=[email])
    msg.html = f"""
    <h5>Dear {kwargs.get('first_name', '')} {kwargs.get('last_name', '')}</h5>
    <p>We regret to inform you that your appointment with MediCare has been canceled.</p>
    <br/>
    <p>Appointment Number: {kwargs.get('appointment_number', '')} </p><br/>
    <p>Date: {kwargs.get('date', '')} </p><br/>
    <p>Time: {kwargs.get('time', '')} </p><br/>
    <p>Doctor: {kwargs.get('doc_first_name', '')} {kwargs.get('doc_last_name', '')}</p><br/>
    <p>Department: {kwargs.get('department', '')} </p><br/>
    <p>Designation: {kwargs.get('designation', '')} </p><br/>
    <p>Appointment Status: Cancelled </p><br/>
    <p>Location: {kwargs.get('location', '')} </p><br/>
    <p>If you have any questions or need to reschedule, 
    <p>please contact us at {kwargs.get('clinic_phone1', '')} or email {kwargs.get('clinic_email1', '')}.</p>
    <br/>
    <br/>
    <p>Thank you for choosing MediCare.</p>
    """
    mail.send(msg)


