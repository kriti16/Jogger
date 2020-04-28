from flask import Flask, jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from app.database.db import init_db
from app.config import Config
from app.scheduler import init_scheduler

from app.api import api_bp
from app.api.auth import api as authapi
from app.api.subscribe import api as subscribeapi
from app.api.account import api as accountapi
from app.api.records import api as recordsapi

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(api_bp)

init_db(app)

mail = Mail(app)
init_scheduler(app, mail)

jwt = JWTManager(app)

if __name__ == "__main__":
	app.run()