from app.app import app

class UserController:

    @app.route('/user/sign_up', methods=['POST'])
    def sign_up(self):
        pass

    @app.route('/user/update_email', methods=['POST'])
    def update_email(self):
        pass

    @app.route('/user/delete', methods=['POST'])
    def delete_user(self):
        pass
