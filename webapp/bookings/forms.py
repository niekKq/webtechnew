from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class BookingForm(FlaskForm):
    start_date = DateField("Startdatum", validators=[DataRequired()], format="%Y-%m-%d")
    end_date = DateField("Einddatum", validators=[DataRequired()], format="%Y-%m-%d")
    num_guests = IntegerField("Aantal gasten", validators=[DataRequired()])
    comments = TextAreaField("Opmerkingen")
    submit = SubmitField("Boeken")


class UpdateBookingForm(FlaskForm):
    start_date = DateField("Nieuwe startdatum", format="%Y-%m-%d")
    end_date = DateField("Nieuwe einddatum", format="%Y-%m-%d")
    num_guests = IntegerField("Nieuw aantal gasten")
    comments = TextAreaField("Nieuwe opmerkingen")
    submit = SubmitField("Bijwerken")
