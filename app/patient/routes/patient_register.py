from flask import session, render_template, flash, redirect, url_for, request
from app import db
from app.patient.forms.patient_register import RegistrationForm
from app.models.patient import Patient
from app.models.token import Token
from app.patient.utils import sendMail
from app.config import serialize_token
from flask_login import current_user

from app.patient.routes import patient

@patient.route('/patientRegister',  methods=['GET', 'POST'], strict_slashes=False)
def patient_register():
    """register user or agent"""
    prev_page = request.referrer
    if current_user.is_authenticated:
        return redirect(prev_page) if prev_page else redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(email=form.email.data).first()
        if patient:
            flash('Email is already in use. Choose a different one.', 'danger')
        else:
            passwd = form.password.data
            new_patient = Patient(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                gender=form.gender.data,
                age=form.age.data,
                date_of_birth=form.date_of_birth.data,
                email=form.email.data,
                password=Patient.hash_password(passwd),
                phone_number=form.phone_number.data,
                contact_address=form.contact_address.data,
            )
            db.session.add(new_patient)
            db.session.commit()
            email = new_patient.email
            # Generate a confirmation token and URL
            try:
                token = serialize_token.dumps(email, salt='email-confirm')
                email_token = Token(
                     user_email = email,
                     email_token = token
                )
                db.session.add(email_token)
                db.session.commit()
                link = url_for('patient.confirm_email', token=token, _external=True)
                sendMail(email, link, form.first_name.data)
                flash('A confirmation email has been sent via email.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(str(e), 'danger')
                return redirect(url_for('patient.patient_register'))  # Redirect the user to the registration page
            return redirect(url_for('patient.login'))
    return render_template('patient_register.html', title="patientRegister", form=form)

