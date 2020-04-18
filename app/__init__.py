from flask import Flask
from database.db import init_db
from config import Config
from flask_restful import Api
from api.routes import init_routes

app = Flask(__name__)
api = Api(app)

app.config.from_object(Config)

init_db(app)

init_routes(api)