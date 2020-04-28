from flask import jsonify, make_response, request, current_app
from flask_restplus import Resource, fields, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from math import ceil

from app.database.models import User
from app.database.db import db
from app.api.roles import ROLES
from app.api.access_control import role_required, auth_required
from app.api.filtering import filter_users, filter_delete
from app.api.errors import error_response
from app.api import users_ns, api

parser = reqparse.RequestParser()
parser.add_argument('Authorization', location='headers', help='Bearer token', required=True)
parser.add_argument('page', type=int, required=False, location='args', help=1)
parser.add_argument('per_page', type=int, required=False, location='args', help=10)
parser.add_argument('filter', type=str, required=False, help='Supported operators >,<,=,!=,AND,OR', location='args')

token_parser = reqparse.RequestParser()
token_parser.add_argument('Authorization', location='headers', help='Bearer token', required=True)

del_parser = reqparse.RequestParser()
del_parser.add_argument('Authorization', location='headers', help='Bearer token', required=True)
del_parser.add_argument('filter', type=str, required=False, help='Supported operators >,<,=,!=,AND,OR', location='args')

meta_data = api.model('meta',{
	'total_items': fields.Integer(required=True, description='Total users', example=5),
	'page': fields.Integer(required=True, description='Current page number', example=2, default=1),
	'total_pages': fields.Integer(required=True, description='Total pages', example=4),
    'per_page': fields.Integer(required=True, description='Users per page', example=10, min=1)
})

user_info = api.model('user',{
	'id': fields.Integer(required=True, description='User id', example=5),
	'username': fields.String(required=True, description='Username', example='athlete'),
	'role': fields.Integer(required=True, description='Roles - 0:user, 1:user_managiger, 2:admin', example=1),
    'email': fields.String(required=True, description='user email', example='athlete@example.com'),
    'subscriber': fields.Boolean(required=True, description='Is user a subscriber', example=True, default=True)
})

users_list_response = api.model('UserList', {
    '_meta': fields.Nested(meta_data, description = 'Meta data'),
    'items': fields.List(fields.Nested(user_info)),
})

del_info = api.model('Del',{
	'count': fields.Integer(required=True, description='Number of users deleted', example=3)
})

put_fields = api.model('UpdateUser', {
	'password': fields.String(required=False, description='Password', example='secure_password'),
    'username': fields.String(required=False, description='Username', example='athlete'),
    'email': fields.String(required=False, description='Email', example='test@example.com')
})

post_fields = api.model('CreateUser', {
	'password': fields.String(required=True, description='Password', example='secure_password'),
    'username': fields.String(required=True, description='Username', example='athlete'),
    'email': fields.String(required=True, description='Email', example='test@example.com')
})

