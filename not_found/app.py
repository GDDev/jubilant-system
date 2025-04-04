from flask import Flask
from flask_restful import Api
from api_quotes import NotFoundPageQuoteApi

app = Flask(__name__)
api = Api(app)
api.add_resource(NotFoundPageQuoteApi, '/not_found/generate_quote')

if __name__ == '__main__':
    app.run(host='localhost', port=9090)
