from flask import Flask
from flask_restful import Api
from api_quotes import NotFoundPageQuoteApi


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_prefixed_env()

api = Api(app)
api.add_resource(NotFoundPageQuoteApi, '/api/generate_quote')


from views import *


if __name__ == '__main__':
    app.run(host='127.0.0.1')
