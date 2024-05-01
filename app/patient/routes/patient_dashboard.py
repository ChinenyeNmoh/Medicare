from flask import  render_template, flash, redirect, url_for, request
from app.models.patient import Patient
from app import db
from flask_login import login_user, current_user, login_required
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.hospital import Hospital
from app.patient.utils import sendCancelAppointmentMail
from app.patient.forms.update_acct import UpdateForm

from app.patient.routes import patient

@patient.route('/patientDashboard', strict_slashes=False)
@login_required
def patientDashboard():
    return render_template('my_appointments.html', title= "dashboardPage")

@patient.route('/my_profile', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def my_profile():
    form = UpdateForm()
    if form.validate_on_submit():
        try:
            update_user = Patient.query.filter_by(email=current_user.email).first()
            if update_user:
                update_user.first_name = form.first_name.data if form.first_name.data else update_user.first_name
                update_user.last_name = form.last_name.data if form.last_name.data else update_user.last_name
                update_user.gender = form.gender.data if form.gender.data else update_user.gender
                update_user.age = form.age.data if form.age.data else update_user.age
                update_user.date_of_birth = form.date_of_birth.data if form.date_of_birth.data else update_user.date_of_birth
                update_user.phone_number = form.phone_number.data if form.phone_number.data else update_user.phone_number
                update_user.contact_address = form.contact_address.data if form.contact_address.data else update_user.contact_address
                db.session.commit()
                flash('Account updated', 'success')
                return redirect(url_for('patient.my_profile'))
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(url_for('patient.my_profile'))
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data=current_user.last_name
        form.age.data=current_user.age
        form.gender.data=current_user.gender
        form.email.data=current_user.email
        form.date_of_birth.data=current_user.date_of_birth
        form.phone_number.data=current_user.phone_number
        form.contact_address.data = current_user.contact_address

    
    return render_template('my_account.html', title="My Profile", form=form)


@patient.route('/my_appointment', strict_slashes=False)
@login_required
def my_appointment():
    find_app = Appointment.query.filter_by(patient_id=current_user.id, appointment_status='Booked').all()
    return render_template(
        'my_appointments.html',
        appointments=find_app, 
        title= "My Appointments"
        )
@patient.route('/closed_appointment', strict_slashes=False)
@login_required
def closed_appointment():
    find_app = Appointment.query.filter(Appointment.patient_id == current_user.id, Appointment.appointment_status != 'Booked').all()
    return render_template(
        'my_appointments.html',
        appointments=find_app, 
        title= "My Appointments"
        )

@patient.route('/my_appointment_details/<id>', strict_slashes=False)
@login_required
def my_appointment_details(id):
    find_app = Appointment.query.filter_by(id=id).first()
    doc = Doctor.query.filter_by(id=find_app.doctor_id).first()
    return render_template(
        'my_appointment_details.html',
        appointments=find_app, 
        title= "My Appointments",
        appointment_detail=find_app,
        doc=doc
        )


@patient.route('/cancel_appointment/<id>', strict_slashes=False)
@login_required
def cancel_appointment(id):
    new_appointment = Appointment.query.filter_by(id=id).first()
    if new_appointment:
        # Extract doctor information using the backref
        doctor_info = new_appointment.doctor
        hospital = Hospital.query.first()
        sendCancelAppointmentMail(
                new_appointment.patient.email,
                    first_name=new_appointment.patient.first_name,
                    last_name=new_appointment.patient.last_name,
                    date=new_appointment.appointment_date,
                    appointment_number=new_appointment.appointment_no,
                    time=new_appointment.appointment_time,
                    doc_first_name=new_appointment.doctor.first_name,
                    doc_last_name=new_appointment.doctor.last_name,
                    department=new_appointment.doctor.department,
                    designation=new_appointment.doctor.designation,
                    appointment_status=new_appointment.appointment_status,
                    location=hospital.location,
                    clinic_phone1=hospital.phone1,
                    clinic_email1=hospital.email1
                    )
        db.session.delete(new_appointment)
        db.session.commit()
        
        flash(f'Appointment with doctor {doctor_info.first_name} canceled successfully.', 'success')
        return redirect(url_for('patient.my_appointment', id=id))
    else:
        flash('Appointment not found', 'danger')
        return redirect(url_for('patient.my_appointment', id=id))
