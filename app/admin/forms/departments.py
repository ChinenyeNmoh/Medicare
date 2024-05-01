#!/usr/bin/python3
"""forms module"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, optional


class DepartmentForm(FlaskForm):
    """department form"""
    title = StringField('Title', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    description = TextAreaField(
            'Description', validators=[DataRequired()]
            )
    submit = SubmitField('Create Department')

class UpdateDepartmentForm(FlaskForm):
    """Update department form"""
    title = StringField('Title', validators=[optional()])
    image = StringField('Image', validators=[optional()])
    description = TextAreaField(
            'Description', validators=[optional()]
            )
    submit = SubmitField('Update Department')