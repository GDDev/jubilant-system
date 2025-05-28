from flask_mailman import Mail, EmailMessage
from os import getenv

mail = Mail()


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
