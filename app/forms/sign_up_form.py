from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

from markupsafe import Markup

class SignUpForm(FlaskForm):
    name = StringField('Nome:', validators=[
        DataRequired('Preencha este campo.')
    ])
    surname = StringField('Sobrenome:', validators=[
        DataRequired('Preencha este campo.')
    ])
    email = EmailField('Email:', validators=[
        DataRequired('Preencha este campo.'),
        Email('Digite um email válido.')
    ])
    username = StringField('Nome de usuário:', validators=[
        DataRequired('Preencha este campo.')
    ])
    pwd = PasswordField('Senha:', validators=[
        DataRequired('Preencha este campo.'),
        EqualTo('pwd2', 'As senhas devem ser iguais')
    ])
    pwd2 = PasswordField('Confirmar senha:', validators=[
        DataRequired('Preencha este campo.'),
        EqualTo('pwd', '')
    ])

    accept_terms = BooleanField(
        Markup('Li e concordo com os <a href="#" target="_blank">Termos e Condições</a>'),
        validators=[InputRequired('Você deve concordar com os termos e condições para acessar o site.')]
    )
    
    submit = SubmitField('Cadastrar')