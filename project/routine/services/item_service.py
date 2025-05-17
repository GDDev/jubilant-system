from ..repositories import ExerciseItemRepository


class ItemService:

    def __init__(self):
        self.item_repo = ExerciseItemRepository()

    # def add_exercise_item(self, item_data: dict):
    #     pass
    #     item_type = ItemType(item_data['item_type'])
    #     item = ExerciseItem(
    #         routine_id=item_data['routine_id'],
    #         type=item_type,
    #         name=item_data['name'],
    #         description=item_data['description'],
    #         exercise_id=item_data['exercise_id'],
    #         min_sets=item_data['min_sets'],
    #         max_sets=item_data['max_sets'],
    #         set_duration=item_data['set_duration'],
    #         set_interval=item_data['set_interval'],
    #         min_reps=item_data['min_reps'],
    #         max_reps=item_data['max_reps'],
    #         weight=item_data['weight']
    #     )
    #     if item_data.get('expiration_date'):
    #         item.expiration_date = item_data['expiration_date']
    #     self.item_repo.insert(item)
    #
    # def add_meal_opt_item(self, item_data: dict):
    #     pass
