from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired


class BookingForm(FlaskForm):
    start_date = DateField("Startdatum", format="%Y-%m-%d", validators=[DataRequired()])
    end_date = DateField("Einddatum", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Boek")


class UpdateBookingForm(FlaskForm):
    new_timeslot = SelectField(
        "Nieuw tijdslot", choices=[], validators=[DataRequired()]
    )
    submit = SubmitField("Bijwerken")
