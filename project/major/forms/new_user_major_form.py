import datetime
from dateutil.relativedelta import relativedelta

from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from ..models import MajorEnum


def start_date_validations(form, field):
    if field.data > datetime.date.today():
        raise ValidationError('A data de início não pode ser no futuro.')


def end_date_validations(form, field):
    start_date = form.start_date.data
    end_date = form.end_date.data
    if start_date and end_date and end_date < start_date:
        raise ValidationError('A data de conclusão não pode ser anterior ao início.')

    duration = relativedelta(end_date, start_date)
    total_months = duration.years * 12 + duration.months

    if total_months < 18:
        raise ValidationError('A duração deve ser de no mínimo 1 ano e meio.')
    if total_months > 120:
        raise ValidationError('A duração deve ser de no máximo 10 anos.')


class NewUserMajorForm(FlaskForm):
    college_code = StringField('Registro institucional', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Ex: 11223344566"})
    institutional_email = StringField('E-mail institucional', validators=[DataRequired(), Length(max=100)], render_kw={"placeholder": "Ex: 11223344566@aluno.uni.com"})
    user_is = SelectField('Selecione uma capacitação', choices=[(training.name, training.value.capitalize()) for training in MajorEnum])
    start_date = DateField('Data de ingresso', format='%Y-%m-%d', validators=[DataRequired(), start_date_validations])
    check_ongoing = BooleanField('Curso em andamento')
    end_date =  DateField('Data de conclusão', format='%Y-%m-%d', validators=[Optional(), end_date_validations])
    submit = SubmitField('Finalizar', render_kw={'class': 'btn btn-outline-success text-white'})
