from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(410)
def handle_410_response(error):
    status_code = 410
    success = False
    response = {
        'success': success,
        'error': {
            'type': 'Gone',
            'message': 'Resource has expired or no longer exists.'
        }
    }
    return jsonify(response), status_code
