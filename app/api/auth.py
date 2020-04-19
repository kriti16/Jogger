from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from app.database.models import User

class AuthApi(Resource):
	def post(self):
		username = request.json.get('username')
		password = request.json.get('password')
		user = User.find_by_username(username)
		if user and user.check_password(password):
			access_token = create_access_token(identity=user.id)
			return make_response(jsonify(access_token=access_token), 200)