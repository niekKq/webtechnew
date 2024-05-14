from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class InfoForm(FlaskForm):
    naam = StringField("naam: ", validators=[DataRequired()])
    email = StringField(
        "email: ", validators=[DataRequired(), Email(message="email is niet geldig")]
    )
    wachtwoord = StringField("wachtwoord: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

