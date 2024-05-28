from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from email_validator import validate_email, EmailNotValidError
from flask_wtf import RecaptchaField


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    recaptcha = RecaptchaField()  
    submit = SubmitField("Sign Up")

    def validate_email_address(self, field):
        try:
            validate_email(field.data)
        except EmailNotValidError:
            raise ValidationError("Dit is geen geldig e-mailadres.")


class LoginForm(FlaskForm):
    naam = StringField("naam: ", validators=[DataRequired()])
    wachtwoord = PasswordField("wachtwoord: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class InfoForm(FlaskForm):
    naam = StringField("naam: ", validators=[DataRequired()])
    email = StringField(
        "email: ", validators=[DataRequired(), Email(message="email is niet geldig")]
    )
    wachtwoord = PasswordField("wachtwoord: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AccountForm(FlaskForm):
    username = StringField("Nieuwe gebruikersnaam")
    email = StringField("Nieuw e-mailadres", validators=[Email()])
    password = PasswordField(
        "Nieuw wachtwoord",
        validators=[
            EqualTo("confirm_password", message="Wachtwoorden moeten overeenkomen")
        ],
    )
    confirm_password = PasswordField("Bevestig nieuw wachtwoord")
    submit = SubmitField("Opslaan")



