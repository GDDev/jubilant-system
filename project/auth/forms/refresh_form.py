from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

class RefreshForm(FlaskForm):
    pwd = PasswordField('Senha:', validators=[DataRequired()])

    submit = SubmitField('Entrar')