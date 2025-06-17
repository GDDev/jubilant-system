import logging
import traceback

from flask import session, flash
from flask_mailman import Mail, EmailMessage
from os import getenv

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

mail = Mail()
serializer = URLSafeTimedSerializer(getenv('FLASK_SECRET_KEY'))


def config_mail(flask):
    from dotenv import load_dotenv

    load_dotenv()

    flask.config['MAIL_SERVER'] = 'smtp.gmail.com'
    flask.config['MAIL_PORT'] = 587
    flask.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
    flask.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
    flask.config['MAIL_USE_TLS'] = True
    flask.config['MAIL_USE_SSL'] = False
    flask.config['MAIL_DEFAULT_SENDER'] = ('Jubilant System Team', getenv('MAIL_USERNAME'))
    mail.init_app(flask)


def send_mail(subject, body, to, html = None) -> None:
    try:
        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=getenv('MAIL_USERNAME'),
            to=[to],
        )
        if html:
            msg.content_subtype = "html"
            msg.body = html
        msg.send()
        logging.info(f'E-mail enviado para {to}.')
    except (BadSignature, Exception) as e:
        logging.error(f'Erro ao enviar e-mail para {to}: {str(e)}')
        logging.error(traceback.format_exc())


def generate_verification_token(email):
    return serializer.dumps(email, salt='jubilant_verification_token')


def verify_verification_token(token, expiration=3600):
    try:
        if not session.get(token):
            session[token] = True
            return serializer.loads(token, salt='jubilant_verification_token', max_age=expiration)
        logging.warning('Token já utilizado.')
    except SignatureExpired:
        logging.warning('Token de verificação expirado.')
    except BadSignature:
        logging.warning('Token de verificação inválido.')
    return False
