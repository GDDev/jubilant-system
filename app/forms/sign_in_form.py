from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SignInForm(FlaskForm):
    user = StringField('Nome de usuário ou Email:', validators=[DataRequired()])
    pwd = PasswordField('Senha:', validators=[DataRequired()])

    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')