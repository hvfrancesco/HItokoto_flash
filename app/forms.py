from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class submitStory(Form):
    autore = StringField('autore', validators=[DataRequired()])
    storia = TextAreaField('storia', validators=[DataRequired()])