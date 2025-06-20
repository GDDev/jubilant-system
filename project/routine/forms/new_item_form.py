import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from utils import valid_name
from utils.validators import valid_text


def not_a_past_date(form, field):
    if field.data <= datetime.date.today():
        raise ValidationError('A data não pode ser no passado.')


class NewItemForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(max=50), valid_name])
    expiration_date = DateField('Expirar em', format='%Y-%m-%d', validators=[Optional(), not_a_past_date])
    source = TextAreaField('Referências',
                           validators=[Length(max=500, message='Limite de 500 caracteres'), valid_text])
    submit = SubmitField('Salvar e continuar', render_kw={'class': 'btn btn-outline-success'})
