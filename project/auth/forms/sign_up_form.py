from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired


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
    role = SelectField('Você é:', choices=[
        ('student', 'Estudante'), ('professor', 'Professor')
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
        validators=[InputRequired('Você deve aceitar os termos e condições para continuar.')]
    )
    
    submit = SubmitField('Cadastrar')