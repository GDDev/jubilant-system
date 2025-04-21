from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user

from ..forms import SignUpForm
from ..services import AuthService
from app.auth import auth
from app.auth.exceptions import AuthException


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    @auth.route('/sign_up', methods=['GET', 'POST'])
    def sign_up(self):
        form = SignUpForm()
        if request.method == 'POST' and form.validate_on_submit():
            try:
                self.auth_service.validate_sign_up_data(form)

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

                profile = self.auth_service.sign_up_user(user_data, profile_data)

                if profile is not None:
                    login_user(profile)
                    # user_profile = UserProfile(1, 'defaulted', 'password')
                    # login_user(user_profile)

                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('home'))
            except AuthException as e:
                flash(e.message)

        return render_template('signup.html', form=form)

    @auth.route('/sing_in', methods=['POST'])
    def sing_in(self):
        pass

    @auth.route('/sign_out', methods=['GET'])
    def sign_out(self):
        pass
