from flask import jsonify, make_response, request, current_app
from flask_restplus import Resource, reqparse, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from math import ceil

from app.database.models import Record, User
from app.database.db import db, es
from app.api.access_control import min_access_level, role_required, auth_required
from app.api.roles import ROLES
from app.api.filtering import filter_records, filter_delete
from app.api.errors import error_response
from app.api import records_ns, api

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

del_info = api.model('Del',{
	'count': fields.Integer(required=True, description='Number of users deleted', example=3)
})

meta_data = api.model('meta',{
	'total_items': fields.Integer(required=True, description='Total users', example=5),
	'page': fields.Integer(required=True, description='Current page number', example=2, default=1),
	'total_pages': fields.Integer(required=True, description='Total pages', example=4),
    'per_page': fields.Integer(required=True, description='Users per page', example=10, min=1)
})

record_info = api.model('record',{
	'id': fields.Integer(required=True, description='Record id', example=5),
	'date': fields.String(required=True, description='Date of jogging Format[yyyy-mm-dd]', example='2020-04-20'),
	'distance': fields.Integer(required=True, description='Jogging distance in metres', example=100),
    'time': fields.Integer(required=True, description='Jogging duration in seconds Format[hh:mm:ss]', example=3600),
    'latitude': fields.Float(required=True, description='Location latitude', example=10.3),
  	'longitude': fields.Float(required=True, description='Location longitude', example=120),
  	'weather': fields.String(required=False, description='Weather during jogging', example='Clear'),
  	'entry_time': fields.Integer(required=True, description='Logging time', example=''),
  	'user_id': fields.Integer(required=True, description='User id of runner', example=5)
})

records_list_response = api.model('RecordList', {
    '_meta': fields.Nested(meta_data, description = 'Meta data'),
    'items': fields.List(fields.Nested(record_info)),
})

put_fields = api.model('UpdateRecord', {
	'date': fields.String(required=False, description='Date of jogging Format[yyyy-mm-dd]', example='2020-04-20'),
	'distance': fields.Integer(required=False, description='Jogging distance in metres', example=100),
    'time': fields.Integer(required=False, description='Jogging duration in seconds Format[hh:mm:ss]', example=3600),
    'latitude': fields.Float(required=False, description='Location latitude', example=10.3),
  	'longitude': fields.Float(required=False, description='Location longitude', example=120)
})

post_fields = api.model('CreateRecord', {
	'date': fields.String(required=True, description='Date of jogging Format[yyyy-mm-dd]', example='2020-04-20'),
	'distance': fields.Integer(required=True, description='Jogging distance in metres', example=100),
    'time': fields.Integer(required=True, description='Jogging duration in seconds Format[hh:mm:ss]', example=3600),
    'latitude': fields.Float(required=True, description='Location latitude', example=10.3),
  	'longitude': fields.Float(required=True, description='Location longitude', example=120),
  	'user_id': fields.Integer(required=False, description='User id of runner', example=5)
})

@records_ns.route('/all')
class RecordsAllApi(Resource):

	@api.expect(parser, validate=True)
	@api.response(200, 'Success', model=records_list_response)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')

	@auth_required
	@jwt_required
	@role_required(ROLES['admin'])
	def get(self):
		""" Read records of all users """
		parser.parse_args()
		page = request.args.get('page', 1, type=int)
		per_page = request.args.get('per_page', current_app.config['RECORDS_PER_PAGE'], type=int)
		where_stmt = request.args.get('filter', "")
		if len(where_stmt)>0:
			where_stmt = 'WHERE ' + where_stmt
		(records, total) = filter_records(current_app, Record.table_schema, 'record', where_stmt, page, per_page)
		total_pages = ceil(total/per_page)
		data = Record.to_dict_collection(records, page, per_page, total_pages)
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
	@role_required(ROLES['admin'])
	def delete(self):
		""" Delete all records"""
		del_parser.parse_args()
		records = Record.query.all()
		where_stmt = request.args.get('filter', "")
		if len(where_stmt)>0:
			where_stmt = 'WHERE ' + where_stmt
		count = filter_delete(current_app, 'record', where_stmt)
		return make_response(jsonify(count = count), 200)

