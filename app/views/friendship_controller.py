from app import main

class FriendshipController:

    @app.route('/friendship/add', methods=['POST'])
    def add_friend(self):
        pass

    @app.route('/friendship/remove', methods=['POST'])
    def remove_friend(self):
        pass

    @app.route('/friendship/get_all', methods=['POST'])
    def get_all_friends(self):
        pass