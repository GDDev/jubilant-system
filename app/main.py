from uuid import UUID

from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect

def create_app() -> Flask:
    from core import db, migrate
    app = Flask(__name__)
    app.config.from_pyfile('.settings.cfg', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    csrf = CSRFProtect(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    with app.app_context():
        from auth import auth
        app.register_blueprint(auth, url_prefix='/auth')

        @login_manager.user_loader
        def load_user(user_id):
            from user import UserProfile
            try:
                return db.session.query(UserProfile).filter_by(alt_id=UUID(user_id)).first()
            except (ValueError, TypeError):
                return None

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8000, debug=True)

