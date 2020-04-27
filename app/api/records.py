from flask import jsonify, make_response, request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import Record, User
from app.database.db import db, es
from app.api.access_control import min_access_level, role_required
from app.api.roles import ROLES
from app.api.filtering import filter_records, filter_delete

# /records/all
class RecordsApi(Resource):
	@jwt_required
	@role_required(ROLES['admin'])
	def get(self):
		page = request.args.get('page', 1, type=int)
		where_stmt = request.args.get('filter', "")
		per_page = current_app.config['RECORDS_PER_PAGE']
		if len(where_stmt)>0:
			where_stmt = 'WHERE ' + where_stmt
		(records, total) = filter_records(current_app, Record.table_schema, 'record', where_stmt, page, per_page)
		data = Record.to_dict_collection(records)
		if total>page*per_page:
			data['next_page'] = page+1
		if page>1:
			data['prev_page'] = page-1
		return make_response(jsonify(data), 200)

	@jwt_required
	@role_required(ROLES['admin'])
	def delete(self):
		records = Record.query.all()
		where_stmt = request.args.get('filter', "")
		if len(where_stmt)>0:
			where_stmt = 'WHERE ' + where_stmt
		count = filter_delete(current_app, 'record', where_stmt)
		return make_response(jsonify(count = count), 200)

# /records/<id>
class RecordApi(Resource):
	@jwt_required
	def get(self, id):
		record = Record.query.get(id)
		if not record:
			return make_response(jsonify(error='NOT_FOUND'), 404)
		# PERMISSION_DENIED because don't want user to know this record id exists
		if record.runner.id!=int(get_jwt_identity()) and not min_access_level(self, ROLES['admin']):
			return make_response(jsonify(error='NOT_FOUND'), 404)
		return make_response(jsonify(record.to_dict()), 200)

	@jwt_required
	def put(self, id):
		record = Record.query.get(id)
		if not record:
			return make_response(jsonify(error='NOT_FOUND'), 404) 
		# PERMISSION_DENIED because don't want user to know this record id exists
		if record.runner.id!=int(get_jwt_identity()) and not min_access_level(self, ROLES['admin']):
			return make_response(jsonify(error='NOT_FOUND'), 404)

		data = request.get_json() or {}
		try:
			record.update(data)
		except ValueError as error:
			print(error)
			return make_response(jsonify(error='User Id doesn\'t exist'), 404)
		except Exception as error:
			print(error)
			return make_response(jsonify(error='PERMISSION_DENIED'), 403)
		db.session.commit()
		return make_response(jsonify(record.to_dict()), 200)

	@jwt_required
	def delete(self, id):
		record = Record.query.get(id)
		if not record:
			return make_response(jsonify(error='NOT_FOUND'), 404) 
		# PERMISSION_DENIED because don't want user to know this record id exists
		if record.runner.id!=int(get_jwt_identity()) and not min_access_level(self, ROLES['admin']):
			return make_response(jsonify(error='NOT_FOUND'), 404)

		data = record.to_dict()
		db.session.delete(record)
		db.session.commit()
		return make_response(jsonify(data), 200)

# /records
class UserRecordsApi(Resource):
	@jwt_required
	def get(self):
		user = User.query.get(get_jwt_identity())
		page = request.args.get('page', 1, type=int)
		where_stmt = request.args.get('filter', "")
		per_page = current_app.config['RECORDS_PER_PAGE']
		if len(where_stmt) > 0:
			where_stmt = "WHERE user_id=%d AND (%s)" %(user.id, where_stmt)
		else:
			where_stmt = "WHERE user_id=%d" %user.id
		(records, total) = filter_records(current_app, Record.table_schema, 'record', where_stmt, page, per_page)	
		data = Record.to_dict_collection(records)
		if total>page*per_page:
			data['next_page'] = page+1
		if page>1:
			data['prev_page'] = page-1
		return make_response(jsonify(data), 200)

	@jwt_required
	def post(self):
		data = request.get_json() or {}
		record = Record()
		try:
			record.from_dict(data)
		except ValueError as error:
			print(error)
			return make_response(jsonify(error='User Id doesn\'t exist'), 404)
		except Exception as error:
			print(error)
			return make_response(jsonify(error='PERMISSION_DENIED'), 403)
		db.session.add(record)
		db.session.commit()
		return make_response(jsonify(record.to_dict()), 201)

	@jwt_required
	def delete(self):
		user = User.query.get(get_jwt_identity())
		where_stmt = request.args.get('filter', "")
		per_page = current_app.config['RECORDS_PER_PAGE']
		if len(where_stmt) > 0:
			where_stmt = "WHERE user_id=%d AND (%s)" %(user.id, where_stmt)
		else:
			where_stmt = "WHERE user_id=%d" %user.id
		# print(where_stmt)
		count = filter_delete(current_app, 'record', where_stmt)
		return make_response(jsonify(count = count), 200)	