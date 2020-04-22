import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class ReadUsersTest(BaseCase):

	def test_read_users_by_none(self):
		with app.app_context():
			response = self.app.get('/users')
			self.assertEqual(401, response.status_code)

	def test_read_users_by_user(self):
		with app.app_context():
			BaseCase.add_user(self)
			payload = json.dumps({
				"username": "user",
				"password": "user"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.get('/users', headers={"Authorization":authorization})
			self.assertEqual(403, response.status_code)

	def test_read_users_by_user_manager(self):
		with app.app_context():
			BaseCase.add_user(self)
			BaseCase.add_user_manager(self)
			payload = json.dumps({
				"username": "manager",
				"password": "manager"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.get('/users', headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['_meta']['total_items'])

	def test_read_users_by_admin(self):
		with app.app_context():
			BaseCase.add_user(self)
			BaseCase.add_user_manager(self)
			BaseCase.add_admin(self)
			payload = json.dumps({
				"username": "admin",
				"password": "admin"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.get('/users', headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(3, response.json['_meta']['total_items'])

	def test_read_user_id_by_none(self):
		with app.app_context():
			BaseCase.add_user(self)
			response = self.app.get('/users/1')
			self.assertEqual(401, response.status_code)

	def test_read_user_id_by_user(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
			BaseCase.add_user_manager(self)
			manager_id = BaseCase.get_user_id(self, 'manager')
			payload = json.dumps({
				"username": "user",
				"password": "user"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.get('/users/%d' %manager_id, headers={"Authorization":authorization})
			self.assertEqual(403, response.status_code)

	def test_read_user_id_self_by_user(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
			payload = json.dumps({
				"username": "user",
				"password": "user"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.get('/users/%d' %user_id, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_id, response.json['id'])
			self.assertEqual('user', response.json['username'])

	def test_read_user_id_by_user_manager(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
			BaseCase.add_user_manager(self)
			payload = json.dumps({
				"username": "manager",
				"password": "manager"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.get('/users/%d' %user_id, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_id, response.json['id'])
			self.assertEqual('user', response.json['username'])

	def test_read_user_id_by_admin(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
			BaseCase.add_user_manager(self)
			manager_id = BaseCase.get_user_id(self, 'manager')
			BaseCase.add_admin(self)
			payload = json.dumps({
				"username": "admin",
				"password": "admin"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.get('/users/%d' %user_id, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_id, response.json['id'])
			self.assertEqual('user', response.json['username'])

			response = self.app.get('/users/%d' %manager_id, headers={"Authorization":authorization})

			self.assertEqual(200, response.status_code)
			self.assertEqual(manager_id, response.json['id'])
			self.assertEqual('manager', response.json['username'])