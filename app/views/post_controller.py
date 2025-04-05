from app import app

class PostController:

    @app.route('/post/new', methods=['POST'])
    def new_post(self):
        pass

    @app.route('/post/update', methods=['POST'])
    def update_post(self):
        pass

    @app.route('/post/delete', methods=['POST'])
    def delete_post(self):
        pass

    @app.route('/post/user_posts', methods=['GET'])
    def get_user_posts(self):
        pass

    @app.route('/post/detail_post', methods=['GET'])
    def detail_post(self):
        pass

    # This will be the feed, probably.
    @app.route('/post/feed', methods=['GET'])
    def get_friends_posts(self): # maybe rename to feed
        pass
