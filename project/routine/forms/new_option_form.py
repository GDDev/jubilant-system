from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.datetime import TimeField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, length


class NewOptionForm(FlaskForm):
    name = StringField(
        'Apelido',
        validators=[
            DataRequired(message='Preencha este campo.'),
            length(max=50, message='Limite de caracteres: 50')
        ],
        render_kw={'placeholder':'Ex: Opção 1'})
    description = StringField(
        'Descrição',
        validators=[length(max=500)],
        render_kw={'placeholder':'Ex: Opção mais leve para dias pesados'}
    )
    meal_time = TimeField(
        'Horário da refeição (H:M)',
        format='%H:%M',
        validators=[DataRequired(message='Preencha este campo.')]
    )
    submit = SubmitField(
        'Salvar e continuar',
        render_kw={'class': 'btn btn-outline-success text-white w-100'}
    )

