import requests
from flask import render_template
from app import app

# TODO: probably turn this into blueprints


@app.route('/', methods=['GET',])
def home():
    return render_template('index.html')


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
        'http://127.0.0.1:5000/api/generate_quote',
        timeout=1000
    )
    quote = response.json()
    return render_template('404.html', quote=quote)
