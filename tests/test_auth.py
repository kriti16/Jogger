import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase

class UserAuthTest(BaseCase):

	def test_admin_token(self):
		with app.app_context():
			BaseCase.add_admin(self)
			payload = json.dumps({
				"username": "admin",
				"password": "admin"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

	def test_none_auth(self):
		with app.app_context():
			payload = json.dumps({
				"username": "non_user",
				"password": "non_user"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(401, response.status_code)