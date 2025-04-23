from uuid import UUID

import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from core import db, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('.settings.cfg', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    csrf = CSRFProtect(app)

    with app.app_context():
        from project.auth import auth
        from project.main import main
        from project.user import user, profile
        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(main, url_prefix='/')
        app.register_blueprint(user, url_prefix='/usuario')
        app.register_blueprint(profile, url_prefix='/perfil')

        login_manager = LoginManager()
        login_manager.login_view = 'auth.signin'
        login_manager.init_app(app)

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

    return app

if __name__ == '__main__':
    app = create_app()

    @app.errorhandler(404)
    def not_found(_):
        response = requests.get(
            'http://127.0.0.1:9090/not_found/generate_quote',
            timeout=1000
        )
        quote = response.json()
        return render_template('not_found.html', quote=quote)

    @app.errorhandler(403)
    def forbidden(_):
        return render_template('forbidden.html'), 403


    app.run(host='127.0.0.1', port=8000, debug=True)

