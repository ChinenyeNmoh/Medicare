from flask import  render_template, flash, redirect, url_for,request
from app.models.department import Department
import os
import secrets
from app.patient.utils import save_picture
from sqlalchemy import case
from flask_login import login_user, current_user, login_required
from app.doctor.forms.update import DoctorUpdateForm, UpdateEducationForm, UpdateWorkExperienceForm, UpdateWorkScheduleForm
from app.models.doctor import Education, WorkExperience, Doctor, WorkSchedule
from app.doctor.routes import doctor
from app import db
from PIL import Image


@doctor.route('/update_personal_info', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_personal_info():
    from app import app
    form = DoctorUpdateForm()

    if form.validate_on_submit():
        try:
            find_doc = Doctor.query.filter_by(id=current_user.id).first()
            if find_doc:
                print('in update doctor')
                
                find_doc.gender = form.gender.data or find_doc.gender
                find_doc.age = form.age.data or find_doc.age
                if form.picture.data:
                    prev_picture = os.path.join(app.root_path, 'static/images/team', find_doc.picture)
                    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'img2.png':
                        os.remove(prev_picture)
                    find_doc.picture = save_picture(form.picture.data)
                else:
                    find_doc.picture = find_doc.picture
                find_doc.date_of_birth = form.date_of_birth.data or find_doc.date_of_birth
                find_doc.phone_number = form.phone_number.data or find_doc.phone_number
                find_doc.contact_address = form.contact_address.data or find_doc.contact_address
                find_doc.bio = form.bio.data or find_doc.bio
                find_doc.linkedin = form.linkedin.data or find_doc.linkedin
                find_doc.facebook = form.facebook.data or find_doc.facebook
                find_doc.instagram = form.instagram.data or find_doc.instagram
                find_doc.youtube = form.youtube.data or find_doc.youtube
                find_doc.twitter = form.twitter.data or find_doc.twitter

                db.session.commit()
                flash('Personal information updated successfully!', 'success')
                return redirect(url_for('doctor.update_personal_info'))
            else:
                flash('Doctor not found', 'danger')
                return redirect(url_for('doctor.update_personal_info'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            print(e)
            return redirect(url_for('doctor.update_personal_info'))

    # Pre-fill form with doctor's information
    find_doc = Doctor.query.filter_by(id=current_user.id).first()
    if find_doc:
        form.gender.data = find_doc.gender
        form.first_name.data = find_doc.first_name
        form.last_name.data = find_doc.last_name
        form.age.data = find_doc.age
        doc_image =  url_for('static', filename='images/team/' + find_doc.picture)
        form.is_active.data = find_doc.is_active
        form.email.data = find_doc.email
        form.department.data = find_doc.department
        form.designation.data = find_doc.designation
        form.consultation_fee.data=find_doc.consultation_fee
        form.date_of_birth.data = find_doc.date_of_birth
        form.phone_number.data = find_doc.phone_number
        form.contact_address.data = find_doc.contact_address
        form.bio.data = find_doc.bio
        form.linkedin.data = find_doc.linkedin
        form.facebook.data = find_doc.facebook
        form.instagram.data = find_doc.instagram
        form.youtube.data = find_doc.youtube
        form.twitter.data = find_doc.twitter

    return render_template(
        'doc_update_profile.html', 
        title="Update Doctor",
        form=form,
        doc_image=doc_image
    )

@doctor.route('/view_details', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def view_details():
    experience_form = UpdateWorkExperienceForm()
    education_form = UpdateEducationForm()
    schedule_form=UpdateWorkScheduleForm()
    find_experience = WorkExperience.query.filter_by(doctor_id=current_user.id).all()
    find_education = Education.query.filter_by(doctor_id=current_user.id).order_by(Education.date_ended).all()
    doc_sc = WorkSchedule.query.filter_by(doctor_id=current_user.id).order_by(
        case(
            (WorkSchedule.day_of_week == 'Monday', 1),
            (WorkSchedule.day_of_week == 'Tuesday', 2),
            (WorkSchedule.day_of_week == 'Wednesday', 3),
            (WorkSchedule.day_of_week == 'Thursday', 4),
            (WorkSchedule.day_of_week == 'Friday', 5),
            (WorkSchedule.day_of_week == 'Saturday', 6),
            (WorkSchedule.day_of_week == 'Sunday', 7),
            else_=8
        )
    ).all()
    return render_template(
        'doc_update_details.html', 
        title="Update Details",
        experiences=find_experience,
        educations =find_education,
        experience_form=experience_form,
        education_form=education_form,
        schedule_form=schedule_form,
        schedules=doc_sc
    )


@doctor.route('/update_details/<id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_details(id):
    
    experience_form = UpdateWorkExperienceForm()
    education_form = UpdateEducationForm()
    schedule_form= UpdateWorkScheduleForm()
    find_experience = WorkExperience.query.filter_by(doctor_id=current_user.id).all()
    find_education = Education.query.filter_by(doctor_id=current_user.id).order_by(Education.date_ended).all()
    doc_sc = WorkSchedule.query.filter_by(doctor_id=current_user.id).order_by(
        case(
            (WorkSchedule.day_of_week == 'Monday', 1),
            (WorkSchedule.day_of_week == 'Tuesday', 2),
            (WorkSchedule.day_of_week == 'Wednesday', 3),
            (WorkSchedule.day_of_week == 'Thursday', 4),
            (WorkSchedule.day_of_week == 'Friday', 5),
            (WorkSchedule.day_of_week == 'Saturday', 6),
            (WorkSchedule.day_of_week == 'Sunday', 7),
            else_=8
        )
    ).all()

    if experience_form.validate_on_submit():
        try:
            ex = WorkExperience.query.filter_by(id=id).first()
            if ex:
                ex.start_date = experience_form.start_date.data if experience_form.start_date.data else ex.start_date
                ex.end_date = experience_form.end_date.data if experience_form.end_date.data else ex.end_date
                ex.company = experience_form.company.data if experience_form.company.data else ex.company
                ex.position = experience_form.position.data if experience_form.position.data else ex.position

                db.session.commit()
                flash('Work experience updated successfully.', 'success')
                return redirect(url_for('doctor.view_details'))
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')

    if education_form.validate_on_submit():
        try:
            ed = Education.query.filter_by(id=id).first()
            print('ed id',ed)
            if ed:
                ed.date_started = education_form.date_started.data if education_form.date_started.data else ed.date_started
                ed.date_ended = education_form.date_ended.data if education_form.date_ended.data else ed.date_ended
                ed.school = education_form.school.data if education_form.school.data else ed.school
                ed.certificate_type = education_form.certificate_type.data if education_form.certificate_type.data else ed.certificate_type
                ed.course_of_study = education_form.course_of_study.data if education_form.course_of_study.data else ed.course_of_study

                db.session.commit()
                flash('Education updated successfully.', 'success')
                return redirect(url_for('doctor.view_details'))
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')
    
    sc = WorkSchedule.query.filter_by(id=id).first()
    if sc:
        print(type(sc.start_time))
        print(sc.end_time)
        try:
            if sc:
                print(type(sc.start_time))
                sc.start_time = schedule_form.start_time.data if schedule_form.start_time.data else sc.start_time
                sc.end_time = schedule_form.end_time.data if schedule_form.end_time.data else sc.end_time
                db.session.commit()
                flash(f'{sc.day_of_week} schedule updated successfully.', 'success')
                return redirect(url_for('doctor.view_details'))
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')  
    return render_template(
        'doc_update_details.html', 
        title="Update Details",
        experience_form=experience_form,
        education_form=education_form,
        schedule_form=schedule_form,
        experiences=find_experience,
        educations =find_education,
        schedules=doc_sc
    )

@doctor.route('/delete_details/<id>', methods=['GET'], strict_slashes=False)
@login_required
def delete_details(id):
    experience_form = UpdateWorkExperienceForm()
    education_form = UpdateEducationForm()
    find_experience = WorkExperience.query.filter_by(doctor_id=current_user.id).all()
    find_education = Education.query.filter_by(doctor_id=current_user.id).order_by(Education.date_ended).all()
    try:
        ex = WorkExperience.query.filter_by(id=id).first()
        ed = Education.query.filter_by(id=id).first()
        if ex:
            db.session.delete(ex)
            db.session.commit()
            flash('Work experience deleted successfully.', 'success')
        elif ed:
            db.session.delete(ed)
            db.session.commit()
            flash('Education deleted successfully.', 'success') 
        else:
            flash('No detail found with the provided ID.', 'danger')
        return redirect(url_for('doctor.view_details'))
    except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')
    return render_template(
        'doc_update_details.html', 
        title="Update Details",
        experience_form=experience_form,
        education_form=education_form,
        experiences=find_experience,
        educations =find_education
    )
