from flask import jsonify, make_response, request
from flask_restplus import Resource, fields
from flask_jwt_extended import create_access_token

from app.database.models import User
from app.api.errors import error_response
from app.api import auth_ns, api

auth_fields = api.model('Auth', {
	'password': fields.String(required=True, description='Password', example='secure_password'),
    'username': fields.String(required=True, description='Username', example='athlete')
})

auth_response = api.model('Acess Token', {
    'access_token': fields.String(description='Bearer acess Token', example="secure_access_token")
})

@auth_ns.route('')
class AuthApi(Resource):

	@api.expect(auth_fields)
	@api.response(201, 'Success', model=auth_response)
	@api.response(400, 'Bad request')
	@api.response(401, 'Incorrect username or password')
	def post(self):
		""" Authorise user and provide access token"""
		username = request.json.get('username')
		password = request.json.get('password')
		user = User.find_by_username(username)
		if not user:
			return error_response('Username does not exist', 401)
		if not user.check_password(password):
			return error_response('Incorrect password', 401)
		access_token = create_access_token(identity=user.id)
		return make_response(jsonify(access_token = access_token), 201)