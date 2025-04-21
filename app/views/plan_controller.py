from app import main

class PlanController:

    @app.route('/plan/new', methods=['POST'])
    def new_plan(self):
        pass

    @app.route('/plan/update/', methods=['POST'])
    def update_plan(self):
        pass

    @app.route('/plan/delete/', methods=['POST'])
    def delete_plan(self):
        pass

    @app.route('/plan/<plan_name>', methods=['POST'])
    def detail_plan(self):
        pass

    @app.route('/plan/list', methods=['POST'])
    def list_all_plans(self):
        pass
