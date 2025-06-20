from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

from utils import valid_firstname, valid_name, valid_username, valid_email


class SignUpForm(FlaskForm):
    name = StringField('Nome:', validators=[
        DataRequired('Preencha este campo.'),
        valid_firstname
    ], render_kw={"placeholder": "Insira seu nome"})
    surname = StringField('Sobrenome:', validators=[
        DataRequired('Preencha este campo.'),
        valid_name
    ], render_kw={"placeholder": "Insira seu sobrenome"})
    email = EmailField('Email:', validators=[
        DataRequired('Preencha este campo.'),
        Email('Digite um email válido.', check_deliverability=True),
        valid_email
    ], render_kw={"placeholder": "Insira seu e-mail"})
    username = StringField('Nome de usuário:', validators=[
        DataRequired('Preencha este campo.'),
        valid_username
    ], render_kw={"placeholder": "Insira um nome de usuário"})
    pwd = PasswordField('Senha:', validators=[
        DataRequired('Preencha este campo.'),
        EqualTo('pwd2', 'As senhas devem ser iguais')
    ], render_kw={"placeholder": "Insira uma senha"})
    pwd2 = PasswordField('Confirmar senha:', validators=[
        DataRequired('Preencha este campo.'),
        EqualTo('pwd', '')
    ], render_kw={"placeholder": "Confirme sua senha"})

    accept_terms = BooleanField(
        validators=[InputRequired('Você deve aceitar os termos e condições para continuar.')],
        render_kw={"class": "form-check-input", "style": "cursor: pointer;"}
    )
    
    submit = SubmitField('Cadastrar')