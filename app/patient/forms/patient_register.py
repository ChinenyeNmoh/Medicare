#!/usr/bin/python3
"""registration forms module"""

from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError, NumberRange


class RegistrationForm(FlaskForm):
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
    age = IntegerField('Age', validators=[
        DataRequired(message='Enter Valid Age'), 
        NumberRange(min=None, max=None)
    ])
    email = StringField('Email', validators=[DataRequired(message='Enter a valid email'), Email(), Length(max=100)])
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(message='Phone number is required'),
            Regexp(r'^[0-9]{11}$', message='Invalid phone number format. Use 11 digits only.')
        ]
    )
    contact_address = StringField('Contact Address', validators=[DataRequired(), Length(max=300)])
    password = PasswordField('Password', validators=[DataRequired(), Length(
        min=8, message='password field should be at least 8 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message="Passwords do not match")])
    submit = SubmitField('Sign Up')


