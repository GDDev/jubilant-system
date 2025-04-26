from . import create_app, config_error_handlers

if __name__ == '__main__':
    app = create_app()
    config_error_handlers(app)
    app.run(host='127.0.0.1', port=8000, debug=True)
