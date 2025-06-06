from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Length

from ..models import Shift


class NewMajorForm(FlaskForm):
    # name = StringField('Nome do curso', validators=[DataRequired(message='Preencha este campo.'), Length(max=50)], render_kw={"disabled": True, "readonly": True, "placeholder":"Ex: Nutrição", "list": "major-options"})
    name = SelectField('Nome do curso', validators=[DataRequired(message='Selecione uma opção.')],
                       choices=[],
                       render_kw={'disabled': True, 'id': 'major-options'})
    # level = StringField('Nível da formação', validators=[DataRequired(message='Preencha este campo.'), Length(max=50)], render_kw={"disabled": True, "readonly": True, "placeholder":"Ex: Bacharelado", "list": "level-options"})
    level = SelectField('Grau da formação', validators=[DataRequired(message='Selecione uma opção.')],
                        choices=[],
                        render_kw={'disabled': True, 'id': 'level-options'})
    university = StringField('Universidade', validators=[DataRequired(message='Preencha este campo.'), Length(max=50)], render_kw={"placeholder": "Ex: Universidade de Mogi das Cruzes", "list": "university-options"})
    uni_acronym = StringField(
        'Sigla da Universidade',
        validators=[DataRequired(message='Preencha este campo.'), Length(max=5)],
        render_kw={"placeholder": "Ex: UMC", "disabled": True, "readonly": True}
    )
    area_tag = SelectField(
        'Área',
        coerce=str,
        validators=[DataRequired(message='Preencha este campo.')],
        render_kw={"disabled": True}
    )
    shift = SelectField(
        'Turno',
        choices=[(shift.name, shift.value.capitalize()) for shift in Shift],
        default=0,
        validators=[Optional()],
        render_kw={"disabled": True}
    )
    min_semesters = IntegerField(
        'Quantidade de semestres',
        validators=[Optional(),NumberRange(min=3, max=12, message='A quantidade de semestres deve estar entre 3 e 12')],
        render_kw = {"disabled": True, "readonly": True, "placeholder": "Ex: 8"}
    )
    max_semesters = IntegerField(
        'Quantidade máxima de semestres',
        validators=[Optional(), NumberRange(min=3, max=22, message='A quantidade máxima de semestres deve estar entre 3 e 22')],
        render_kw={"disabled": True, "readonly": True, "placeholder": "Ex: 12"}
    )
    submit = SubmitField('Salvar e continuar', render_kw={'class': 'btn btn-outline-success text-white'})
