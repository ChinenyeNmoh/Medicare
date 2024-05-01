from flask import render_template, flash, redirect, url_for, request
from app import db
import os
from sqlalchemy import or_
from flask_login import login_user, current_user, login_required
from app.doctor.forms.doctor_register import DoctorRegistrationForm, EducationForm, WorkExperienceForm
from app.doctor.forms.update import AdminDoctorUpdateForm
from app.admin.forms.hospital import HospitalRegistrationForm, HospitalUpdateForm
from app.models.patient import Patient
from app.models.doctor import  Doctor
from app.models.hospital import Hospital
from app.patient.utils import save_favicon, save_logo
from app.models.appointment import Appointment
from datetime import datetime

from app.admin.routes import admin

#hospital details
@admin.route('/create_hospital_details', methods=['GET', 'POST'], strict_slashes=False)
def create_hospital_details():
   form = HospitalRegistrationForm()
   if form.validate_on_submit():
      try:
         # Check if hospital details already exist
         hospital_count = Hospital.query.count()
         if hospital_count >= 1:
            flash('Hospital Details Already Created. You can update it.', 'warning')
            return redirect(url_for('admin.update_hospital_details'))
            
         # Extract data from the form
         name = form.name.data
         phone1 = form.phone1.data
         phone2 = form.phone2.data
         email1 = form.email1.data
         email2 = form.email2.data
         facebook = form.facebook.data
         twitter = form.twitter.data
         youtube = form.youtube.data
         instagram = form.instagram.data
         linkedin = form.linkedin.data
         location = form.location.data
         domain_name = form.domain_name.data
         favicon = form.favicon.data 
         logo = form.logo.data
            
         # Create new instance of Hospital
         new_hospital = Hospital(
                name=name,
                phone1=phone1,
                phone2=phone2,
                email1=email1,
                email2=email2,
                facebook=facebook,
                twitter=twitter,
                youtube=youtube,
                instagram=instagram,
                linkedin=linkedin,
                location=location,
                domain_name=domain_name,
                favicon=favicon,
                logo=logo
            )
            
         # Save the new hospital instance
         db.session.add(new_hospital)
         db.session.commit()
            
         flash('Hospital Details Created Successfully!', 'success')
         return redirect(url_for('admin.'))
      except Exception as e:
         flash('Error creating hospital details. Please try again.', 'danger')
         print(str(e))
    
   return render_template('hospital_details.html', form=form)
         
   
