import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase


class SubscriptionTest(BaseCase):

	def test_subscribe_by_none(self):
		with app.app_context():
			payload = json.dumps({
				"username": "test",
				"password": "test"
				})

			response = self.app.post('/subscribe', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(401, response.status_code)

	def test_subscribe_by_user(self):
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

			payload = json.dumps({
				"email": "test@gmail.com"
				})

			response = self.app.post('/subscribe', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertEqual(user_id, response.json['user_id'])
			self.assertEqual("user", response.json['username'])
			self.assertEqual("test@gmail.com", response.json['email'])
			self.assertIsNotNone(response.json['id'])

	def test_subscribe_by_user_without_email(self):
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

			payload = json.dumps({})

			response = self.app.post('/subscribe', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(400, response.status_code)

	def test_update_subscribe_by_user(self):
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

			payload = json.dumps({
				"email": "test@gmail.com"
				})

			response = self.app.post('/subscribe', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)

			payload = json.dumps({
				"email": "newtest@gmail.com"
				})

			response = self.app.put('/subscribe', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(200, response.status_code)

			response = self.app.get('/subscribe', headers={"Authorization":authorization},)
			self.assertEqual(user_id, response.json['user_id'])
			self.assertEqual("user", response.json['username'])
			self.assertEqual("newtest@gmail.com", response.json['email'])
			self.assertIsNotNone(response.json['id'])

	def test_update_subscribe_by_non_subscriber(self):
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

			payload = json.dumps({
				"email": "newtest@gmail.com"
				})

			response = self.app.put('/subscribe', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(404, response.status_code)

	def test_unsubscribe_by_user(self):
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

			payload = json.dumps({
				"email": "test@gmail.com"
				})

			response = self.app.post('/subscribe', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)

			response = self.app.post('/unsubscribe', headers={"Authorization":authorization})
			self.assertEqual(201, response.status_code)

			response = self.app.get('/subscribe', headers={"Authorization":authorization},)
			self.assertEqual(404, response.status_code)

	def test_unsubscribe_by_non_subscriber(self):
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

			response = self.app.post('/unsubscribe', headers={"Authorization":authorization})
			self.assertEqual(404, response.status_code)