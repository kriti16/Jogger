from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, make_response

from app.database.models import User

def role_required(role):
	def decorator(f):
		def wrapper(self, *args):
			user = User.query.get(get_jwt_identity())
			if user.role<role:
				return make_response(jsonify(error='PERMISSION_DENIED'), 403)
			return f(self, *args)
		return wrapper
	return decorator

@jwt_required
def min_access_level(self, role):
	current_user = User.query.get(get_jwt_identity())
	return current_user.role>=role