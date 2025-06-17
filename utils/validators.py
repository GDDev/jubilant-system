import re

from wtforms.validators import ValidationError

from .regex import re_name, re_f_name, re_username


def valid_firstname(form, field):
    if field.data:
        firstname = field.data.strip()
        if not re.match(re_f_name, firstname):
            raise ValidationError(f'O primeiro nome deve uma palavra e apenas letras.')
        if len(firstname) < 3:
            raise ValidationError(f'O primeiro nome deve ter no mínimo 3 letras.')


def valid_name(form, field):
    if field.data:
        name = field.data.strip()
        if not re.match(re_name, name):
            raise ValidationError(f'O sobrenome deve conter apenas letras.')
        if len(name) < 3:
            raise ValidationError(f'O sobrenome deve ter no mínimo 3 letras.')


def valid_username(form, field):
    if field.data:
        if not re.match(re_username, field.data.strip()):
            raise ValidationError(f'O nome de usuário pode conter letras, números e "_" apenas.')


def valid_access_creds(form, field):
    if field.data:
        if not re.match(re_username, field.data.strip()):
            raise ValidationError(f'Informações de acesso inválidas.')
