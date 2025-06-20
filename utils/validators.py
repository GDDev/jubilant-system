import re

from wtforms.validators import ValidationError

from .regex import re_name, re_f_name, re_username, re_text


def validate_post(title: str | None, content: str) -> None:
    from project.post import PostException
    from .regex import re_text
    if title:
        if not re.match(re_text, title):
            raise PostException('Caracteres não permitidos encontrados no título da postagem.')
        if len(title) > 50:
            raise PostException('O título não pode ter mais de 50 caracteres.')
    if not content or content.strip() == '':
        raise PostException('O conteúdo da postagem não pode ser vazia.')
    if not re.match(re_text, content):
        raise PostException('Caracteres não permitidos encontrados no conteúdo da postagem.')
    if len(content) > 500:
        raise PostException('O conteúdo não pode ter mais de 500 caracteres.')


def validate_comment(comment: str) -> None:
    from project.post import CommentException

    if not comment or comment.strip() == '':
        raise CommentException('Comentário não pode ser vazio.')
    if not re.match(re_text, comment):
        raise CommentException('Caracteres não permitidos encontrados no seu comentário.')
    if len(comment) > 200:
        raise CommentException('O comentário não pode ter mais de 200 caracteres.')



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
