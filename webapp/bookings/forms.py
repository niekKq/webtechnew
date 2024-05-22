from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, SelectField, SubmitField
from wtforms.validators import DataRequired


class BookingForm(FlaskForm):
    start_date = DateField("Startdatum", format="%Y-%m-%d", validators=[DataRequired()])
    end_date = DateField("Einddatum", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Boek")


class UpdateBookingForm(FlaskForm):
    new_start = DateField('Nieuwe tijdslot',format="%Y-%m-%d" , validators=[DataRequired()])
    new_end = DateField('Nieuwe einddatum',format="%Y-%m-%d" , validators=[DataRequired()])
    submit = SubmitField('Bijwerken')

class DeleteBookingForm(FlaskForm):
    # Verborgen veld om het boekings-ID door te geven
    booking_id = HiddenField()

    # Knop om de boeking te verwijderen
    submit = SubmitField("Verwijderen")