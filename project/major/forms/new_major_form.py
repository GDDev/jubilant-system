from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Length

from ..models import AreaTags, Shift


class NewMajorForm(FlaskForm):
    name = StringField('Nome do curso', validators=[DataRequired(), Length(max=50)], render_kw={"disabled": True, "readonly": True, "placeholder":"Ex: Nutrição", "list": "major-options"})
    level = StringField('Nível da formação', validators=[DataRequired(), Length(max=50)], render_kw={"disabled": True, "readonly": True, "placeholder":"Ex: Bacharelado", "list": "level-options"})
    university = StringField('Universidade', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Ex: Universidade de Mogi das Cruzes", "list": "university-options"})
    uni_acronym = StringField(
        'Sigla da Universidade',
        validators=[Optional(), Length(max=5)],
        render_kw={"placeholder": "Ex: UMC", "disabled": True, "readonly": True}
    )
    area_tag = SelectField(
        'Área',
        choices=[(area.name, area.value.capitalize()) for area in AreaTags],
        default=0,
        validators=[DataRequired()],
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
