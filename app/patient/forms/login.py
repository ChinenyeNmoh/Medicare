#!/usr/bin/python3
"""forms module"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    """login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
            'Password', validators=[DataRequired(), Length(min=8, max=72)]
            )
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')