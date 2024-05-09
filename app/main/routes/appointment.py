from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, login_required
import secrets
from app.models.appointment import Appointment
from app import db
from datetime import datetime, timedelta
from app.models.doctor import  Doctor, WorkSchedule
from app.models.hospital import Hospital
from app.models.patient import Patient
from app.patient.utils import sendAppointmentMail

from app.main.routes import main

def generate_appointment_days():
    appointment_days = []
    day_of_week = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = today + timedelta(days=7)
    
    while today < end_of_week:
        time_slot = today.strftime(" %d %B, %Y ")
        days = today.strftime(" %A")
        appointment_days.append(time_slot)
        day_of_week.append(days)
        today += timedelta(days=1)
    
    return appointment_days, day_of_week

def generate_appointment_slots(start_time, end_time):
    appointment_slots = []
    today = datetime.now().replace(hour=start_time, minute=0, second=0, microsecond=0)
    end_of_day = today.replace(hour=end_time, minute=0, second=0, microsecond=0)
    
    while today < end_of_day:
        time_slot = today.strftime("%H:%M")
        appointment_slots.append(time_slot)
        today += timedelta(minutes=30)
    
    return appointment_slots

def generate_int_time(start_time,end_time):
    str_time = start_time.strftime('%H')
    ed_time = end_time.strftime('%H')
    if  int(str_time) < 10 :
        startTime = str_time[1:]
    else:
        startTime = str_time

    if  int(ed_time) < 10 :
        endTime = ed_time[1:]
    else:
        endTime = ed_time
    return int(startTime), int(endTime)


@main.route('/appointment/<id>', strict_slashes=False)
@login_required 
def appointment(id):
    appointment_days, day_names = generate_appointment_days()

    appointment_info = zip(appointment_days, day_names)
    doc_time = WorkSchedule.query.filter_by(doctor_id=id).all()
    doc = Doctor.query.filter_by(id=id).first()
    appointment_day = request.args.get('appointment_day')
    day_name = request.args.get('day_name')
    appoint_time = request.args.get('appointment_time')
    booked_app = Appointment.query.filter_by(doctor_id=id).all()
    appointment_dict = {}
    current = datetime.now()
    current_str = current.strftime(" %d %B, %Y ").strip()
    print(current_str)
    for t in booked_app:
        if t.appointment_status == 'Booked':
            appointment_date, appoint_d = t.appointment_date.split(',', 1)
            appointment_date=appointment_date.strip()
            print('appointment',appointment_date)
            appoint_d=appoint_d.strip()
            print(appoint_d)
            appointment_time = t.appointment_time.strip()
            if appoint_d > current_str:
                appointment_dict[appointment_date] = appointment_time

    print(appointment_dict)
    try:
        if appointment_day and day_name and appoint_time:
            docs = Doctor.query.filter_by(id=current_user.id).first()
            if docs or current_user.id == id:
                flash('Select a patient to book appointment for', 'warning ')
                return redirect(url_for('doctor.all_patients'))
            find_app = Appointment.query.filter_by(doctor_id=id, patient_id=current_user.id, appointment_status='Booked').first()
            print(find_app)
            if find_app:
                flash(f'You have a pending appointment with doctor {doc.first_name}. You can book with another doctor', 'warning')
                return redirect(url_for('patient.my_appointment'))
            else:
                new_appointment = Appointment(
                    doctor_id=id,
                    patient_id=current_user.id,
                    appointment_time=appoint_time,
                    appointment_date=f"{day_name}, {appointment_day}",
                    appointment_no=secrets.token_hex(4)
                )
                db.session.add(new_appointment)
                db.session.commit()
                hospital = Hospital.query.first()
                sendAppointmentMail(
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
                    consultation_fee=new_appointment.doctor.consultation_fee,
                    payment_status=new_appointment.payment_status,
                    appointment_status=new_appointment.appointment_status,
                    location=hospital.location,
                    clinic_phone1=hospital.phone1,
                    clinic_email1=hospital.email1
                    )
                flash('New appointment created. A confirmation mail has been sent to your email', 'success')
                return redirect(url_for('patient.my_appointment'))
    except Exception as e:
        flash(f'Error creating appointment: {e}', 'danger')
        return redirect(url_for('main.appointment', id=id))

    context = {
        'title': "appointmentPage",
        'appointment_info': appointment_info,
        'doc_time': doc_time,
        'generate_appointment_slots': generate_appointment_slots,
        'generate_int_time': generate_int_time,
        'doc': doc,
        'now': datetime.now(),
        'appointment_dict': appointment_dict
        
    }

    return render_template('book_appointment.html', **context)


@main.route('/doc_book_appointment/<id>', strict_slashes=False)
@login_required 
def doc_book_appointment(id):
    appointment_days, day_names = generate_appointment_days()

    appointment_info = zip(appointment_days, day_names)
    doc_time = WorkSchedule.query.filter_by(doctor_id=current_user.id).all()
    pat = Patient.query.filter_by(id=id).first()
    appointment_day = request.args.get('appointment_day')
    day_name = request.args.get('day_name')
    appoint_time = request.args.get('appointment_time')
    booked_app = Appointment.query.filter_by(doctor_id=current_user.id).all()
    appointment_dict = {}
    current = datetime.now()
    current_str = current.strftime(" %d %B, %Y ").strip()
    print(current_str)
    for t in booked_app:
        if t.appointment_status == 'Booked':
            appointment_date, appoint_d = t.appointment_date.split(',', 1)
            appointment_date=appointment_date.strip()
            print('appointment',appointment_date)
            appoint_d=appoint_d.strip()
            print(appoint_d)
            appointment_time = t.appointment_time.strip()
            if appoint_d > current_str:
                appointment_dict[appointment_date] = appointment_time

    print(appointment_dict)
    try:
        if appointment_day and day_name and appoint_time:
            find_app = Appointment.query.filter_by(doctor_id=current_user.id, patient_id=id, appointment_status='Booked').first()
            print(find_app)
            if find_app:
                flash(f'You have a pending appointment with patient {pat.first_name}. Update the pending appointment to book', 'warning')
                return redirect(url_for('doctor.doc_appointments'))
            else:
                new_appointment = Appointment(
                    doctor_id=current_user.id,
                    patient_id=id,
                    appointment_time=appoint_time,
                    appointment_date=f"{day_name}, {appointment_day}",
                    appointment_no=secrets.token_hex(4)
                )
                db.session.add(new_appointment)
                db.session.commit()
                hospital = Hospital.query.first()
                sendAppointmentMail(
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
                    consultation_fee=new_appointment.doctor.consultation_fee,
                    payment_status=new_appointment.payment_status,
                    appointment_status=new_appointment.appointment_status,
                    location=hospital.location,
                    clinic_phone1=hospital.phone1,
                    clinic_email1=hospital.email1
                    )
                flash('New appointment created. A confirmation mail has been sent to patients email', 'success')
                return redirect(url_for('doctor.doc_appointments'))
    except Exception as e:
        flash(f'Error creating appointment: {e}', 'danger')
        return redirect(url_for('doctor.all_patients', id=id))

    context = {
        'title': "appointmentPage",
        'appointment_info': appointment_info,
        'doc_time': doc_time,
        'generate_appointment_slots': generate_appointment_slots,
        'generate_int_time': generate_int_time,
        'pat': pat,
        'now': datetime.now(),
        'appointment_dict': appointment_dict
        
    }

    return render_template('doc_book_patient_appointment.html', **context)
