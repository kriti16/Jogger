from .account import UsersApi, UserApi
from .records import RecordsApi, RecordApi, UserRecordsApi
from .auth import AuthApi
from .subscribe import SubscribeApi, UnsubscribeApi

def init_routes(api):
	api.add_resource(UsersApi, '/api/users')
	api.add_resource(UserApi, '/api/users/<id>')
	api.add_resource(UserRecordsApi, '/api/records')	# Records related to a user
	api.add_resource(RecordsApi, '/api/records/all')
	api.add_resource(RecordApi, '/api/records/<id>')
	api.add_resource(AuthApi, '/api/auth')
	api.add_resource(SubscribeApi, '/api/subscribe')
	api.add_resource(UnsubscribeApi, '/api/unsubscribe')