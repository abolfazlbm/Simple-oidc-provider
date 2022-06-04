from flask import jsonify
from webargs.flaskparser import parser


class CustomException(Exception):
    def __init__(self, message, status=400, code=None, error_message=None, ):
        self.error_message = error_message
        self.message = message
        self.status = status
        self.code = code
        if self.error_message is None:
            self.error_message = message
        super().__init__(
            {"message": self.message, "status": self.status, "code": self.code, "error_message": self.error_message})


class BadRequest(CustomException):
    """Custom exception class to be thrown when local error occurs."""
    status = 400


class NoResultFound(CustomException):
    code = 102
    message = "Result Not Found"


def init_error_handeler(app):
    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        """Catch BadRequest exception globally, serialize into JSON, and respond with 400."""
        message = error.message
        status_code = error.status
        response = {
            'status': status_code,
            'message': message,
            'error': {
                'type': error.__class__.__name__,
                'message': message,
                'code': error.code
            }
        }
        return jsonify(response), status_code

    @app.errorhandler(Exception)
    def handle_error(error):
        """Catch all exceptions globally, serialize into JSON, and respond with 500."""
        print(error)
        if 'message' in error.__dict__:
            message = error.message
        else:
            message = "Internal Server Error"

        if 'code' in error.__dict__:
            code = error.code
        else:
            code = 0

        if 'status' in error.__dict__:
            status = error.status
        else:
            status = 500

        if 'error_message' in error.__dict__:
            error_message = error.error_message
        else:
            error_message = message

        response = {
            'status': status,
            'message': message,
            'error': {
                'type': error.__class__.__name__,
                'message': error_message,
                'code': code
            }
        }
        return jsonify(response), status

    @parser.error_handler
    def handle_error(error, req, schema, *, error_status_code, error_headers):
        raise CustomException(message="Validation error", error_message=error.messages, code=9103, status=400)

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(
            {"message": "Address not found", "status": 404,
             "error": {'type': e.__class__.__name__, 'message': 'Url Incorrect',
                       'code': 9001}}), 404
