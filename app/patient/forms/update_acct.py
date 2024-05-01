#!/usr/bin/python3
"""registration forms module"""

from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, IntegerField
from wtforms.validators import Length, Regexp, ValidationError, NumberRange, Optional, Email


class UpdateForm(FlaskForm):
    """Update form"""
    first_name = StringField(
        'First Name',

    )
    last_name = StringField(
        'Last Name',
        
    )
    
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=100)])
    gender = SelectField(
            'Gender',
            validators=[Optional()],
            choices=[('male', 'Male'), ('female', 'Female')]
            )
    age = IntegerField('Age', validators=[Optional()]
    )
    phone_number = StringField(
        'Phone Number', validators=[Optional()]
    )
    contact_address = StringField('Contact Address', validators=[Optional()],)
    submit = SubmitField('Update Account')


