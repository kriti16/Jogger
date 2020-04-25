from .account import UsersApi, UserApi
from .records import RecordsApi, RecordApi, UserRecordsApi
from .auth import AuthApi
from .subscribe import SubscribeApi, UnsubscribeApi

def init_routes(api):
	api.add_resource(UsersApi, '/users')
	api.add_resource(UserApi, '/users/<id>')
	api.add_resource(UserRecordsApi, '/records')	# Records related to a user
	api.add_resource(RecordsApi, '/records/all')
	api.add_resource(RecordApi, '/records/<id>')
	api.add_resource(AuthApi, '/auth')
	api.add_resource(SubscribeApi, '/subscribe')
	api.add_resource(UnsubscribeApi, '/unsubscribe')