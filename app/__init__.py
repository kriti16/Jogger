from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from app.database.db import init_db
from app.config import Config
from app.api.routes import init_routes
from app.scheduler import init_scheduler

app = Flask(__name__)

api = Api(app)

app.config.from_object(Config)

init_db(app)

init_routes(api)

mail = Mail(app)
init_scheduler(app, mail)

jwt = JWTManager(app)

if __name__ == "__main__":
	app.run()