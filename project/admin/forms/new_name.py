from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from utils.validators import valid_name, valid_firstname


class NewNameForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), valid_firstname, Length(max=50)],
                       render_kw={'placeholder': 'Ex: João'})
    surname = StringField('Sobrenome', validators=[DataRequired(), valid_name, Length(max=100)],
                          render_kw={'placeholder': 'Ex: da Silva Santos'})
