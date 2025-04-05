from app import app

class MajorController:

    @app.route('/major/list', methods=['GET'])
    def list_all_majors(self):
        pass

    @app.route('/major/add', methods=['POST'])
    def add_major(self):
        pass

    @app.route('/major/update', methods=['POST'])
    def update_major(self):
        pass

    # Maybe?
    @app.route('/major/delete', methods=['POST'])
    def delete_major(self):
        pass
