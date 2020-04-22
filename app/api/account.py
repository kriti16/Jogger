from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import User
from app.database.db import db
from app.api.roles import ROLES
from app.api.access_control import min_access_level

class UsersApi(Resource):
	@jwt_required
	def get(self):
		current_user = User.query.get(get_jwt_identity())
		if(current_user.role < ROLES['user_manager']):
			return make_response(jsonify(error="PERMISSION DENIED"), 403)
		data = User.to_dict_collection(User.query.all())
		return make_response(jsonify(data), 200)	

	def post(self):
		data = request.get_json() or {}
		user = User()
		user.from_dict(data)
		if user.role == ROLES['user']:
			db.session.add(user)
			db.session.commit()
			return make_response(jsonify(user.to_dict()), 201)				
		try:
			if min_access_level(self, user.role):
				db.session.add(user)
				db.session.commit()
				return make_response(jsonify(user.to_dict()), 201)
			else:
				return make_response(jsonify(error = 'PERMISSION DENIED'), 403)	
		except:
			return make_response(jsonify(error = 'PERMISSION DENIED'), 403)

	@jwt_required
	def delete(self):
		if not min_access_level(self, ROLES['user_manager']):
			return make_response(jsonify(error = 'PERMISSION_DENIED'), 403)
		users = User.query.all()
		current_user = User.query.get(get_jwt_identity())
		count = 0
		for u in users:
			if u.role <= current_user.role:
				db.session.delete(u)
				count+=1
		db.session.commit()
		return make_response(jsonify(count=count), 200)


class UserApi(Resource):
	@jwt_required
	def get(self, id):
		user = User.query.get(id)
		if not user:
			return make_response(jsonify(error = 'USER NOT FOUND'), 404)
		if int(id)==int(get_jwt_identity()) or min_access_level(self, ROLES['user_manager']):
			return make_response(jsonify(user.to_dict()), 200)
		else:
			return make_response(jsonify(error = 'PERMISSION DENIED'), 403)

	@jwt_required
	def put(self, id):
		user = User.query.get(id)
		if int(id) != int(get_jwt_identity()) and not min_access_level(self, ROLES['user_manager']):
			return make_response(jsonify(error='PERMISSION_DENIED'), 403)
		if min_access_level(self, user.role):
			data = request.get_json() or {}
			print(data)
			user.update(data)	
			db.session.commit()
			return make_response(jsonify(user.to_dict()), 200)
		else:
			return make_response(jsonify(error='PERMISSION_DENIED'), 403)

	@jwt_required
	def delete(self, id):
		user = User.query.get(id)
		if int(id) != int(get_jwt_identity()) and not min_access_level(self, ROLES['user_manager']):
			return make_response(jsonify(error='PERMISSION_DENIED'), 403)
		if min_access_level(self, user.role):
			data = user.to_dict()
			db.session.delete(user)
			db.session.commit()
			return make_response(jsonify(data), 200)
		else:
			return make_response(jsonify(error='PERMISSION_DENIED'), 403)
