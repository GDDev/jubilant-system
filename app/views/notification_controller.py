from app import app

class NotificationController:

    @app.route('/notification/list', methods=['GET'])
    def list_all_notifications(self):
        pass
