from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, SelectField, IntegerField
from wtforms.validators import DataRequired, Optional


class NewRoutineForm(FlaskForm):
    routine_id = IntegerField('Routine ID', validators=[Optional()])
    who_for = SelectField('Selecionar amigo', validators=[DataRequired(message='Selecione um amigo.')])
    submit = SubmitField('Salvar seleção')