@admin.route('/update_hospital_details', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_hospital_details():
   from app import app
   form = HospitalUpdateForm()
   if form.validate_on_submit():
      print(request.form)
      try:
         hospital = Hospital.query.filter_by().first()
         if hospital:
            print(hospital)
            if form.favicon.data:
               print('form1' )
               prev_picture = os.path.join(app.root_path, 'static/images', hospital.favicon)
               print('prev', prev_picture)
               if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'favicon.png':
                  os.remove(prev_picture)
               hospital.favicon = save_favicon(form.favicon.data)
            else:
               hospital.favicon = hospital.favicon
            print(hospital.favicon)


            if form.logo.data:
               prev_picture = os.path.join(app.root_path, 'static/images', hospital.logo)
               if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'logo.png':
                  os.remove(prev_picture)
               hospital.logo = save_logo(form.logo.data)
            else:
               hospital.logo = hospital.logo
            existing_emails = [hospital.email1, hospital.email2]
                  
            # Update hospital details
            hospital.name = form.name.data or hospital.name
            hospital.email1 = form.email1.data if form.email1.data not in existing_emails else hospital.email1
            hospital.email2 = form.email2.data if form.email2.data not in existing_emails else hospital.email2
            hospital.domain_name = form.domain_name.data or hospital.domain_name
            hospital.phone1 = form.phone1.data or hospital.phone1
            hospital.phone2 = form.phone2.data or hospital.phone2
            hospital.location = form.location.data or hospital.location
            hospital.linkedin = form.linkedin.data or hospital.linkedin
            hospital.instagram = form.instagram.data or hospital.instagram
            hospital.youtube = form.youtube.data or hospital.youtube
            hospital.twitter = form.twitter.data or hospital.twitter

            db.session.commit()
            flash('Hospital details updated successfully!', 'success')
            return redirect(url_for('admin.update_hospital_details'))
         else:
            flash('No hospital details found', 'danger')
            return redirect(url_for('admin.update_hospital_details'))
      except Exception as e:
         flash(f'An error occurred: {str(e)}', 'danger')
         print(e)
         return redirect(url_for('admin.update_hospital_details'))
   # Pre-fill form with doctor's information
   hospital = Hospital.query.filter_by().first()
   if hospital:
      form.name.data = hospital.name
      form.domain_name.data = hospital.domain_name
      form.email1.data =  hospital.email1
      form.email2.data =  hospital.email2
      form.phone1.data = hospital.phone1
      form.phone2.data = hospital.phone2
      form.location.data = hospital.location
      form.linkedin.data = hospital.linkedin
      form.facebook.data = hospital.facebook
      form.instagram.data = hospital.instagram
      form.youtube.data = hospital.youtube
      form.twitter.data = hospital.twitter

   return render_template(
        'update_hospital_details.html', 
        title="Update Hospital",
        form=form,
    )


# add doctor
@admin.route('/addDoctor', methods=['GET', 'POST'], strict_slashes=False)
def addDoctor():
   form = DoctorRegistrationForm()
   if form.validate_on_submit():
      try:
         find_doc = Doctor.query.filter_by(email=form.email.data).first()
         find_user = Patient.query.filter_by(email=form.email.data).first()
         if find_doc or find_user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('admin.addDoctor'))
         else:
            passwd = form.password.data
            new_doc = Doctor(
               first_name=form.first_name.data,
               last_name=form.last_name.data,
               gender=form.gender.data, 
               age=form.age.data, 
               date_of_birth=form.date_of_birth.data, 
               email=form.email.data, 
               consultation_fee=form.consultation_fee.data,
               password=Doctor.hash_password(passwd), 
               phone_number=form.phone_number.data,
               contact_address=form.contact_address.data, 
               designation=form.designation.data, 
               bio=form.bio.data, 
               department=form.department.data 
            )
            db.session.add(new_doc)
            db.session.commit()
            flash(f'Doctor {new_doc.first_name} Added.', 'success')
            return redirect(url_for('admin.addDoctor'))
      except Exception as e:
         db.session.rollback()
         flash(str(e), 'danger')
   return render_template(
        'add_doctor.html', 
        title="Add Doctor",
        form=form
        )

#view doctors
@admin.route('/admin_view_doctors', strict_slashes=False)
@login_required
def admin_view_doctors():
    form = AdminDoctorUpdateForm()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('entries', 6, type=int)
    print(per_page)
    search_query = request.args.get('search_query', '', type=str)
    print(search_query)
    # Query departments and apply search filter
    find_doc = Doctor.query.order_by(Doctor.first_name)
    if search_query:
        find_doc = find_doc.filter(or_(Doctor.first_name.contains(search_query), Doctor.last_name.contains(search_query)))
       
    
    # Paginate the results
    find_doc = find_doc.paginate(page=page, per_page=per_page, error_out=False)
    total = find_doc.total

    return render_template(
        'admin_update_doc.html', 
        title="View Doctors", 
        form=form, 
        doctors=find_doc,
        total=total,
        per_page=per_page,
        search_query=search_query
        )

