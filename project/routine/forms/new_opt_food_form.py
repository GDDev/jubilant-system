from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, length, Optional, NumberRange


class NewOptFoodForm(FlaskForm):
    @staticmethod
    def normalize_comma(value):
        if isinstance(value, str):
            return value.replace(',', '.')
        return value

    name = StringField(
        'Alimento',
        validators=[
            DataRequired(message='Preencha este campo.'),
            length(max=50, message='Limite de caracteres: 50')
        ],
        render_kw={'placeholder': 'Ex: Peito de frango'}
    )
    quantity = IntegerField(
        'Quantidade',
        validators=[
            Optional(),
            NumberRange(min=1, max=50, message='A quantidade possui o gentil limite de 1 à 50.')
        ],
        render_kw={'placeholder': '(Opcional) Ex: 1'}
    )
    weight = DecimalField(
        'Peso (g)',
        places=2,
        filters=[normalize_comma],
        validators=[
            Optional(),
            NumberRange(min=1, max=5000, message='O peso possui o gentil limite de 1 à 5000 (5kg).')
        ],
        render_kw={'placeholder': '(Opcional) Ex: 250'}
    )
    description = StringField(
        'Observações',
        validators=[
            Optional(),
            length(max=500, message='Limite de caracteres: 500')
        ],
        render_kw={'placeholder': 'Ex: Peito de frango pode ser cozido ou frito em Air Fryer'}
    )
    submit = SubmitField(
        'Salvar',
        render_kw={'class': 'btn btn-outline-success text-white w-100'}
    )
