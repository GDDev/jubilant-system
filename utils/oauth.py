from os import getenv
from authlib.integrations.flask_client import OAuth


oauth = OAuth()


def config_oauth(flask):
    from dotenv import load_dotenv
    load_dotenv()

    oauth.init_app(flask)
    oauth.register(
        name='google',
        client_id=getenv('GOOGLE_CLIENT_ID'),
        client_secret=getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
