from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user
from markupsafe import Markup

from ..forms import SignUpForm, SignInForm
from ..services import AuthService
from project.auth import auth
from project.auth.exceptions import AuthException

auth_service = AuthService()

@auth.route('/signup', methods=['GET', 'POST'])
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
                'role': form.role.data,
                'username': form.username.data,
                'password': form.pwd.data
            }

            profile = auth_service.sign_up_user(user_data, profile_data)

            print(profile)

            if profile is not None:
                login_user(profile)
                # user_profile = UserProfile(1, 'defaulted', 'password')
                # login_user(user_profile)

                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.home'))
        except AuthException as e:
            flash(str(e))

    return render_template('signup.html', form=form)

@auth.route('/singin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    return render_template('signin.html', form=form)

@auth.route('/signout', methods=['GET'])
def signout():
    pass
