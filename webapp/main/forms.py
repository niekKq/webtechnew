from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class InfoForm(FlaskForm):
    naam = StringField("naam: ", validators=[DataRequired()])
    email = StringField(
        "email: ", validators=[DataRequired(), Email(message="email is niet geldig")]
    )
    wachtwoord = StringField("wachtwoord: ", validators=[DataRequired()])
    submit = SubmitField("Submit")
