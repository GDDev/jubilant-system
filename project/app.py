import os

from core import mock_100_users
from . import create_app, config_error_handlers

app = create_app()
config_error_handlers(app)
# if not os.environ.get("WERKZEUG_RUN_MAIN"):
#     mock_100_users(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9090, debug=True)
