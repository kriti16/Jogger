from flask import jsonify, make_response
from werkzeug.http import HTTP_STATUS_CODES

def error_response(message, status_code):
	response = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
	response['message'] = message
	return make_response(jsonify(response), status_code)

def bad_request(message):
	error_response(message, 400)