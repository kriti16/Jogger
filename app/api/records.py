from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import Record
from app.database.db import db

class RecordsApi(Resource):
	@jwt_required
	def get(self):
		data = Record.to_dict_collection(Record.query.all())
		return make_response(jsonify(data), 200)

	@jwt_required
	def post(self):
		data = request.get_json() or {}
		record = Record()
		record.from_dict(data)
		db.session.add(record)
		db.session.commit()
		return make_response(jsonify(id=record.id), 201)

class RecordApi(Resource):
	@jwt_required
	def put(self, id):
		data = request.get_json() or {}
		record = Record.query.get(id)
		record.update(data)
		db.session.commit()
		return make_response('', 200)

	@jwt_required
	def delete(self, id):
		record = Record.query.get(id)
		db.session.delete(record)
		db.session.commit()
		return make_response('', 200)