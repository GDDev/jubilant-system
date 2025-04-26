import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from core import db, migrate


def config_flask() -> Flask:
    flask = Flask(__name__)
    flask.config.from_pyfile('.settings.py', silent=True)
    return flask

def init_db(flask: Flask):
    db.init_app(flask)
    migrate.init_app(flask, db)

def register_all_bp(flask: Flask):
    from project.auth import auth
    from project.main import main
    from project.user import user, profile

    flask.register_blueprint(auth, url_prefix='/auth')
    flask.register_blueprint(main, url_prefix='/')
    flask.register_blueprint(user, url_prefix='/usuario')
    flask.register_blueprint(profile, url_prefix='/perfil')

def config_login_manager(flask: Flask):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.refresh_view = 'auth.refresh'
    login_manager.needs_refresh_message = 'Por favor, confirme sua senha para continuar.'
    login_manager.init_app(flask)

    @login_manager.user_loader
    def load_user(user_id):
        from project.user import UserProfile
        try:
            return db.session.query(UserProfile).filter_by(alt_id=user_id).first()
        except (ValueError, TypeError):
            return None

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.args.get('next') is None:
            return redirect(url_for('auth.signin'))
        return render_template('unauthorized.html'), 401

def create_app() -> Flask:
    flask = config_flask()

    init_db(flask)

    csrf = CSRFProtect(flask)
    with flask.app_context():
        register_all_bp(flask)
        config_login_manager(flask)

    return flask

def config_error_handlers(flask: Flask):
    @flask.errorhandler(404)
    def not_found(_):
        response = requests.get(
            'http://127.0.0.1:9090/not_found/generate_quote',
            timeout=1000
        )
        quote = response.json()
        return render_template('not_found.html', quote=quote)

    @flask.errorhandler(403)
    def forbidden(_):
        return render_template('forbidden.html'), 403

if __name__ == '__main__':
    app = create_app()
    config_error_handlers(app)
    app.run(host='127.0.0.1', port=8000, debug=True)
