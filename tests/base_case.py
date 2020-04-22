import json
import unittest
import os

from app import app
from app.database.db import db
from app.database.models import User
from app.api.roles import ROLES

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, 'app_test.db')

class BaseCase(unittest.TestCase):	
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' %path
		with app.app_context():
			self.app = app.test_client()
			db.create_all()

	def add_admin(self):
		with app.app_context():
			u = User(username='admin', role=ROLES['admin'])
			u.set_password('admin')
			db.session.add(u)
			db.session.commit()		

	def add_user_manager(self):
		with app.app_context():
			u = User(username='manager', role=ROLES['user_manager'])
			u.set_password('manager')
			db.session.add(u)
			db.session.commit()	

	def add_user(self):
		with app.app_context():
			u = User(username='user', role=ROLES['user'])
			u.set_password('user')
			db.session.add(u)
			db.session.commit()

	def get_user_id(self, username):
		with app.app_context():
			u = User.find_by_username(username)
			return u.id

	#Called after every test function in the class
	def tearDown(self):
		with app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()