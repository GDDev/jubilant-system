from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .models import UserProfile
from .utils import db

# Flask
app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG_PATH')

# Flask-SQLAlchemy
db.init_app(app)
with app.app_context():
    db.create_all()

# Flask-Login
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(alt_id):
    return UserProfile()


from .views.views import *


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
