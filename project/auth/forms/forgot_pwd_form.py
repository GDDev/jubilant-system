from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired, Email


class ForgotPwdForm(FlaskForm):
    email = EmailField(
        'Email:',
        validators=[
            DataRequired(),
            Email(message='Por favor insira um e-mail válido.', check_deliverability=True)
        ],
        render_kw={"placeholder": "Insira o e-mail cadastrado"}
    )
    submit = SubmitField('Enviar nova senha', render_kw={'class': 'btn btn-outline-success text-white w-100'})