@users_ns.route('/all')
class UsersAllApi(Resource):

	@api.expect(parser, validate=True)
	@api.response(200, 'Success', model=users_list_response)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')

	@auth_required
	@jwt_required
	@role_required(ROLES['user_manager'])
	def get(self):
		""" Read information of all users.
		Note : Cannot read information of users with higher role"""
		parser.parse_args()
		current_user = User.query.get(get_jwt_identity())
		page = request.args.get('page', 1, type=int)
		per_page = request.args.get('per_page', current_app.config['USERS_PER_PAGE'], type=int)
		if per_page > current_app.config['USERS_PER_PAGE']:
			per_page = current_app.config['USERS_PER_PAGE']
		where_stmt = request.args.get('filter', "")
		if len(where_stmt)>0:
			where_stmt = 'WHERE role<=%d AND (%s)' %(current_user.role, where_stmt)
		else:
			where_stmt = 'WHERE role<=%d' %current_user.role
		(users, total) = filter_users(current_app, User.table_schema, 'user', where_stmt, page, per_page)
		total_pages = ceil(total/per_page)
		data = User.to_dict_collection(users, page, per_page, total_pages)
		if total>page*per_page:
			data['next_page'] = page+1
		if page>1:
			data['prev_page'] = page-1
		return make_response(jsonify(data), 200)

	@api.expect(del_parser, validate=True)
	@api.response(200, 'Success', model=del_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.response(403, 'Permission denied')

	@auth_required
	@jwt_required
	@role_required(ROLES['user_manager'])
	def delete(self):
		""" Delete all users. Cannot remove user with higher roles"""
		del_parser.parse_args()
		current_user = User.query.get(get_jwt_identity())
		where_stmt = request.args.get('filter', "")
		if len(where_stmt)>0:
			where_stmt = 'WHERE (role<=%d AND id!=%d) AND (%s)' %(current_user.role, current_user.id, where_stmt)
		else:
			where_stmt = 'WHERE role<=%d AND id!=%d' %(current_user.role, current_user.id)
		count = filter_delete(current_app, 'user', where_stmt)
		return make_response(jsonify(count=count), 200)

@users_ns.route('/<int:id>')
class UserApi(Resource):

	@api.expect(token_parser, validate=True)
	@api.response(200, 'Success', model=user_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.response(404, 'User not found')

	@auth_required
	@jwt_required
	def get(self, id):
		""" Get information of a particular user. Access level is restricted by roles.
		user : Can only access own information
		user_manager : Can access information of all users and user_managers
		admin : Can access information of everyone"""
		user = User.query.get(id)
		current_user = User.query.get(get_jwt_identity())
		if not user:
			return error_response('USER NOT FOUND', 404)
		if int(id)!=int(get_jwt_identity()) and (current_user.role<user.role or current_user.role==ROLES['user']):
			return error_response('PERMISSION DENIED', 403)
		else:
			return make_response(jsonify(user.to_dict()), 200)

	@api.expect(put_fields)
	@api.expect(token_parser, validate=True)
	@api.response(200, 'Success', model=user_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.response(403, 'Permission denied')
	@api.response(404, 'User not found')

	@auth_required
	@jwt_required
	def put(self, id):
		""" Edit information of a particular user. Access level is restricted by roles.
		user : Can only edit own information
		user_manager : Can edit information of all users and user_managers
		admin : Can edit information of everyone
		Note : Cannot update subscribe status and role"""
		token_parser.parse_args()
		user = User.query.get(id)
		current_user = User.query.get(get_jwt_identity())
		if not user:
			return error_response('USER NOT FOUND', 404)
		if int(id)!=int(get_jwt_identity()) and (current_user.role<user.role or current_user.role==ROLES['user']):
			return error_response('PERMISSION DENIED', 403)
		else:
			data = request.get_json() or {}
			try:
				user.update(data)	
			except Exception as e:
				return error_response(e, 400)
			db.session.commit()
			return make_response(jsonify(user.to_dict()), 200)

	@api.expect(token_parser, validate=True)
	@api.response(200, 'Success', del_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.response(403, 'Permission denied')
	@api.response(404, 'User not found')

	@auth_required
	@jwt_required
	def delete(self, id):
		""" Delete account of a particular user. Access level is restricted by roles.
		user : Can only delete own account
		user_manager : Can delete account of all users and user_managers
		admin : Can delete account of everyone """
		token_parser.parse_args()
		user = User.query.get(id)
		current_user = User.query.get(get_jwt_identity())
		if not user:
			return error_response('USER NOT FOUND', 404)
		if int(id)!=int(get_jwt_identity()) and (current_user.role<user.role or current_user.role==ROLES['user']):
			return error_response('PERMISSION DENIED', 403)
		db.session.delete(user)
		db.session.commit()
		return make_response(jsonify(count=1), 200)

@users_ns.route('/')
@users_ns.route('')
class UsersApi(Resource):

	@api.expect(post_fields)
	@api.response(201, 'Success', model=user_info)
	@api.response(400, 'username or email already exist')

	def post(self):
		""" Create user account"""
		data = request.get_json() or {}
		user = User()
		try:
			user.from_dict(data)
		except Exception as error:
			return error_response(error, 400)
		db.session.add(user)
		db.session.commit()
		return make_response(jsonify(user.to_dict()), 201)
