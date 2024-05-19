from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired


class BungalowForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    bungalow_type = SelectField("Type", choices=[("Type1", "Type2")])
    weekprice = DecimalField("Week Price", validators=[DataRequired()])
    submit = SubmitField("Add Bungalow")
