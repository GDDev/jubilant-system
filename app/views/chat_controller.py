from app import app

class ChatController:

    @app.route('/chat/new', methods=['POST'])
    def new_chat(self):
        pass

    @app.route('/chat/delete/', methods=['POST'])
    def delete_chat(self):
        pass

    @app.route('/chat/<chat_id>', methods=['POST'])
    def detail_chat(self):
        pass

    @app.route('/chat/list', methods=['POST'])
    def list_user_chats(self):
        pass
