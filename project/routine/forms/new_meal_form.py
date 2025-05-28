from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import length, Optional


class NewMealForm(FlaskForm):
    @staticmethod
    def normalize_comma(value):
        if isinstance(value, str):
            return value.replace(',', '.')
        return value

    total_calories = DecimalField('Calorias totais (Kcal)',
                                  places=2, filters=[normalize_comma],
                                  validators=[Optional()],
                                  render_kw={'placeholder': 'Ex: 5'})
    total_protein = DecimalField('Quantidade total de proteína (g)',
                                 places=2, filters=[normalize_comma],
                                 validators=[Optional()],
                                 render_kw={'placeholder': 'Ex: 10'})
    total_fat = DecimalField('Quantidade total de gordura (g)',
                             places=2, filters=[normalize_comma],
                             validators=[Optional()],
                             render_kw={'placeholder': 'Ex: 15'})
    total_carbs = DecimalField('Quantidade total de carboidratos (g)',
                               places=2, filters=[normalize_comma],
                               validators=[Optional()],
                               render_kw={'placeholder': 'Ex: 20'})
    goal = StringField('Objetivo', validators=[
        length(max=100, message='Seja sucinto, o limite de caracteres é 100.'),
        Optional()],
       render_kw={'placeholder': 'Ex: Hipertrofia e manutenção de massa magra.'})
    submit = SubmitField('Salvar e continuar', render_kw={'class': 'btn btn-outline-success text-white w-100'})
