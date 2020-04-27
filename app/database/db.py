from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from elasticsearch import Elasticsearch

db = SQLAlchemy()
migrate = Migrate()
es = Elasticsearch()

def init_db(app):
	db.init_app(app)
	migrate.init_app(app, db)