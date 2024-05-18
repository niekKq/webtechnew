from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BungalowForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()])
    bungalow_type = StringField("Type", validators=[DataRequired()])
    weekprice = StringField("Prijs per week", validators=[DataRequired()])
    submit = SubmitField("Opslaan")