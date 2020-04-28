import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class UpdateUserTest(BaseCase):

	def test_update_user_id_by_none(self):
		with app.app_context():
			BaseCase.add_user(self)
			response = self.app.put('/api/users/1')
			self.assertEqual(400, response.status_code)

	def test_update_user_id_by_user(self):
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

			payload = json.dumps({
				"username": "new_user"
				})
			response = self.app.put('/api/users/%d' %manager_id, headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(403, response.status_code)

	def test_update_user_id_self_by_user(self):
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

			payload = json.dumps({
				"username": "new_user"
				})
			response = self.app.put('/api/users/%d' %user_id, headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)

			self.assertEqual(200, response.status_code)
			self.assertEqual(user_id, response.json['id'])
			self.assertEqual('new_user', response.json['username'])

	def test_update_user_id_by_user_manager(self):
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

			payload = json.dumps({
				"username": "new_user"
				})

			response = self.app.put('/api/users/%d' %user_id, headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_id, response.json['id'])
			self.assertEqual('new_user', response.json['username'])

	def test_update_user_id_by_admin(self):
		with app.app_context():
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

			payload = json.dumps({
				"username": "new_manager"
				})

			response = self.app.put('/api/users/%d' %manager_id, headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(manager_id, response.json['id'])
			self.assertEqual('new_manager', response.json['username'])

			reponse = self.app.get('/api/users/%d' %manager_id, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(manager_id, response.json['id'])
			self.assertEqual('new_manager', response.json['username'])			