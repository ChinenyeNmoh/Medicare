from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

class UpdateAppointmentForm(FlaskForm):
    appointment_comment = TextAreaField('Doctor\'s Comment', validators=[
        Optional()
    ])
    appointment_status = SelectField('Appointment Status', choices=[
        ('', 'Select status'),
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
        ('Patient Absent', 'Patient Absent')
    ],
    validators=[Optional()]
    )
    payment_status = SelectField('Payment Status', choices=[
        ('', 'Select status'),
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    ],
    validators=[Optional()]
    )
    submit = SubmitField('Update')
