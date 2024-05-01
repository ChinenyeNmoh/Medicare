from flask import Flask, render_template, flash, redirect, url_for, request
from app.patient.forms.reset import RequestResetForm, ResetPasswordForm
from app.models.patient import Patient
from app.models.token import Token
from app.config import serialize_token
from itsdangerous import SignatureExpired, BadData
from app.patient.utils import sendResetMail
from app import db
from app.models.doctor import  Doctor

from app.patient.routes import patient

@patient.route('/resetPassword',  methods=['GET', 'POST'], strict_slashes=False)
def passwordReset():
    """Reset password route"""
    try:
        form = RequestResetForm()
        if form.validate_on_submit():
            userEmail = form.email.data
            user = Patient.query.filter_by(email=userEmail).first()
            doc = Doctor.query.filter_by(email=userEmail).first()
            print(doc)
            print(doc.is_email_verified)
            if user:
                if not user.is_email_verified:
                    flash('You have not verified your email. Check your email for the verification link.', 'warning')
                    return redirect(url_for('patient.login'))
                else:
                    token = serialize_token.dumps(userEmail, salt='reset-password')
                    link = url_for('patient.update_password', token=token, _external=True)
                    sendResetMail(userEmail, link, user.first_name)
                    flash('An email has been sent with instructions to reset your password.', 'success')
            elif doc:
                token = serialize_token.dumps(userEmail, salt='reset-password')
                link = url_for('patient.update_password', token=token, _external=True)
                sendResetMail(userEmail, link, doc.first_name)
                flash('An email has been sent with instructions to reset your password.', 'success')
            else:
                flash('User not found. Please check the email address entered.', 'danger')
                return redirect(url_for('patient.login'))
    except Exception as e:
        flash('An error occurred: {}'.format(str(e)), 'danger')
        return redirect(url_for('patient.login'))
    
    return render_template('reset_password.html', title="passwordPage", form=form)


@patient.route("/update_password/<token>", methods=['GET', 'POST'])
def update_password(token):
    """Update password route"""
    form = ResetPasswordForm()
    try:
        email = serialize_token.loads(token, salt='reset-password', max_age=3600)  # Adjust max_age as needed
        user = Patient.query.filter_by(email=email).first()
        doc = Doctor.query.filter_by(email=email).first()
        if user:
            if form.validate_on_submit():
                hashed_password = Patient.hash_password(form.password.data)
                user.password = hashed_password
                db.session.commit()
                flash('Your password has been updated! You are now able to log in.', 'success')
                return redirect(url_for('patient.login'))
        elif doc:
            if form.validate_on_submit():
                hashed_password = Doctor.hash_password(form.password.data)
                doc.password = hashed_password
                db.session.commit()
                flash('Your password has been updated! You are now able to log in.', 'success')
                return redirect(url_for('patient.login'))
        else:
            flash('Invalid token or user not found.', 'danger')
            return redirect(url_for('patient.login'))
    except SignatureExpired:
        flash('Token has expired. Please request a new password reset.', 'danger')
        return redirect(url_for('patient.login'))
    except BadData:
        flash('Invalid token.', 'danger')
        return redirect(url_for('patient.login'))

    return render_template('update_password.html', title="Update Password", form=form)
