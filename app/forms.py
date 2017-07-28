from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class submitStory(FlaskForm):
    autore = StringField('autore', validators=[DataRequired()])
    storia = TextAreaField('storia', validators=[DataRequired()])