from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user, confirm_login
from markupsafe import Markup
from werkzeug.security import check_password_hash

from ..forms import SignUpForm, SignInForm
from ..forms.refresh_form import RefreshForm
from ..services import AuthService
from project.auth import auth
from project.auth.exceptions import AuthException

auth_service = AuthService()

@auth.route('/cadastrar', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    form.accept_terms.label.text = Markup(f'Li e concordo com os <a href="{url_for("main.terms")}" target="_blank">Termos e '
                                'Condições</a>')

    if request.method == 'POST' and form.validate_on_submit():
        try:
            auth_service.validate_sign_up_data(form)

            user_data = {
                'name': form.name.data,
                'surname': form.surname.data,
                'email': form.email.data
            }
            profile_data = {
                'username': form.username.data,
                'password': form.pwd.data
            }

            profile = auth_service.sign_up_user(user_data, profile_data)

            if profile is not None:
                login_user(profile)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.home'))
        except AuthException as e:
            flash(str(e))

    return render_template('signup.html', form=form)

@auth.route('/entrar', methods=['GET', 'POST'])
def signin():
    form = SignInForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            profile = auth_service.sign_in_user(form.user.data, form.pwd.data)

            if profile is not None:
                login_user(profile, remember=form.remember_me.data)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.home'))
        except AuthException as e:
            flash(str(e))

    return render_template('signin.html', form=form)

@auth.route('/entrar_novamente', methods=['GET', 'POST'])
def refresh():
    form = RefreshForm()
    if form.validate_on_submit():
        try:
            if check_password_hash(current_user.pwd, form.pwd.data):
                confirm_login()
                next_page = request.form.get('next')
                return redirect(next_page or url_for('main.home'))
        except AuthException as e:
            flash(str(e))

    return render_template('refresh.html', form=form)

@auth.route('/sair', methods=['GET'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin'))


@auth.route('/esqueci_senha', methods=['GET', 'POST'])
def forgot_password():
    pass