@records_ns.route('/<int:id>')
class RecordApi(Resource):

	@api.expect(token_parser, validate=True)
	@api.response(200, 'Success', model=record_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.response(404, 'Record not found')

	@auth_required
	@jwt_required
	def get(self, id):
		""" Read a particular record. Access level is restricted by roles.
		user : Can only access own records
		user_manager : Can only access own records
		admin : Can access all records"""
		record = Record.query.get(id)
		if not record:
			return error_response('RECORD_NOT_FOUND', 404)
		# PERMISSION_DENIED because don't want user to know this record id exists
		if record.runner.id!=int(get_jwt_identity()) and not min_access_level(self, ROLES['admin']):
			return error_response('RECORD_NOT_FOUND', 404)
		return make_response(jsonify(record.to_dict()), 200)

	@api.expect(put_fields)
	@api.expect(token_parser, validate=True)
	@api.response(200, 'Success', model=record_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.response(403, 'Permission denied')
	@api.response(404, 'Record not found')

	@auth_required
	@jwt_required
	def put(self, id):
		""" Edit a particular record. Access level is restricted by roles.
		user : Can only edit own record
		user_manager : Can only edit own record
		admin : Can edit all records
		Note : Cannot update weather information and entry_time. Updated automatically"""
		token_parser.parse_args()
		record = Record.query.get(id)
		if not record:
			return error_response('RECORD NOT FOUND', 404) 
		# PERMISSION_DENIED because don't want user to know this record id exists
		if record.runner.id!=int(get_jwt_identity()) and not min_access_level(self, ROLES['admin']):
			return error_response('RECORD NOT FOUND', 404) 

		data = request.get_json() or {}
		try:
			record.update(data)
		except ValueError as error:
			return error_response('RECORD NOT FOUND', 404)
		except Exception as error:
			return error_response('PERMISSION DENIED', 403)
		db.session.commit()
		return make_response(jsonify(record.to_dict()), 200)

	@api.expect(token_parser, validate=True)
	@api.response(200, 'Success', del_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.response(403, 'Permission denied')
	@api.response(404, 'Record not found')

	@auth_required
	@jwt_required
	def delete(self, id):
		""" Delete a particular record. Access level is restricted by roles.
		user : Can only delete own record
		user_manager : Can only delete own record
		admin : Can delete all records """
		token_parser.parse_args()
		record = Record.query.get(id)
		if not record:
			return error_response('RECORD NOT FOUND', 404) 
		# PERMISSION_DENIED because don't want user to know this record id exists
		if record.runner.id!=int(get_jwt_identity()) and not min_access_level(self, ROLES['admin']):
			return error_response('RECORD NOT FOUND', 404)

		db.session.delete(record)
		db.session.commit()
		return make_response(jsonify(count=1), 200)

@records_ns.route('')
class UserRecordsApi(Resource):

	@api.expect(parser, validate=True)
	@api.response(200, 'Success', del_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')

	@auth_required
	@jwt_required
	def get(self):
		""" Read all records of logged in user """
		parser.parse_args()
		user = User.query.get(get_jwt_identity())
		page = request.args.get('page', 1, type=int)
		per_page = request.args.get('per_page', current_app.config['RECORDS_PER_PAGE'], type=int)
		where_stmt = request.args.get('filter', "")
		if len(where_stmt) > 0:
			where_stmt = "WHERE user_id=%d AND (%s)" %(user.id, where_stmt)
		else:
			where_stmt = "WHERE user_id=%d" %user.id
		(records, total) = filter_records(current_app, Record.table_schema, 'record', where_stmt, page, per_page)	
		total_pages = ceil(total/per_page)
		data = Record.to_dict_collection(records, page, per_page, total_pages)
		if total>page*per_page:
			data['next_page'] = page+1
		if page>1:
			data['prev_page'] = page-1
		return make_response(jsonify(data), 200)

	@api.expect(token_parser, validate=True)
	@api.expect(post_fields)
	@api.response(201, 'Success', model=record_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.response(403, 'Permission denied')

	@auth_required
	@jwt_required
	def post(self):
		""" Create new record. weather and entry_time columns are filled automatically """
		token_parser.parse_args()
		data = request.get_json() or {}
		record = Record()
		try:
			record.from_dict(data)
		except ValueError as error:
			return error_response('user_id does not exist', 404)
		except Exception:
			return error_response('User id change not permitted', 403)
		db.session.add(record)
		db.session.commit()
		return make_response(jsonify(record.to_dict()), 201)

	@api.expect(del_parser, validate=True)
	@api.response(200, 'Success', model=del_info)
	@api.response(400, 'Invalid authentication header')
	@api.response(401, 'Authentication failed')
	@api.response(403, 'Permission denied')

	@auth_required
	@jwt_required
	def delete(self):
		""" Delete all records"""
		del_parser.parse_args()
		user = User.query.get(get_jwt_identity())
		where_stmt = request.args.get('filter', "")
		per_page = current_app.config['RECORDS_PER_PAGE']
		if len(where_stmt) > 0:
			where_stmt = "WHERE user_id=%d AND (%s)" %(user.id, where_stmt)
		else:
			where_stmt = "WHERE user_id=%d" %user.id
		count = filter_delete(current_app, 'record', where_stmt)
		return make_response(jsonify(count = count), 200)	