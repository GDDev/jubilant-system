from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import StringField, BooleanField
from wtforms.validators import DataRequired, Length, Optional


class NewUserMajorForm(FlaskForm):
    college_code = StringField('Registro institucional', validators=[DataRequired(), Length(max=50)])
    institutional_email = StringField('E-mail institucional', validators=[DataRequired(), Length(max=60)])
    start_date = DateField('Data de ingresso', format='%m/%Y', validators=[DataRequired()])
    check_ongoing = BooleanField('Curso em andamento')
    end_date =  DateField('Data de conclusão', format='%m/%Y', validators=[Optional()])
