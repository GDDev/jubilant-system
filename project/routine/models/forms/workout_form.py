from wtforms import Form, SelectField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class RoutineForm(Form):
    name = StringField('Apelido', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])


class WorkoutForm(Form):
    min_sets = IntegerField('Mínimo de séries', validators=[DataRequired()])
    max_sets = IntegerField('Máximo de séries')
    set_duration = DateTimeField('Duração das séries')
    set_interval = DateTimeField
