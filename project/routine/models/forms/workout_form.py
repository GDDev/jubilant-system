from wtforms import Form, SelectField, StringField, IntegerField, DateTimeField, FloatField
from wtforms.validators import DataRequired


class RoutineForm(Form):
    name = StringField('Apelido', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])


class WorkoutForm(Form):
    min_sets = IntegerField('Mínimo de séries', validators=[DataRequired()])
    max_sets = IntegerField('Máximo de séries')
    set_duration = DateTimeField('Duração das séries')
    set_interval = DateTimeField('Tempo de descanso')
    min_reps = IntegerField('Repetições mínimas')
    max_reps = IntegerField('Repetições máximas')
    weight = FloatField('Peso')
