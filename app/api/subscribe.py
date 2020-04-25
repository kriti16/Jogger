from flask import jsonify, make_response, request	

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import Subscriber, User
from app.database.db import db

class SubscribeApi(Resource):
	@jwt_required
	def get(self):
		user = User.query.get(get_jwt_identity())
		if not user.email:
			return make_response(jsonify(error='User not a subscriber'), 404)			
		subscriber = Subscriber.query.get(user.email.id)
		return make_response(jsonify(subscriber.to_dict()), 200)

	@jwt_required
	def post(self):
		data = request.get_json() or {}
		subscriber = Subscriber()
		try:
			subscriber.from_dict(data)
		except ValueError as error:
			return make_response(jsonify(error = 'email required'), 400)
		db.session.add(subscriber)
		db.session.commit()
		return make_response(jsonify(subscriber.to_dict()), 201)

	@jwt_required
	def put(self):
		user = User.query.get(get_jwt_identity())
		if not user.email:
			return make_response(jsonify(error='User not a subscriber'), 404)			
		subscriber = Subscriber.query.get(user.email.id)
		data = request.get_json() or {}
		subscriber.update(data)
		db.session.commit()
		return make_response(jsonify(subscriber.to_dict()), 200)

class UnsubscribeApi(Resource):
	@jwt_required
	def post(self):
		user = User.query.get(get_jwt_identity())
		if not user.email:
			return make_response(jsonify(error='User not a subscriber'), 404)			
		subscriber = Subscriber.query.get(user.email.id)
		db.session.delete(subscriber)
		db.session.commit()
		return make_response(jsonify(msg = 'Unsubscribed'), 201)