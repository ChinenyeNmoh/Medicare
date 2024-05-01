from flask import Flask, render_template, flash, redirect, url_for
from app import db
from app.models.patient import Patient
from app.models.token import Token
from app.config import serialize_token
from itsdangerous import SignatureExpired, BadData
from app.patient.utils import sendMail

from app.patient.routes import patient

@patient.route('/comfirmMail/<token>',  methods=['GET', 'POST'], strict_slashes=False)
def confirm_email(token):
    """comfirm email"""
    try:
        email = serialize_token.loads(token, salt='email-confirm', max_age=120) # 3600 seconds = 1 hour
        findUser = Patient.query.filter_by(email=email).first()
        if findUser:
            if not findUser.is_email_verified:
                findUser.is_email_verified = True
                db.session.commit()
                findUser = Token.query.filter_by(user_email = email).first()
                print(findUser)
                if findUser:
                    db.session.delete(findUser)
                    db.session.commit()
                else:
                    flash('Email verified. You are now able to login', 'success')

            else:
                flash('account already confirmed. You can Login', 'info')
    except SignatureExpired:
        email = serialize_token.loads(token, salt='email-confirm', max_age=120) # 3600 seconds = 1 hour
        token = serialize_token.dumps(email, salt='email-confirm')
        link = url_for('patient.confirm_email', token=token, _external=True)
        sendMail(email, link)
        flash('Token has expired, Another verfication mail has been sent to you.', 'info')
        return redirect(url_for('patient.patient_register'))
    except BadData:
        flash('Invalid confirmation link',
              'danger')
        return redirect(url_for('patient.patient_register'))
    return redirect(url_for('patient.login'))
