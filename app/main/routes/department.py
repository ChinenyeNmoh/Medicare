from flask import  render_template, flash, redirect, url_for,request
from app.models.department import Department
from app import db
from flask_login import login_user, current_user, login_required
from app.main.routes import main
from app.models.messages import Message

@main.route('/department', strict_slashes=False)
def department():
    findDept = Department.query.filter_by().all()
    return render_template('department.html', title= "departmentPage", departments=findDept)


#view messages
@main.route('/create_message', methods= ['GET', 'POST'], strict_slashes=False)
def create_message():
    prev_page = request.referrer
    try:
        new_msg = Message(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone_number=request.form.get('phone_number'),
            comment=request.form.get('comment'),
        )
        db.session.add(new_msg)
        db.session.commit()
        flash('Message submitted successfully', 'success')
        return redirect(prev_page) if prev_page else redirect(url_for('main.home'))
    except Exception as e:
        db.session.rollback()
        flash(str(e), 'danger')
        return redirect(prev_page) if prev_page else redirect(url_for('main.home'))