from flask import render_template, flash, redirect, url_for, request
from app import db
from sqlalchemy.orm import exc
from sqlalchemy import case
from app.models.department import Department
from flask_login import login_user, current_user
from app.models.patient import Patient
from app.models.doctor import Education, WorkExperience, Doctor, WorkSchedule
from app.main.routes import main

@main.route('/docDetails/<id>', strict_slashes=False)
def doc_details(id):
    try:
        doc = Doctor.query.filter_by(id=id).first()
        doc_edu = Education.query.filter_by(doctor_id=id).order_by(Education.date_ended).all()
        doc_ex = WorkExperience.query.filter_by(doctor_id=id).order_by(WorkExperience.end_date).all()
        doc_sc = WorkSchedule.query.filter_by(doctor_id=id).order_by(
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
    except exc.NoResultFound:
        flash("Doctor not found", "error")
        return redirect(url_for('main.doctors'))
    except Exception as e:
        flash("An error occurred while fetching doctor details: " + str(e), "error")
        return redirect(url_for('main.doctors'))
    find_dept = Department.query.all()
    return render_template(
        'doc_details.html', 
        title="detailPage",
        doctor=doc,
        educations=doc_edu,
        experiences=doc_ex,
        schedules=doc_sc,
        departments=find_dept
    )