from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.datetime import TimeField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, length, Optional, NumberRange


class NewOptionForm(FlaskForm):
    ref_time = TimeField(
        'Horário da refeição (H:M)',
        format='%H:%M',
        validators=[DataRequired(message='Preencha este campo.')]
    )
    goal = StringField('Objetivo', validators=[Optional(), length(max=100, message='Limite de 100 caracteres.')],
                       render_kw={
                           'placeholder': 'Ex: Refeição pré treino para garantir a performance.'})
    total_calories = DecimalField(
        'Calorias totais (kcal)',
        validators=[Optional(), NumberRange(min=0, max=20000, message='Kcal devem estar entre 0 e 20.000.')],
        render_kw={'placeholder': 'Ex: 10'}
    )
    total_protein = DecimalField(
        'Quantidade total de proteínas (g)',
        validators=[Optional(), NumberRange(min=0, max=300, message='Gramas de proteína devem estar entre 0 e 300.')],
        render_kw={'placeholder': 'Ex: 10'}
    )
    total_fat = DecimalField(
        'Quantidade total de gorduras (g)',
        validators=[Optional(), NumberRange(min=0, max=350, message='Gorduras totais devem estar entre 0 e 350.')],
        render_kw={'placeholder': 'Ex: 10'}
    )
    total_carbs = DecimalField(
        'Quantidade total de carboidratos (g)',
        validators=[Optional(), NumberRange(min=0, max=1200, message='Carboidratos totais devem estar entre 0 e 1.200.')],
        render_kw={'placeholder': 'Ex: 10'}
    )

    submit = SubmitField(
        'Salvar e continuar',
        render_kw={'class': 'btn btn-outline-success text-white w-100'}
    )

