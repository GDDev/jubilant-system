import requests
from flask import Flask, render_template
from flask_restful import Api
from api_quotes import NotFoundPageQuoteApi


app = Flask(__name__)
api = Api(app)


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


@app.errorhandler(404)
def get_404(e):
    response = requests.get('http://127.0.0.1:8000/api/generate_quote')
    quote = response.json()
    return render_template('404.html', quote=quote)


api.add_resource(NotFoundPageQuoteApi, '/api/generate_quote')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
