from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from utils import valid_access_creds


class SignInForm(FlaskForm):
    user = StringField('Nome de usuário ou Email:', validators=[
        DataRequired(message='Preencha este campo.'),
        valid_access_creds
    ],
                       render_kw={"placeholder": "Insira seu nome de usuário",
                                  "style": "min-width: fit-content;"})
    pwd = PasswordField('Senha:', validators=[DataRequired(message='Preencha este campo.')],
                        render_kw={"placeholder": "Insira sua senha",
                                  "style": "min-width: fit-content;"})

    remember_me = BooleanField('Lembrar de mim', render_kw={"style": "cursor: pointer;"})
    submit = SubmitField('Entrar')