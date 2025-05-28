from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


from ..models import MajorEnum


class NewUserMajorForm(FlaskForm):
    college_code = StringField('Registro institucional', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Ex: 11223344566"})
    institutional_email = StringField('E-mail institucional', validators=[DataRequired(), Length(max=100)], render_kw={"placeholder": "Ex: 11223344566@aluno.uni.com"})
    user_is = SelectField('Selecione uma capacitação', choices=[(training.name, training.value.capitalize()) for training in MajorEnum])
    start_date = DateField('Data de ingresso', format='%Y-%m-%d', validators=[DataRequired()])
    check_ongoing = BooleanField('Curso em andamento')
    end_date =  DateField('Data de conclusão', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Finalizar', render_kw={'class': 'btn btn-outline-success text-white'})
