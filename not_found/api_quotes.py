from flask import jsonify, make_response
from flask_restful import Resource

from not_found import choose_quote


class NotFoundPageQuoteApi(Resource):
    def get(self):
        quote = choose_quote()
        response = make_response(jsonify(quote))
        response.set_cookie(
            'last_quote',
            quote['quote'],
        )
        return response
