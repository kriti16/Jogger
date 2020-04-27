from flask import Flask, jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from app.database.db import init_db
from app.config import Config
from app.api.routes import init_routes
from app.scheduler import init_scheduler
from app.api_def import init_api

app = Flask(__name__)

app.config.from_object(Config)

init_db(app)
api = init_api(app)
init_routes(api)

mail = Mail(app)
init_scheduler(app, mail)

jwt = JWTManager(app)

if __name__ == "__main__":
	app.run()