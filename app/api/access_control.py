from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, make_response, request, current_app
import jwt

from app.database.models import User
from .errors import error_response

def role_required(role):
	def decorator(f):
		def wrapper(self, *args):
			user = User.query.get(get_jwt_identity())
			if user.role<role:
				return error_response('Operation not permitted for this role', 403)
			return f(self, *args)
		return wrapper
	return decorator

def auth_required(f):
	def wrapper(*args, **kwargs):
		if 'Authorization' not in request.headers:
			return error_response('Bearer Authorization header required', 400)
		auth = str(request.headers.get('Authorization'))
		if not auth.startswith('Bearer '):
			return error_response('Invalid Bearer auth token', 400)
		auth = auth.split(' ', 1)[1]
		try:
			jwt.decode(auth, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
		except:
			return error_response('Invalid Bearer auth token', 400)
		return f(*args, **kwargs)
	return wrapper

@jwt_required
def min_access_level(self, role):
	current_user = User.query.get(get_jwt_identity())
	return current_user.role>=role