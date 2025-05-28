from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.fields.datetime import TimeField
from wtforms.fields.numeric import DecimalField
from wtforms.validators import DataRequired, length, Optional, NumberRange


class NewOptionForm(FlaskForm):
    @staticmethod
    def normalize_comma(value):
        if isinstance(value, str):
            return value.replace(',', '.')
        return value

    i_name = StringField('Apelido', validators=[DataRequired(message='Preencha este campo.'),
                                                  length(max=50, message='Limite de caracteres: 50')],
                       render_kw={'placeholder':'Ex: Opção 1'})
    i_description = StringField('Descrição', validators=[length(max=500)], render_kw={'placeholder':'Ex: Opção mais '
                                                                                                   'leve para dias pesados'})
    meal_time = TimeField('Horário da refeição (H:M)', format='%H:%M', validators=[DataRequired(message='Preencha este campo.')])

    f_name = StringField('Alimento', validators=[DataRequired(message='Preencha este campo.'),
                                                  length(max=50, message='Limite de caracteres: 50')],
                        render_kw={'placeholder':'Ex: Peito de frango'})
    quantity = IntegerField('Quantidade', validators=[Optional(), NumberRange(min=1)], render_kw={
        'placeholder':'Ex: 1'})
    weight = DecimalField('Peso (g)', places=2, filters=[normalize_comma], validators=[Optional(), NumberRange(
        min=1)], render_kw={'placeholder':'Ex: 250'})
    f_description = StringField('Observações', validators=[Optional(), length(max=500)],
                              render_kw={'placeholder':'Ex: Peito de frango pode ser cozido ou frito em Air Fryer'})
