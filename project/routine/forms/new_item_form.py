from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Optional


class NewItemForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    expiration_date = DateField('Expirar em', format='%Y-%m-%d', validators=[Optional()])
    description = TextAreaField('Descrição/Observação', validators=[Length(max=500)])
    submit = SubmitField('Salvar e continuar', render_kw={'class': 'btn btn-outline-success'})
