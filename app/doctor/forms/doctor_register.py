from datetime import date
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField,  TimeField, PasswordField, FormField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Email,  Length, Optional, Regexp, ValidationError, NumberRange


class EducationForm(FlaskForm):
    def validate_date(self, field):
        if field.data and int(field.data) > date.today().year:
            raise ValidationError('Year cannot be in the future')

    date_started = StringField('Start Date (Year)', validators=[DataRequired(), Length(min=4, max=4), validate_date])
    date_ended = StringField('End Date (Year)', validators=[DataRequired(message="Enter Valid year"), Length(min=4, max=4), validate_date])
    school = StringField('School', validators=[DataRequired()])
    course_of_study = StringField('Course of Study', validators=[DataRequired()])
    certificate_type = SelectField('Certificate Type', choices=[
        ('Diploma', 'Diploma'),
        ('High school certificate', 'High School Certificate'),
        ('Degree', 'Degree'), 
        ('Masters', 'Masters'),
        ('Phd', 'PHD'),
        ('Professional certificate', 'Professional Certificate'),
        ('Other', 'Other')
        ], validators=[DataRequired()])
    education_submit = SubmitField('Save Education')


class WorkExperienceForm(FlaskForm):
    def validate_date(self, field):
        print('date validator')
        if field.data:
            print(field.data)
            if not field.data.isdigit():
                raise ValidationError('Invalid year format: must be a number')
            year = int(field.data)
            current_year = date.today().year
            if year > current_year:
                raise ValidationError('Year cannot be in the future')
    
    start_date = StringField('Start Date (Year)', validators=[DataRequired(), Length(min=4, max=4),  validate_date])
    end_date = StringField('End Date (Year)', validators=[DataRequired(message="Enter Valid year"), Length(min=4, max=4),  validate_date])
    company = StringField('Company', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    experience_submit = SubmitField('Save Experience')


class WorkScheduleForm(FlaskForm):
    day_of_week = SelectField('Day of the Week', choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()], format='%H:%M')
    end_time = TimeField('End Time', validators=[DataRequired()], format='%H:%M')
    schedule_submit = SubmitField('Save')
   

class DoctorRegistrationForm(FlaskForm):
    """registration form"""
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
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
            DataRequired(),
            Length(min=2, max=30, message="Please enter a valid name"),
            Regexp(
                r'^[A-Za-z\s\-\']+$',
                message='Invalid name format. Use letters, spaces, and hyphens only.'
            )
        ]
    )
    def validate_date_of_birth(self, field):
        if field.data and field.data > date.today():
            raise ValidationError('Date of birth cannot be in the future')
    
    date_of_birth = DateField('Date of Birth', validators=[DataRequired(), validate_date_of_birth], format='%Y-%m-%d')
    gender = SelectField(
            'Gender',
            choices=[('male', 'Male'), ('female', 'Female')],
            validators=[DataRequired(message='Select gender')]
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
            validators=[DataRequired(message='Select Department')]
            )
    age = IntegerField('Age', validators=[
        DataRequired(message='Enter Valid Age from 17 to 90'), 
        NumberRange(min=17, max=90)
    ])
    email = StringField('Email', validators=[DataRequired(message='Enter a valid email'), Email(), Length(max=100)])
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(message='Phone number is required'),
            Regexp(r'^[0-9]{11}$', message='Invalid phone number format. Use 11 digits only.')
        ]
    )
    consultation_fee = IntegerField('Consultation Fee', validators=[
        DataRequired(message='Enter Valid Amount'), 
        NumberRange(min=None, max=None)
    ])
    is_banned = BooleanField('Is Banned', validators=[Optional()], default=False)
    is_active = BooleanField('Is Active', validators=[Optional()], default=True)
    contact_address = StringField('Contact Address', validators=[DataRequired(), Length(max=300)])
    bio = TextAreaField(
            'Bio', validators=[DataRequired()]
            )
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    designation = StringField('Designation', validators=[DataRequired(), Length(max=300)])
    facebook = StringField('Facebook', validators=[Optional(), Length(max=300)])
    instagram = StringField('Instagram', validators=[Optional(), Length(max=300)])
    twitter = StringField('Twitter', validators=[Optional(), Length(max=300)])
    youtube = StringField('Youtube', validators=[Optional(), Length(max=300)])
    linkedin = StringField('Linkedin', validators=[Optional(), Length(max=300)])
    password = PasswordField('Password', validators=[DataRequired(), Length(
        min=8, message='password field should be at least 8 characters')])
    submit = SubmitField('Save Personal Info')