@admin.route('/admin_update_doc/<id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def admin_update_doc(id):
   form = AdminDoctorUpdateForm()
   if form.validate_on_submit():
      try:
         update_doc = Doctor.query.filter_by(id=id).first()
         if update_doc:
            update_doc.first_name = form.first_name.data
            update_doc.last_name = form.last_name.data
            update_doc.department = form.department.data
            update_doc.is_banned = form.is_banned.data
            update_doc.is_active = form.is_active.data
            update_doc.consultation_fee = form.consultation_fee.data
            update_doc.designation = form.designation.data
                
            db.session.commit()
            flash(f"Doctor {update_doc.first_name}'s info  updated", 'success')
            return redirect(url_for('admin.admin_view_doctors'))
      except Exception as e:
         flash(str(e), 'danger')
   update_doc = Doctor.query.filter_by(id=id).first()
   if update_doc:
            form.first_name.data=update_doc.first_name
            form.last_name.data=update_doc.last_name
            form.department.data=update_doc.department
            form.is_banned.data=update_doc.is_banned
            form.is_active.data=update_doc.is_active
            form.designation.data=update_doc.designation
            form.consultation_fee.data=update_doc.consultation_fee

   return render_template('admin_update_doc.html', title="Doctors", form=form)

    
#delete department
@admin.route('/delete_doc/<id>', methods= ['GET'], strict_slashes=False)
@login_required
def delete_doc(id):
        try:
            doc = Doctor.query.filter_by(id=id).first()
            if doc:
                db.session.delete(doc)
                db.session.commit()
                flash(f'Doctor deleted', 'success')
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')
        return redirect(url_for('admin.admin_view_doctors'))



@admin.route('/todays_appointments', methods=['GET'], strict_slashes=False)
@login_required
def todays_appointments():
   page = request.args.get('page', 1, type=int)
   per_page = request.args.get('entries', 6, type=int)
   search_query = request.args.get('search_query', '', type=str)

   # Get the current date and format it as a string
   todays_date = datetime.now()
   string_date = todays_date.strftime(" %A,  %d %B, %Y ")
   print(string_date)

    # Query appointments for the current date
   query = db.session.query(Appointment).join(Patient).filter(Appointment.appointment_date == string_date)
   if search_query:
      query  = query.filter(
            (Patient.first_name.contains(search_query)) | 
            (Patient.last_name.contains(search_query))
            )
   query = query.order_by(Appointment.appointment_time)
   appointments = query.paginate(page=page, per_page=per_page, error_out=False)
   total = appointments.total
   return render_template(
        'admin_todays_appointments.html', 
        title='Todays Appointments', 
        total=total, 
        appointments=appointments,
        per_page=per_page,
        search_query=search_query
    )


@admin.route('/today_appointment_details/<id>', strict_slashes=False)
@login_required
def today_appointment_details(id):
    find_app = Appointment.query.filter_by(id=id).first()
    doc = Doctor.query.filter_by(id=find_app.doctor_id).first()
    return render_template(
        'admin_appointment_details.html',
        appointments=find_app, 
        title= "Appointment Details",
        appointment_detail=find_app,
        doc=doc
        )

@admin.route('/admin_closed_appointments', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def admin_closed_appointments():
    try:
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('entries', 6, type=int)
      search_query = request.args.get('search_query', '', type=str)

        # Base query
      query = db.session.query(Appointment).join(Patient).filter(Appointment.appointment_status != "Booked")
        # Apply search filter
      if search_query:
         query = query.filter(
            (Patient.first_name.contains(search_query)) | 
            (Patient.last_name.contains(search_query))
            )
      else:
         query = query.order_by(Appointment.appointment_date, Appointment.appointment_time)
        # Paginate the results
      appointments = query.paginate(page=page, per_page=per_page, error_out=False)
      total = appointments.total
    except Exception as e:
      flash('Error retrieving Appointment data: {}'.format(str(e)), 'danger')
      total = 0
      appointments = None

    return render_template(
        'admin_closed_appointments.html', 
        title='Closed Appointments', 
        total=total, 
        appointments=appointments,
        per_page=per_page,
        search_query=search_query
    )


@admin.route('/admin_open_appointments', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def admin_open_appointments():
   try:
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('entries', 6, type=int)
      search_query = request.args.get('search_query', '', type=str)

      # Get the current date and format it as a string
      todays_date = datetime.now()
      string_date = todays_date.strftime(" %A,  %d %B, %Y ")
      print(string_date)
        # Base query
      query = db.session.query(Appointment).join(Patient).filter(Appointment.appointment_status == 'Booked', Appointment.appointment_date != string_date)
        # Apply search filter
      if search_query:
         query = query.filter(
            (Patient.first_name.contains(search_query)) | 
            (Patient.last_name.contains(search_query))
            )
      query = query.order_by(Appointment.appointment_date, Appointment.appointment_time)
        # Paginate the results
      appointments = query.paginate(page=page, per_page=per_page, error_out=False)
      total = appointments.total
   except Exception as e:
      flash('Error retrieving Appointment data: {}'.format(str(e)), 'danger')
      total = 0
      appointments = None
   return render_template(
        'admin_open_appointments.html', 
        title='Open Appointments', 
        total=total, 
        appointments=appointments,
        per_page=per_page,
        search_query=search_query
    )