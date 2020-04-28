from flask import jsonify, make_response, request	
from flask_restplus import Resource, fields, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import User
from app.database.db import db
from app.api.errors import error_response
from app.api import subscribe_ns, api, unsubscribe_ns
from app.api.access_control import auth_required

parser = reqparse.RequestParser()
parser.add_argument('Authorization', location='headers', help='Bearer token', required=True)

subscribe_response = api.model('Subscribe', {
    'message': fields.String(description='Subscription status', example="Subscribed successfully")
})

unsubscribe_response = api.model('Unsubscribe', {
    'message': fields.String(description='Subscription status', example="Unsubscribed successfully")
})

@subscribe_ns.route('')
class SubscribeApi(Resource):

	@api.response(201, 'Success', model=subscribe_response)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.doc(parser = parser)
	@auth_required	
	@jwt_required
	def post(self):
		""" Subscribe to weekly jogging report"""
		parser.parse_args()
		user = User.query.get(get_jwt_identity())
		if user.subscriber:
			message = 'Already a subscriber'
		else:
			message = 'Subscribed successfully'
			user.subscriber = True
			db.session.commit()
		return make_response(jsonify(message=message), 201)

@unsubscribe_ns.route('')
class UnsubscribeApi(Resource):

	@api.response(201, 'Success', model = unsubscribe_response)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.doc(parser = parser)
	@auth_required
	@jwt_required
	def post(self):
		""" Unsubscribe to weekly jogging report"""
		parser.parse_args()
		user = User.query.get(get_jwt_identity())
		if user.subscriber:
			message = 'Unsubscribed successfully'
			user.subscriber = False
			db.session.commit()
		else:
			message = 'Not a subscriber'
		return make_response(jsonify(message = message), 201)