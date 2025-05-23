import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from core import db, migrate
from project.routine import item_bp


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
    from project.friendship import friendship
    from project.notification import notification
    from project.academia import Major, UserMajor
    from project.post import post_bp, comment_bp
    from project.routine import routine_bp, item_bp

    flask.register_blueprint(auth, url_prefix='/auth')
    flask.register_blueprint(main, url_prefix='/')
    flask.register_blueprint(user, url_prefix='/usuario')
    flask.register_blueprint(profile, url_prefix='/perfil')
    flask.register_blueprint(friendship, url_prefix='/amigo')
    flask.register_blueprint(notification, url_prefix='/notificacao')
    flask.register_blueprint(post_bp, url_prefix='/postagem')
    flask.register_blueprint(comment_bp, url_prefix='/comentario')
    flask.register_blueprint(routine_bp, url_prefix='/rotina')
    flask.register_blueprint(item_bp, url_prefix='/item')

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
        register_filters(flask)
        config_login_manager(flask)

    return flask

def config_error_handlers(flask: Flask):
    @flask.errorhandler(404)
    def not_found(_):
        from not_found import NotFoundPageQuoteApi

        quote = NotFoundPageQuoteApi().get().json
        return render_template('not_found.html', quote=quote)

    @flask.errorhandler(403)
    def forbidden(_):
        return render_template('forbidden.html'), 403

    @flask.errorhandler(500)
    def internal_server_error(e):
        return render_template('internal_server_error.html', error=str(e)), 500

def register_filters(flask: Flask):
    import emoji
    @flask.template_filter('emojify')
    def emoji_filter(s):
        return emoji.emojize(s)