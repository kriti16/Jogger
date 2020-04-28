import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class DeleteUsersTest(BaseCase):

	def test_delete_all_users_without_auth_header(self):
		with app.app_context():
			response = self.app.delete('/api/users/all')
			self.assertEqual(400, response.status_code)

	def test_delete_all_users_by_user(self):
		with app.app_context():
			BaseCase.add_user(self)
			payload = json.dumps({
				"username": "user",
				"password": "user"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.delete('/api/users/all', headers={"Authorization":authorization})
			self.assertEqual(403, response.status_code)

	def test_delete_all_users_by_user_manager(self):
		with app.app_context():
			BaseCase.add_user(self)
			BaseCase.add_user_manager(self)
			BaseCase.add_admin(self)
			payload = json.dumps({
				"username": "manager",
				"password": "manager"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.delete('/api/users/all', headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['count'])

	def test_delete_all_filtered_users_by_user_manager(self):
		with app.app_context():
			BaseCase.add_user(self)
			BaseCase.add_user_manager(self)
			BaseCase.add_admin(self)
			payload = json.dumps({
				"username": "manager",
				"password": "manager"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			q = "role>=1"
			response = self.app.delete('/api/users/all?filter=%s' %q, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(0, response.json['count'])

	def test_delete_all_users_by_admin(self):
		with app.app_context():
			BaseCase.add_user(self)
			BaseCase.add_user_manager(self)
			BaseCase.add_admin(self)
			payload = json.dumps({
				"username": "admin",
				"password": "admin"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.delete('/api/users/all', headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['count'])

	def test_delete_all_filtered_users_by_admin(self):
		with app.app_context():
			BaseCase.add_user(self)
			BaseCase.add_user_manager(self)
			BaseCase.add_admin(self)
			payload = json.dumps({
				"username": "admin",
				"password": "admin"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			q = "role>=1"
			response = self.app.delete('/api/users/all?filter=%s' %q, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['count'])

	def test_delete_user_id_by_none(self):
		with app.app_context():
			BaseCase.add_user(self)
			response = self.app.delete('/api/users/1')
			self.assertEqual(400, response.status_code)

	def test_delete_user_id_by_user(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
			BaseCase.add_user_manager(self)
			manager_id = BaseCase.get_user_id(self, 'manager')
			payload = json.dumps({
				"username": "user",
				"password": "user"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.delete('/api/users/%d' %manager_id, headers={"Authorization":authorization})
			self.assertEqual(403, response.status_code)

	def test_delete_user_id_self_by_user(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
			payload = json.dumps({
				"username": "user",
				"password": "user"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.delete('/api/users/%d' %user_id, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['count'])

	def test_delete_user_id_by_user_manager(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
			BaseCase.add_user_manager(self)
			payload = json.dumps({
				"username": "manager",
				"password": "manager"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.delete('/api/users/%d' %user_id, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['count'])

	def test_delete_user_id_by_admin(self):
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

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.delete('/api/users/%d' %user_id, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['count'])

			response = self.app.delete('/api/users/%d' %manager_id, headers={"Authorization":authorization})

			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['count'])

			response = self.app.get('/api/users/%d' %user_id, headers={"Authorization":authorization})
			self.assertEqual(404, response.status_code)