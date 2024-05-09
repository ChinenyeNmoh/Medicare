from flask import  render_template, flash, redirect, url_for,request
from app.models.department import Department
from app import db
from flask_login import login_user, current_user, login_required
from app.doctor.forms.doctor_register import DoctorRegistrationForm, EducationForm, WorkExperienceForm, WorkScheduleForm
from app.doctor.forms.appointment import UpdateAppointmentForm
from app.models.doctor import Education, WorkExperience, Doctor, WorkSchedule
from app.models.appointment import Appointment
from app.models.patient import Patient
from sqlalchemy import literal, join

from app.doctor.routes import doctor

#admin dashboard
@doctor.route('/docDashboard', strict_slashes=False)
@login_required
def docDashboard():
    closed = Appointment.query.filter(Appointment.doctor_id == current_user.id, Appointment.appointment_status !='Booked').count()
    op = Appointment.query.filter(Appointment.doctor_id == current_user.id, Appointment.appointment_status =='Booked').count()
    all = Appointment.query.filter_by(doctor_id = current_user.id).count()
    return render_template(
        'doc_default.html', 
        title= "Doctor Dashboard",
        cls=closed,
        op=op,
        all=all
        )

# add experience
@doctor.route('/addDetails', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def addDetails():
   experience_form = WorkExperienceForm()
   education_form = EducationForm()
   schedule_form=WorkScheduleForm()
   if experience_form.validate_on_submit():
      try:
         new_ex = WorkExperience(
            doctor_id=current_user.id,
            start_date=experience_form.start_date.data,
            end_date=experience_form.end_date.data,
            company=experience_form.company.data,
            position=experience_form.position.data
         )

         db.session.add(new_ex)
         db.session.commit()
         flash('New experience added successfully.', 'success')
         return redirect(url_for('doctor.addDetails'))  # Redirect back to addExperience page for further additions
      except Exception as e:
         db.session.rollback()
         flash(str(e), 'danger')
   elif education_form.validate_on_submit():
      try:
         new_ed = Education(
            doctor_id=current_user.id,
            date_started=education_form.date_started.data,
            date_ended=education_form.date_ended.data,
            school=education_form.school.data,
            certificate_type=education_form.certificate_type.data,
            course_of_study=education_form.course_of_study.data
         )

         db.session.add(new_ed)
         db.session.commit()
         flash('New Education added successfully.', 'success')
         return redirect(url_for('doctor.addDetails'))  # Redirect back to addExperience page for further additions
      except Exception as e:
         db.session.rollback()
         flash(str(e), 'danger')
   elif schedule_form.validate_on_submit():
      try:
         work_day = schedule_form.day_of_week.data
         find_day = WorkSchedule.query.filter_by(doctor_id=current_user.id, day_of_week=work_day).first()
         if find_day:
            flash(f'Schedule already exist for {work_day}', 'danger')
         else:
            print('start time', schedule_form.start_time.data)
            print('end time', schedule_form.end_time.data)
            new_schedule = WorkSchedule(
               doctor_id=current_user.id,
               day_of_week=schedule_form.day_of_week.data,
               start_time=schedule_form.start_time.data,
               end_time=schedule_form.end_time.data,
            )
            db.session.add(new_schedule)
            db.session.commit()
            flash('Schedule added successfully.', 'success')
            return redirect(url_for('doctor.addDetails'))  # Redirect back to addExperience page for further additions
      except Exception as e:
         db.session.rollback()
         flash(str(e), 'danger')
   return render_template(
        'experience.html', 
        title="Add Experience",
        experience_form=experience_form,
        education_form=education_form,
        schedule_form=schedule_form
        )

@doctor.route('/doc_appointments', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def doc_appointments():
    try:
      page = request.args.get('page', 1, type=int)
      per_page = 10
      status = request.args.get('status', '', type=str)
      search_query = request.args.get('search_query', '', type=str)

        # Base query
      if status:
         if status == "open_appointments":
            query = db.session.query(Appointment).join(Patient).filter(Appointment.doctor_id == current_user.id, Appointment.appointment_status =='Booked')
         elif status == 'closed_appointments':
           query = db.session.query(Appointment).join(Patient).filter(Appointment.doctor_id == current_user.id, Appointment.appointment_status !='Booked')
         else:
            query = db.session.query(Appointment).join(Patient).filter(Appointment.doctor_id == current_user.id)
      else:
         query = db.session.query(Appointment).join(Patient).filter(Appointment.doctor_id == current_user.id)

        # Apply search filter
      if search_query:
         print(search_query)
         query = query.filter(
            (Patient.first_name.contains(search_query)) | 
            (Patient.last_name.contains(search_query))
            )
         print('query', query)

      query = query.order_by(Appointment.appointment_date, Appointment.appointment_time)
        # Paginate the results
      appointments = query.paginate(page=page, per_page=per_page, error_out=False)
      total = appointments.total
    except Exception as e:
        flash('Error retrieving Appointment data: {}'.format(str(e)), 'danger')
        total = 0
        appointments = Appointment.query.filter(literal(False))

    return render_template(
        'all_doc_appointment.html', 
        title='All Appointments', 
        total=total, 
        appointments=appointments,
        per_page=per_page,
        search_query=search_query
    )


        
@doctor.route('/doc_appointment_details/<id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def doc_appointment_details(id):
    form = UpdateAppointmentForm()
    find_app = Appointment.query.filter_by(id=id).first()
    if request.method == 'GET':
       if find_app.appointment_comment:
         form.appointment_comment.data = find_app.appointment_comment
    if form.validate_on_submit():
        if find_app:
            find_app.payment_status = form.payment_status.data if form.payment_status.data else find_app.payment_status
            find_app.appointment_status = form.appointment_status.data if form.appointment_status.data else find_app.appointment_status
            find_app.appointment_comment = form.appointment_comment.data if form.appointment_comment.data else find_app.appointment_comment
            db.session.commit()
            if find_app.appointment_status == 'Cancelled':
               db.session.delete(find_app)
               db.session.commit()
               flash('Appointment cancelled successfully!', 'success')
               return redirect(url_for('doctor.doc_appointments'))
            else:
               flash('Appointment information updated successfully!', 'success')
               return redirect(url_for('doctor.doc_appointment_details', id=id))
        else:
            flash('Appointment not found', 'danger')
            return redirect(url_for('doctor.doc_appointment_details', id=id))

    return render_template(
        'doc_appointment_details.html', 
        title="My Appointments",
        appointment_detail=find_app,
        form=form
    )


@doctor.route('/all_patients', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def all_patients():
    try:
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('entries', 6, type=int)
      search_query = request.args.get('search_query', '', type=str)

      unique_patient_ids = set()
      pats = Appointment.query.filter_by(doctor_id = current_user.id).all()
      for ids in pats:
         unique_patient_ids.add(ids.patient_id)
        # Base query
      query = Patient.query.filter(Patient.id.in_(unique_patient_ids))
        # Apply search filter
      if search_query:
         query = query.filter(
            (Patient.first_name.contains(search_query)) | 
            (Patient.last_name.contains(search_query))
            )
      else:
         query = query.order_by(Patient.first_name)
      # Paginate the results
      patients = query.paginate(page=page, per_page=per_page, error_out=False)
     
      total = patients.total
    except Exception as e:
      flash('Error retrieving patients data: {}'.format(str(e)), 'danger')
      total = 0
      patients = db.session.query(Appointment).join(Patient).filter(literal(False))


    return render_template(
        'doc_all_patient.html', 
        title='All patients', 
        total=total, 
        patients=patients,
        per_page=per_page,
        search_query=search_query
    )
        