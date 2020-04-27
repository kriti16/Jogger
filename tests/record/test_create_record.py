import json
import unittest

from app import app
from app.database.models import User, Record
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class CreateRecordTest(BaseCase):

	def test_create_record_by_none(self):
		with app.app_context():
			payload = json.dumps({
				"date": "2020-01-01",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(401, response.status_code)

	def test_create_record_by_user(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = self.get_user_id('user')
			payload = json.dumps({
				"username": "user",
				"password": "user"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			payload = json.dumps({
				"date": "2020-01-01",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertEqual("2020-01-01", response.json['date'])
			self.assertEqual(1000, response.json['distance'])
			self.assertEqual(3600, response.json['time'])
			self.assertEqual(51.5, response.json['latitude'])
			self.assertEqual(0.127, response.json['longitude'])
			self.assertEqual(user_id, response.json['user_id'])
			self.assertIsNotNone(response.json['id'])
			self.assertIsNotNone(response.json['weather'])

	def test_create_record_by_user_change_user_id(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = self.get_user_id('user')
			BaseCase.add_user_manager(self)
			manager_id = self.get_user_id('manager')
			payload = json.dumps({
				"username": "user",
				"password": "user"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			payload = json.dumps({
				"date": "2020-01-01",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127,
				"user_id": manager_id
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(403, response.status_code)	

	def test_create_record_by_admin_change_user_id(self):
		with app.app_context():
			BaseCase.add_admin(self)
			admin_id = self.get_user_id('admin')
			BaseCase.add_user_manager(self)
			manager_id = self.get_user_id('manager')
			payload = json.dumps({
				"username": "admin",
				"password": "admin"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			payload = json.dumps({
				"date": "2020-01-01",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127,
				"user_id": int(manager_id)
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertEqual("2020-01-01", response.json['date'])
			self.assertEqual(1000, response.json['distance'])
			self.assertEqual(3600, response.json['time'])
			self.assertEqual(51.5, response.json['latitude'])
			self.assertEqual(0.127, response.json['longitude'])
			self.assertEqual(manager_id, response.json['user_id'])
			self.assertIsNotNone(response.json['id'])
			self.assertIsNotNone(response.json['weather'])	

	def test_create_record_by_admin_change_wrong_user_id(self):
		with app.app_context():
			BaseCase.add_admin(self)
			admin_id = self.get_user_id('admin')
			payload = json.dumps({
				"username": "admin",
				"password": "admin"
				})

			response = self.app.post('/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			payload = json.dumps({
				"date": "2020-01-01",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127,
				"user_id": int(admin_id+1)
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(404, response.status_code)