from flask import session, render_template,  flash, redirect, url_for, request
from app.patient.forms.login import LoginForm
from app.models.patient import Patient
from app.models.token import Token
from app.patient.routes import patient
from app.patient.utils import sendMail
from flask_login import login_user, current_user, logout_user, login_required
from app.config import serialize_token
from itsdangerous import SignatureExpired
from app import  bcrypt
from app.models.doctor import Education, WorkExperience, Doctor

@patient.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    form = LoginForm()
    # Before redirecting
    prev_page = request.referrer
    if current_user.is_authenticated:
        return redirect(prev_page) if prev_page else redirect(url_for('main.home'))
    print('before validate')
    if form.validate_on_submit():
        print('after validate')
        try:
            user = Patient.query.filter_by(email=form.email.data).first()
            doc = Doctor.query.filter_by(email=form.email.data).first()
            print(doc)
            if user:
                passMatch = bcrypt.check_password_hash(user.password, form.password.data)
                if passMatch:
                    if not user.is_email_verified:
                        print(user.is_email_verified)
                        token_entry = Token.query.filter_by(user_email=form.email.data).first()
                        if token_entry:
                            try:
                                email = serialize_token.loads(token_entry.email_token, salt='email-confirm', max_age=120)
                                flash('Check your Email for email verification link', 'warning')
                            except SignatureExpired:
                                token = serialize_token.dumps(form.email.data, salt='email-confirm')
                                link = url_for('patient.confirm_email', token=token, _external=True)
                                sendMail(form.email.data, link)
                                flash('Token has expired, Another verification email has been sent to you.', 'warning')
                                return redirect(url_for('patient.login'))
                        else:
                            flash('Email verification token not found. Please register or request a new verification email.', 'danger')
                    else:
                        login_user(user, remember=form.remember.data)
                        flash('Login successful!', 'success')
                        next_page = request.args.get('next')
                        
                        if current_user.role.value == 'admin':
                            return redirect(next_page) if next_page else redirect(url_for('admin.adminDashboard'))
                        else:
                            return redirect(next_page) if next_page else redirect(url_for('patient.my_appointment'))
                else:
                    flash('Incorrect password', 'danger')
            elif doc:
                passMatch = bcrypt.check_password_hash(doc.password, form.password.data)
                if passMatch:
                    if doc.is_banned:
                        flash('Sorry you have been banned, contact admin', 'danger')
                        return redirect(url_for('patient.login'))
                    else:
                        login_user(doc, remember=form.remember.data)
                        flash('Login successful!', 'success')
                        next_page = request.args.get('next')
                        return redirect(next_page) if next_page else redirect(url_for('doctor.docDashboard'))
                else:
                    flash('Incorrect password', 'danger')
            else:
                flash('User with email not found', 'danger')
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('login.html', title="loginPage", form=form)


@patient.route("/logout", strict_slashes=False)
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
