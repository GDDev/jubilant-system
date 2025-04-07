import requests
from flask import render_template, request, url_for, redirect
from flask_login import LoginManager, login_required, login_user
from app.app import app
from app.models import User
from app.models import UserProfile
from app.services import us
# from models.profile import Profile

# TODO: probably turn this into blueprints


@app.route('/', methods=['GET',])
def home():
    return render_template('index.html')


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     from app.forms import SignUpForm
#     form = SignUpForm()
#
#     if form.validate_on_submit():
#         profile = us.create_user(
#             form.name.data,
#             form.surname.data,
#             form.email.data,
#             form.username.data,
#             form.pwd.data,
#             form.pwd2.data,
#             form.accept_terms.data
#             )
#         if profile is not None:
#             login_user(profile)
#         # user_profile = UserProfile(1, 'defaulted', 'password')
#         # login_user(user_profile)
#
#             next = request.args.get('next')
#             return redirect(next or url_for('home'))
#
#     return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    pass


@app.route('/diets', methods=['GET',])
def user_diets():
    return render_template('user_diets.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/workouts', methods=['GET',])
def user_workouts():
    return render_template('user_workouts.html')


@app.route('/chats', methods=['GET',])
def chats():
    return render_template('chats.html')


@app.route('/notifications', methods=['GET',])
def notifications():
    return render_template('notifications.html')


@app.errorhandler(404)
def not_found(_):
    response = requests.get(
        'http://127.0.0.1:9090/not_found/generate_quote',
        timeout=1000
    )
    quote = response.json()
    return render_template('404.html', quote=quote)
