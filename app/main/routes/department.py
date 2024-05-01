from flask import  render_template, flash, redirect, url_for,request
from app.models.department import Department
from app import db
from flask_login import login_user, current_user, login_required
from app.main.routes import main

@main.route('/department', strict_slashes=False)
def department():
    findDept = Department.query.filter_by().all()
    return render_template('department.html', title= "departmentPage", departments=findDept)