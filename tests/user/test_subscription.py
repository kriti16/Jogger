import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase

class SubscriptionTest(BaseCase):

	def test_subscribe_by_none(self):
		with app.app_context():
			response = self.app.post('/api/subscribe', headers={"Content-Type": "application/json"})
			self.assertEqual(401, response.status_code)

	def test_subscribe_by_user(self):
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
			response = self.app.post('/api/subscribe', headers={"Content-Type": "application/json", "Authorization":authorization})
			self.assertEqual(201, response.status_code)
			self.assertEqual('Already a subscriber', response.json['msg'])

	def test_unsubscribe_by_user(self):
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

			response = self.app.post('/api/unsubscribe', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertEqual('Unsubscribed successfully', response.json['msg'])

			response = self.app.post('/api/subscribe', headers={"Authorization":authorization})
			self.assertEqual(201, response.status_code)
			self.assertEqual('Subscribed successfully', response.json['msg'])

	def test_unsubscribe_by_non_subscriber(self):
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

			response = self.app.post('/api/unsubscribe', headers={"Authorization":authorization})
			self.assertEqual(201, response.status_code)
			self.assertEqual('Unsubscribed successfully', response.json['msg'])

			response = self.app.post('/api/unsubscribe', headers={"Authorization":authorization})
			self.assertEqual(201, response.status_code)
			self.assertEqual('Not a subscriber', response.json['msg'])