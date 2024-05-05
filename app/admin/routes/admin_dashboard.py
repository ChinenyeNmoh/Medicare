from flask import  render_template, flash, redirect, url_for,request
from app.models.department import Department
from app import db
from datetime import datetime
from flask_login import current_user, login_required
from app.models.doctor import  Doctor
from app.models.patient import Patient, UserRole
from app.models.appointment import Appointment
from app.models.messages import Message

from app.admin.forms.departments import DepartmentForm, UpdateDepartmentForm

from app.admin.routes import admin

#admin dashboard
@admin.route('/adminDashboard', strict_slashes=False)
@login_required
def adminDashboard():
    findDept = Department.query.count()
    find_doc = Doctor.query.count()
    patient_count = Patient.query.count()
    admin_count = Patient.query.filter_by(role=UserRole.ADMIN).count()
    todays_date = datetime.now()
    string_date = todays_date.strftime(" %A,  %d %B, %Y ")
    todays_appointments = Appointment.query.filter_by(appointment_date=string_date).count()
    open_appointment = Appointment.query.filter(Appointment.appointment_status == 'Booked', Appointment.appointment_date != string_date).count()
    closed_appointment =  Appointment.query.filter(Appointment.appointment_status != "Booked").count()

    return render_template(
        'admin_default.html', 
        title= "Admin Dashboard",
        count=findDept,
        doc_count=find_doc,
        patient_count=patient_count,
        admin_count=admin_count,
        todays_appointments=todays_appointments,
        open_appointment=open_appointment,
        closed_appointment=closed_appointment
        )


#create department
@admin.route('/create_department', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def create_department():
    form=DepartmentForm()
    prev_page = request.referrer
    if form.validate_on_submit():
        try:
            findDept = Department.query.filter_by(title=form.title.data).first()
            if findDept:
                flash('Department Already Exist', 'danger')
                return redirect(prev_page)
            else:
                department = Department(
                    title=form.title.data,
                    image=form.image.data,
                    description=form.description.data
                    )
                
                # Add the new department to the database session
                db.session.add(department)
                db.session.commit()
                flash('New Department Created', 'success')
                return redirect(prev_page)
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('create_dept.html', title= "Create Department", form=form)


#admin dashboard
@admin.route('/view_department', strict_slashes=False)
@login_required
def view_department():
    form = UpdateDepartmentForm()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('entries', 6, type=int)
    print(per_page)
    search_query = request.args.get('search_query', '', type=str)
    print(search_query)
    # Query departments and apply search filter
    findDept = Department.query.order_by(Department.title)
    if search_query:
        findDept = findDept.filter(Department.title.contains(search_query))
       
    
    # Paginate the results
    findDept = findDept.paginate(page=page, per_page=per_page, error_out=False)
    total = findDept.total

    return render_template(
        'view_department.html', 
        title="View Department", 
        form=form, 
        departments=findDept,
        total=total,
        per_page=per_page,
        search_query=search_query
        )


#update department
@admin.route('/update_department/<id>', methods= ['GET', 'POST'], strict_slashes=False)
@login_required
def update_department(id):
    form = UpdateDepartmentForm()
    if form.validate_on_submit():
        try:
            update_dept = Department.query.filter_by(id=id).first()
            if update_dept:
                update_dept.title = form.title.data if form.title.data else update_dept.title
                update_dept.image = form.image.data if form.image.data else update_dept.image
                update_dept.description = form.description.data if form.description.data else update_dept.description
                db.session.commit()
                flash('Department updated', 'success')
                return redirect(url_for('admin.view_department'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('update_department.html', title= "Department", form=form)
    
#delete department
@admin.route('/delete_department/<id>', methods= ['GET'], strict_slashes=False)
@login_required
def delete_department(id):
        try:
            department = Department.query.filter_by(id=id).first()
            if department:
                db.session.delete(department)
                db.session.commit()
                flash('Department deleted', 'success')
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')
        return redirect(url_for('admin.view_department'))



#messages
@admin.route('/view_messages', strict_slashes=False)
@login_required
def view_messages():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    status = request.args.get('status', '', type=str)
    search_query = request.args.get('search_query', '', type=str)
    # Query departments and apply search filter
    if status:
        query = Message.query.filter_by(message_status = status).order_by(Message.created_at)
    else:
        query = Message.query.order_by(Message.created_at)
    if search_query:
        query = query.filter(Message.name.contains(search_query))
    # Paginate the results
    messages = query.paginate(page=page, per_page=per_page, error_out=False)
    total = messages.total

    return render_template(
        'view_messages.html', 
        title="View Messages", 
        messages=messages,
        total=total,
        per_page=per_page,
        search_query=search_query
        )


#update messages
@admin.route('/update_message/<id>', methods=['GET'], strict_slashes=False)
@login_required
def update_message(id):
    msg = Message.query.filter_by(id=id).first()
    if msg:
        msg.message_status='Resolved'
        db.session.commit()
        flash('Message Updated', 'success')
    else:
        flash('Message not found', 'danger')
    return redirect(url_for('admin.view_messages'))

#delete messages
@admin.route('/delete_message/<id>', methods=['GET'], strict_slashes=False)
@login_required
def delete_message(id):
    msg = Message.query.filter_by(id=id).first()
    if msg:
        db.session.delete(msg)
        db.session.commit()
        flash('Message deleted', 'success')
    else:
        flash('Message not found', 'danger')
    return redirect(url_for('admin.view_messages'))