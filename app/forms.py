# -*- coding: utf-8 -*- 

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class submitStory(FlaskForm):
    autore = StringField('autore', validators=[DataRequired(u'devi indicare il tuo nome')])
    titolo = StringField('titolo')
    storia = TextAreaField('storia', validators=[DataRequired(u'che storia corta! sei sicuro? era proprio vuota'), Length(max=9999, message=u'mi dispiace, questa storia è troppo lunga') ])