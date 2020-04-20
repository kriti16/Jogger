from .account import UsersApi, UserApi
from .records import RecordsApi, RecordApi
from .auth import AuthApi

def init_routes(api):
	api.add_resource(UsersApi, '/users')
	api.add_resource(UserApi, '/users/<id>')
	api.add_resource(RecordsApi, '/records')
	api.add_resource(RecordApi, '/records/<id>')
	api.add_resource(AuthApi, '/auth')