from flask import jsonify, make_response, request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import User
from app.database.db import db
from app.api.roles import ROLES
from app.api.access_control import min_access_level, role_required
from app.api.filtering import filter_users, filter_delete

# /users
class UsersApi(Resource):
	@jwt_required
	@role_required(ROLES['user_manager'])
	def get(self):
		current_user = User.query.get(get_jwt_identity())
		page = request.args.get('page', 1, type=int)
		where_stmt = request.args.get('filter', "")
		if len(where_stmt)>0:
			where_stmt = 'WHERE role<=%d AND (%s)' %(current_user.role, where_stmt)
		else:
			where_stmt = 'WHERE role<=%d' %current_user.role
		per_page = current_app.config['USERS_PER_PAGE']
		(users, total) = filter_users(current_app, User.table_schema, 'user', where_stmt, page, per_page)
		data = User.to_dict_collection(users)
		if total>page*per_page:
			data['next_page'] = page+1
		if page>1:
			data['prev_page'] = page-1
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
	@role_required(ROLES['user_manager'])
	def delete(self):
		current_user = User.query.get(get_jwt_identity())
		where_stmt = request.args.get('filter', "")
		if len(where_stmt)>0:
			where_stmt = 'WHERE role<=%d AND (%s)' %(current_user.role, where_stmt)
		else:
			where_stmt = 'WHERE role<=%d' %current_user.role
		count = filter_delete(current_app, 'user', where_stmt)
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
