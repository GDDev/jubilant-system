from app import main


class UserController:

    @app.route('/user/update_email', methods=['POST'])
    def update_email(self):
        pass

    @app.route('/user/delete', methods=['POST'])
    def delete_user(self):
        pass
