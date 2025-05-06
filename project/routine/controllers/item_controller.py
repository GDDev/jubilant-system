from .. import Routine
from ..services import ItemService


item_service = ItemService()


def add_workout():
    pass
    item_data = {}
    item_service.add_exercise_item(item_data)
