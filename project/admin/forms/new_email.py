from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email

from utils import valid_email


class NewEmailForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Por favor insira um email válido.'),
        valid_email
    ])
