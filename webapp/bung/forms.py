from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

class BungalowForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    bungalow_type = StringField('Type', validators=[DataRequired()])
    weekprice = StringField('Prijs per week', validators=[DataRequired()])
    submit = SubmitField('Opslaan')