from flask import Flask, render_template  # type: ignore

app = Flask(__name__)


@app.route('/', methods=['GET',])
def get_index():
    return render_template('index.html')


@app.errorhandler(404)
def get_404(e):
    return render_template('404.html')
