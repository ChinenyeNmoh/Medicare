from flask import render_template, flash, redirect, url_for, request
from app import db
from sqlalchemy import case
from app.models.department import Department
from flask_login import login_user, current_user, login_required
from app.models.doctor import  Doctor,WorkSchedule
from app.main.routes import main

@main.route('/doctors', methods=['GET', 'POST'], strict_slashes=False)
def doctors():
    find_doc = Doctor.query.filter_by(is_active=True).all()
    for i in find_doc:
        print(i)
    find_dept = Department.query.all()

    doc_sc = WorkSchedule.query.order_by(
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
        'doctors.html',
        title="doctorPage",
        doctors=find_doc,
        departments=find_dept,
        schedules=doc_sc
    )