from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, TimeField, StringField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, ValidationError


def not_default(form, field):
    if field.data == '':
        raise ValidationError('Selecione uma opção válida.')


class NewWorkoutForm(FlaskForm):
    @staticmethod
    def normalize_comma(value):
        if isinstance(value, str):
            return value.replace(',', '.')
        return value

    exercise_name = StringField('Nome do exercício', validators=[Length(max=50), DataRequired()])
    #TODO: Change to a SelectField

    # muscle_group = StringField('Grupo muscular alvo', validators=[Length(max=50), DataRequired()])
    muscle_group = SelectField('Grupo muscular alvo',
                                   validators=[DataRequired()],
                                   choices=[
                                       ('','-----Selecione-----'),
                                       ('Bíceps', 'Bíceps'),
                                       ('Tríceps', 'Tríceps'),
                                       ('Antebraço', 'Antebraço'),
                                       ('Peitoral', 'Peitoral'),
                                       ('Superior de costas', 'Superior de costas'),
                                       ('Dorsal', 'Dorsal'),
                                       ('Inferior de costas', 'Inferior de costas'),
                                       ('Deltóide frontal', 'Deltóide frontal'),
                                       ('Deltóide medial', 'Deltóide medial'),
                                       ('Deltóide posterior', 'Deltóide posterior'),
                                       ('Abdômen', 'Abdômen'),
                                       ('Oblíquos', 'Oblíquos'),
                                       ('Lombar', 'Lombar'),
                                       ('Quadríceps', 'Quadríceps'),
                                       ('Anterior de coxa', 'Anterior de coxa'),
                                       ('Posterior de coxa', 'Posterior de coxa'),
                                       ('Panturrilha', 'Panturrilha'),
                                       ('Glúteos', 'Glúteos'),
                                       ('Full body', 'Full body')
                                   ]
                               )
    instruction = TextAreaField('Intruções de execução', validators=[Optional(), Length(max=500)])


    min_sets = IntegerField('Quantidade mínima de séries', validators=[DataRequired(), NumberRange(min=1)])
    max_sets = IntegerField('Quantidade máxima de séries', validators=[Optional(), NumberRange(max=30)])
    set_duration = TimeField('Duração das séries (min:seg)', format='%M:%S', validators=[Optional()])
    set_interval = TimeField('Tempo de descanso (min:seg)', format='%M:%S', validators=[Optional()])
    min_reps = IntegerField('Repetições mínimas', validators=[DataRequired(), NumberRange(min=1, max=100)])
    max_reps = IntegerField('Repetições máximas', validators=[Optional(), NumberRange(max=100)])
    weight = DecimalField('Peso (kg)', places=1, filters=[normalize_comma],
    validators=[Optional(), NumberRange(max=500.0, message='O peso deve estar entre 0 e 500 kg.')])
