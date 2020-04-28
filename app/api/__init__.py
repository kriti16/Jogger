from flask_restplus import Api
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, title='Jogger API', description='REST API')

users_ns = api.namespace('users', 'User APIs')
records_ns = api.namespace('records', 'User records APIs')
auth_ns = api.namespace('auth', 'Authorise user')
subscribe_ns = api.namespace('subscribe', 'Subscribe')
unsubscribe_ns = api.namespace('unsubscribe', 'Unsubscribe')