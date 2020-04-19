from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import User
from app.database.db import db

class UsersApi(Resource):
	@jwt_required
	def get(self):
		data = User.to_dict_collection(User.query.all())
		return make_response(jsonify(data), 200)

	def post(self):
		data = request.get_json() or {}
		user = User()
		user.from_dict(data)
		db.session.add(user)
		db.session.commit()
		return make_response(jsonify(user.to_dict()), 201)