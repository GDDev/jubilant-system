from app import app

class UserProfileController:

    @app.route('/profile/sing_in', methods=['POST'])
    def sing_in(self):
        pass

    @app.route('/profile/sign_out', methods=['GET'])
    def sign_out(self):
        pass

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
