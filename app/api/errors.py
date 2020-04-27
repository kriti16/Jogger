from flask import jsonify, make_response
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
	response = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
	if message:
		response['msg'] = message
	return make_response(jsonify(response), status_code)

def bad_request(message):
	error_response(400, message)