from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from flask_jwt_extended import get_jwt_identity

from .db import db
from app.weather import get_weather_data
from app.api.roles import ROLES

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	username = db.Column(db.String(64), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	role = db.Column(db.Integer, nullable=False, default=ROLES['user'])	
	email = db.Column(db.String(320), nullable=False, unique=True)
	subscriber = db.Column(db.Boolean, nullable=False, default=True)

	records = db.relationship('Record', backref='runner', lazy='dynamic')
	table_schema = 'id, username, role, email, subscriber'

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def to_dict(self):
		data = {
			'id': self.id,
			'username': self.username,
			'role': self.role,
			'email': self.email,
			'subscriber': self.subscriber
		}
		return data

	def from_dict(self, data):
		for key in ['username', 'email', 'subscriber']:
			if key in data:
				setattr(self, key, data[key])
		if 'role' in data:
			self.role = data['role']
		else:
			self.role = ROLES['user']
		self.set_password(data['password'])

	def to_dict_collection(users):
		data = {
			'_meta' : {
				'total_items' : len(users)
			},
			'items':[User.to_dict(u) for u in users]
		}
		return data

	def find_by_username(username):
		return User.query.filter_by(username = username).first()

	def update(self, data):
		if 'username' in data:
			if data['username'] != self.username:
				user = User.find_by_username(data['username'])
				if user:
					print("username already exists")
					return
			self.username = data['username']
		if 'password' in data:
			self.set_password(data['password'])

class Record(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.String(10), nullable=False, default=date.today())	# 2016-01-01
	distance = db.Column(db.Integer, nullable=False, default=0) # in metres
	time = db.Column(db.Integer, nullable=False, default=1)	# 12:00:00
	latitude = db.Column(db.Float, nullable=False, default=-1)	
	longitude = db.Column(db.Float, nullable=False, default=-1)	
	weather = db.Column(db.String(100))
	entry_time = db.Column(db.String(8), nullable=False, default="12:00:00")	# 12:00:00
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	table_schema = 'id, date, distance, time, latitude, longitude, weather, entry_time, user_id'

	def to_dict(self):
		data = {
			'id': self.id,
			'date': self.date,
			'distance': self.distance, 
			'time': self.time,
			'latitude': self.latitude,
			'longitude': self.longitude,
			'weather': self.weather,
			'user_id': self.user_id
		}
		return data

	def from_dict(self, data):
		for key in ['date', 'distance', 'time', 'latitude', 'longitude']:
			if key in data:
				setattr(self, key, data[key])
		user = User.query.get(get_jwt_identity())
		if 'user_id' in data:
			if user.role==ROLES['admin'] or data['user_id']==int(get_jwt_identity()):
				new_user = User.query.get(data['user_id']);
				if not new_user:
					raise ValueError('user_id doesn\'t exist') 
				self.runner = new_user
			else:
				raise Exception('User id change not permitted')
				return 
		else:
			self.runner = user
		self.entry_time = datetime.now().strftime("%H:%M:%S")
		self.weather = get_weather_data(self.latitude, self.longitude, self.date, self.entry_time)

	def to_dict_collection(records):
		data = {
			'_meta' : {
				'total_items' : len(records)
			},
			'items':[Record.to_dict(r) for r in records]
		}
		return data

	def update(self, data):
		for key in ['date', 'distance', 'time', 'latitude', 'longitude']:
			if key in data:
				setattr(self, key, data[key])
		if 'user_id' in data:
			user = User.query.get(get_jwt_identity())
			if user.role==ROLES['admin'] or data['user_id']==int(get_jwt_identity()):
				new_user = User.query.get(data['user_id']);
				if not new_user:
					raise ValueError('user_id doesn\'t exist') 
				self.runner = new_user
			else:
				raise Exception('User id change not permitted')
		self.weather = get_weather_data(self.latitude, self.longitude, self.date, self.entry_time)