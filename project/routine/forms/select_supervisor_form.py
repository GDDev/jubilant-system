from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import Optional, DataRequired


class NewRoutineForm(FlaskForm):
    who_for = SelectField('Selecionar professor', validators=[DataRequired(message='Selecione um professor.')])
    submit = SubmitField('Salvar seleção')
