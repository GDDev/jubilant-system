from flask import render_template

from .. import item_bp
from ..services import ItemService


item_service = ItemService()


@item_bp.route('/adicionar/<string:tipo>', methods=['GET'])
def add(tipo: str):
    pass
