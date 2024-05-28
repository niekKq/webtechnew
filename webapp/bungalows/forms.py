from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired


class BungalowForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    bungalow_type = SelectField(
        "Type",
        choices=[("4 persoons", "4 persoons"), ("6 persoons", "6 persoons"), ("8 persoons", "8 persoons")],
        validators=[DataRequired()],
    )
    weekprice = DecimalField("Week Price", validators=[DataRequired()])
    submit = SubmitField("Add Bungalow")
