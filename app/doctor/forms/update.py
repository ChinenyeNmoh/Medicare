from datetime import date
from flask_wtf import FlaskForm
import re
from flask_wtf.file import FileField, FileAllowed
from wtforms_components import DateRange
from wtforms import StringField, TextAreaField, SelectField, BooleanField,  TimeField,  SubmitField, DateField, IntegerField
from wtforms.validators import Email,  Length, Optional, Regexp, ValidationError, NumberRange

class DoctorUpdateForm(FlaskForm):
    """Update form"""
    first_name = StringField(
        'First Name',
        validators=[
            Optional(),
            Length(min=2, max=30, message="Please enter a valid name"),
            Regexp(
                r'^[A-Za-z\s\-\']+$',
                message='Invalid name format. Use letters, spaces, and hyphens only.'
            )
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            Optional(),
            Length(min=2, max=30, message="Please enter a valid name"),
            Regexp(
                r'^[A-Za-z\s\-\']+$',
                message='Invalid name format. Use letters, spaces, and hyphens only.'
            )
        ]
    )
    date_of_birth = DateField('Date of Birth', validators=[Optional(), DateRange(max=date.today())], format='%Y-%m-%d')
    gender = SelectField(
        'Gender',
        choices=[('male', 'Male'), ('female', 'Female')],
        validators=[Optional()]
    )
    department = SelectField(
        'Select Department',
        choices=[
            ('Oncology and Radiology', 'Oncology and Radiology'),
            ('Neurology', 'Neurology'),
            ('Respiratory Medicine', 'Respiratory Medicine'),
            ('Cardiology', 'Cardiology'),
            ('Ophthalmology', 'Ophthalmology'),
            ('Orthopedics', 'Orthopedics'),
        ],
        validators=[Optional()]
    )
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=100)])
    phone_number = StringField(
        'Phone Number',
        validators=[
            Optional(),
            Regexp(r'^[0-9]{11}$', message='Invalid phone number format. Use 11 digits only.')
        ]
    )
    is_active = BooleanField('Is Active', validators=[Optional()], default=True)
    contact_address = StringField('Contact Address', validators=[Optional(), Length(max=300)])
    consultation_fee = IntegerField('Consultation Fee', validators=[
        Optional(), 
        NumberRange(min=None, max=None)
    ])
    bio = TextAreaField('Bio', validators=[Optional()])
    picture = FileField('Profile Picture', validators=[Optional(), FileAllowed(['jpg', 'png'])])
    designation = StringField('Designation', validators=[Optional(), Length(max=300)])
    facebook = StringField('Facebook', validators=[Optional(), Length(max=300)])
    instagram = StringField('Instagram', validators=[Optional(), Length(max=300)])
    twitter = StringField('Twitter', validators=[Optional(), Length(max=300)])
    youtube = StringField('Youtube', validators=[Optional(), Length(max=300)])
    linkedin = StringField('Linkedin', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Update Personal Info')




class UpdateEducationForm(FlaskForm):
    def validate_date(self, field):
        if field.data:
            if not re.match(r'^\d{4}$', field.data):
                raise ValidationError('Invalid year format: must be a 4-digit number')

            year = int(field.data)
            current_year = date.today().year
            if year > current_year:
                raise ValidationError('Year cannot be in the future')

    date_started = StringField(
        'Start Date (Year)', 
        validators=[Optional(), 
                    Length(min=4, max=4), 
                    validate_date])
    
    date_ended = StringField(
        'End Date (Year)', 
        validators=[Optional(), 
                    Length(min=4, max=4), 
                    validate_date])
    school = StringField('School', validators=[Optional()])
    course_of_study = StringField('Course of Study', validators=[Optional()])
    certificate_type = SelectField('Certificate Type', choices=[
        ('Diploma', 'Diploma'),
        ('High school certificate', 'High School Certificate'),
        ('Degree', 'Degree'), 
        ('Masters', 'Masters'),
        ('Phd', 'PHD'),
        ('Professional certificate', 'Professional Certificate'),
        ('Other', 'Other')
        ], validators=[Optional()])




class UpdateWorkExperienceForm(FlaskForm):
    def validate_date(self, field):
        if field.data:
            if not re.match(r'^\d{4}$', field.data):
                raise ValidationError('Invalid year format: must be a 4-digit number')

            year = int(field.data)
            current_year = date.today().year
            if year > current_year:
                raise ValidationError('Year cannot be in the future')
    
    start_date = StringField(
        'Start Date (Year)', 
        validators=[Optional(), 
                    Length(min=4, max=4), 
                    validate_date])
    end_date = StringField(
        'End Date (Year)', 
        validators=[Optional(), 
                    Length(min=4, max=4), 
                    validate_date])
    company = StringField('Company', validators=[Optional()])
    position = StringField('Position', validators=[Optional()])



class UpdateWorkScheduleForm(FlaskForm):
    day_of_week = SelectField('Day of the Week', choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], validators=[Optional()])
    start_time = TimeField('Start Time', validators=[Optional()], format='%H:%M')
    end_time = TimeField('End Time', validators=[Optional()], format='%H:%M')
    schedule_submit = SubmitField('Save')



class AdminDoctorUpdateForm(FlaskForm):
    """Doctor Upgrade form"""
    first_name = StringField(
        'First Name',
        validators=[
            Optional(),
            Length(min=2, max=30, message="Please enter a valid name"),
            Regexp(
                r'^[A-Za-z\s\-\']+$',
                message='Invalid name format. Use letters, spaces, and hyphens only.'
            )
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            Optional(),
            Length(min=2, max=30, message="Please enter a valid name"),
            Regexp(
                r'^[A-Za-z\s\-\']+$',
                message='Invalid name format. Use letters, spaces, and hyphens only.'
            )
        ]
    )
    department = SelectField(
            'Select Department',
            choices=[('Oncology and Radiology', 'Oncology and Radiology'),
                      ('Neurology', 'Neurology'),
                      ('Respiratory Medicine', 'Respiratory Medicine'),
                      ('Cardiology', 'Cardiology'),
                      ('Ophthalmology', 'Ophthalmology'),
                      ('Orthopedics', 'Orthopedics'),
                      ],
            validators=[Optional()]
            )
    designation = StringField('Designation', validators=[Optional(), Length(max=300)])
    consultation_fee = IntegerField('Consultation Fee', validators=[
        Optional(), 
        NumberRange(min=None, max=None)
    ])
    is_banned = BooleanField('Is Banned', validators=[Optional()], default=False)
    is_active = BooleanField('Is Active', validators=[Optional()], default=True)
    submit = SubmitField('Update')
