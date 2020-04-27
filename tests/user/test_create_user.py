import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class CreateUserTest(BaseCase):

	def test_create_user_by_none(self):
		with app.app_context():
			payload = json.dumps({
				"username": "test",
				"password": "test",
				"role": ROLES['user']
				})

			response = self.app.post('/api/users', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertEqual("test", response.json['username'])
			self.assertEqual(ROLES['user'], response.json['role'])

	def test_create_user_manager_by_none(self):
		with app.app_context():
			payload = json.dumps({
				"username": "test",
				"password": "test",
				"role": ROLES['user_manager']
				})

			response = self.app.post('/api/users', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(403, response.status_code)

	def test_create_user_manager_by_admin(self):
		with app.app_context():
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
				"username": "test",
				"password": "test",
				"role": ROLES['user_manager']
				})

			response = self.app.post('/api/users', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertEqual("test", response.json['username'])
			self.assertEqual(ROLES['user_manager'], response.json['role'])
			self.assertTrue('password' not in response.json)
			self.assertIsNotNone(response.json['id'])

	def test_create_user_manager_by_user_manager(self):
		with app.app_context():
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
				"username": "test",
				"password": "test",
				"role": ROLES['user_manager']
				})

			response = self.app.post('/api/users', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertEqual("test", response.json['username'])
			self.assertEqual(ROLES['user_manager'], response.json['role'])
			self.assertTrue('password' not in response.json)
			self.assertIsNotNone(response.json['id'])

	def test_create_admin_by_user_manager(self):
		with app.app_context():
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
				"username": "test",
				"password": "test",
				"role": ROLES['admin']
				})

			response = self.app.post('/api/users', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(403, response.status_code)