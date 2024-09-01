from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Oops, an error occurred: {str(e)}")
        response = {
            "error": "General Internal Server Error",
            "message": f"Oops, an error occurred: {str(e)}",
        }
        return jsonify(response), 500
