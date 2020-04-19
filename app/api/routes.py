from .account import UsersApi
from .records import RecordsApi
from .auth import AuthApi

def init_routes(api):
	api.add_resource(UsersApi, '/users')
	api.add_resource(RecordsApi, '/records')
	api.add_resource(AuthApi, '/auth')