from datetime import date
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField,  TimeField, PasswordField, FormField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Email,  Length, Optional, Regexp, ValidationError, NumberRange

class HospitalRegistrationForm(FlaskForm):
    """ hospital registration form"""
    name = StringField(
        'App Name',
        validators=[
            DataRequired(),
            Length(min=2, max=30, message="Please enter a valid name")
        ]
    )
    domain_name = StringField(
        'Domain Name',
        validators=[
            DataRequired(),
            Length(min=2, max=30, message="Please enter a valid name")
        ]
    )
    
    
    email1 = StringField('Email1', validators=[DataRequired(message='Enter a valid email'), Email(), Length(max=100)])
    email2 = StringField('Email2', validators=[Optional(), Email(), Length(max=100)])
    phone1 = StringField(
        'Phone Number1',
        validators=[
            DataRequired(message='Phone number is required'),
            Regexp(r'^[0-9]{11}$', message='Invalid phone number format. Use 11 digits only.')
        ]
    )
    phone2 = StringField(
        'Phone Number2',
        validators=[
            Optional(),
            Regexp(r'^[0-9]{11}$', message='Invalid phone number format. Use 11 digits only.')
        ]
    )
    location = StringField('Location', validators=[DataRequired(), Length(max=300)])
    favicon = FileField('Favicon', validators=[FileAllowed(['jpg', 'png'])])
    logo = FileField('Logo', validators=[FileAllowed(['jpg', 'png'])])
    facebook = StringField('Facebook', validators=[Optional(), Length(max=300)])
    instagram = StringField('Instagram', validators=[Optional(), Length(max=300)])
    twitter = StringField('Twitter', validators=[Optional(), Length(max=300)])
    youtube = StringField('Youtube', validators=[Optional(), Length(max=300)])
    linkedin = StringField('Linkedin', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Save')

class HospitalUpdateForm(FlaskForm):
    """ hospital Update form"""
    name = StringField(
        'App Name',
        validators=[
            Optional(),
            Length(min=2, max=30, message="Please enter a valid name")
        ]
    )
    domain_name = StringField(
        'Domain Name',
        validators=[
            Optional(),
            Length(min=2, max=30, message="Please enter a valid name")
        ]
    )
    
    
    email1 = StringField('Email1', validators=[Optional(), Email(), Length(max=100)])
    email2 = StringField('Email2', validators=[Optional(), Email(), Length(max=100)])
    phone1 = StringField(
        'Phone Number1',
        validators=[
            Optional(),
            Regexp(r'^[0-9]{11}$', message='Invalid phone number format. Use 11 digits only.')
        ]
    )
    phone2 = StringField(
        'Phone Number2',
        validators=[
            Optional(),
            Regexp(r'^[0-9]{11}$', message='Invalid phone number format. Use 11 digits only.')
        ]
    )
    location = StringField('Location', validators=[Optional(), Length(max=300)])
    favicon = FileField('Favicon', validators=[Optional(), FileAllowed(['jpg', 'png'])])
    logo = FileField('Logo', validators=[Optional(), FileAllowed(['jpg', 'png'])])
    facebook = StringField('Facebook', validators=[Optional(), Length(max=300)])
    instagram = StringField('Instagram', validators=[Optional(), Length(max=300)])
    twitter = StringField('Twitter', validators=[Optional(), Length(max=300)])
    youtube = StringField('Youtube', validators=[Optional(), Length(max=300)])
    linkedin = StringField('Linkedin', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Update')
