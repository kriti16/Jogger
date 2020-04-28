import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class CreateUserTest(BaseCase):

	def test_create_user_without_email(self):
		with app.app_context():
			payload = json.dumps({
				"username": "test",
				"password": "test",
				"role": ROLES['user']
				})

			response = self.app.post('/api/users', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(400, response.status_code)

	def test_create_user(self):
		with app.app_context():
			payload = json.dumps({
				"username": "test",
				"password": "test",
				"email": "test@example.com"
				})

			response = self.app.post('/api/users', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertTrue('id' in response.json)
			self.assertEqual("test", response.json['username'])
			self.assertEqual("test@example.com", response.json['email'])
			self.assertEqual(True, response.json['subscriber'])