from .account import UsersApi
from .records import RecordsApi

def init_routes(api):
	api.add_resource(UsersApi, '/users')
	api.add_resource(RecordsApi, '/records')