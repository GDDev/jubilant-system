from app import app


class UserProfileController:

    @app.route('/profile/detail', methods=['POST'])
    def detail_profile(self):
        pass

    @app.route('/profile/update', methods=['POST'])
    def update_profile(self):
        pass

    # Maybe?
    @app.route('/profile/find', methods=['POST'])
    def find_profile(self):
        pass
