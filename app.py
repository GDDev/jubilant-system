import requests
from flask import Flask, render_template, jsonify, make_response
from not_found import choose_quote

app = Flask(__name__)


@app.route('/', methods=['GET',])
def get_index():
    return render_template('index.html')


@app.route('/diets', methods=['GET',])
def get_user_diets():
    return render_template('user_diets.html')


@app.route('/workouts', methods=['GET',])
def get_user_workouts():
    return render_template('user_workouts.html')


@app.route('/chats', methods=['GET',])
def get_chats():
    return render_template('chats.html')


@app.route('/notifications', methods=['GET',])
def get_notifications():
    return render_template('notifications.html')


@app.route('/generate_quote', methods=['GET',])
def get_quote():
    quote = choose_quote()
    response = make_response(jsonify(quote))
    response.set_cookie('used_quote', quote['quote'])
    return response


@app.errorhandler(404)
def get_404(e):
    response = requests.get('http://127.0.0.1:5000/generate_quote')
    quote = response.json()
    return render_template('404.html', quote=quote)
