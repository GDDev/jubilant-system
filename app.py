import requests
from flask import Flask, render_template, jsonify
from not_found import choose_quote

app = Flask(__name__)


@app.route('/', methods=['GET',])
def get_index():
    return render_template('index.html')


@app.route('/generate_quote', methods=['GET',])
def get_quote():
    return jsonify(choose_quote())


@app.errorhandler(404)
def get_404(e):
    response = requests.get('http://127.0.0.1:5000/generate_quote')
    quote = response.json()
    return render_template('404.html', quote=quote)
