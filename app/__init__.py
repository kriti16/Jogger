from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from app.database.db import init_db
from app.config import Config
from app.api.routes import init_routes

app = Flask(__name__)

api = Api(app)

app.config.from_object(Config)

init_db(app)

init_routes(api)

jwt = JWTManager(app)

if __name__ == "__main__":
	app.run()