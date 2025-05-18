from wtforms import IntegerField, DecimalField, TimeField
from wtforms.validators import DataRequired, NumberRange

from .new_item_form import NewItemForm


class NewWorkoutForm(NewItemForm):
    @staticmethod
    def normalize_comma(value):
        if isinstance(value, str):
            return value.replace(',', '.')
        return value

    min_sets = IntegerField('Quantidade mínima de séries', validators=[DataRequired(), NumberRange(min=1)])
    max_sets = IntegerField('Quantidade máxima de séries', validators=[NumberRange(min=1, max=30)])
    set_duration = TimeField('Duração das séries', format='%M:%S')
    set_interval = TimeField('Tempo de descanso', format='%M:%S')
    min_reps = IntegerField('Repetições mínimas', validators=[DataRequired(), NumberRange(min=1, max=100)])
    max_reps = IntegerField('Repetições máximas', validators=[NumberRange(min=1, max=100)])
    weight = DecimalField('Peso (kg)', places=1, filters=[normalize_comma], validators=[NumberRange(min=0.0, max=500.0, message='O peso deve estar entre 0 e 500 kg.')])
