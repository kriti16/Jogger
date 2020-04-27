from flask import jsonify, make_response, request	
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import User
from app.database.db import db
from app.api.errors import error_response

class SubscribeApi(Resource):
	@jwt_required
	def post(self):
		user = User.query.get(get_jwt_identity())
		if user.subscriber:
			message = 'Already a subscriber'
		else:
			message = 'Subscribed successfully'
			user.subscriber = True
			db.session.commit()
		return make_response(jsonify(msg = message), 201)

class UnsubscribeApi(Resource):
	@jwt_required
	def post(self):
		user = User.query.get(get_jwt_identity())
		if user.subscriber:
			message = 'Unsubscribed successfully'
			user.subscriber = False
			db.session.commit()
		else:
			message = 'Not a subscriber'
		return make_response(jsonify(msg = message), 201)