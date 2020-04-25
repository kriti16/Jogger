import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class putRecordsTest(BaseCase):

	def test_put_records_id_by_user(self):
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
				"time": "11:30:00",
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)			
			self.assertIsNotNone(response.json['id'])
			record_id = int(response.json['id'])

			payload = json.dumps({
				"date": "2020-01-20",
				"distance": 100
				})			

			response = self.app.put('/records/%d' %record_id, headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(200, response.status_code)
			self.assertEqual(record_id, response.json['id'])
			self.assertEqual(100, response.json['distance'])
			self.assertEqual("2020-01-20", response.json['date'])
			self.assertIsNotNone(response.json['weather'])

	def test_put_admin_records_id_by_user(self):
		with app.app_context():
			BaseCase.add_admin(self)
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
				"time": "11:30:00",
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['id'])

			admin_record_id = int(response.json['id'])

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
				"date": "2020-01-20",
				"distance": 100
				})	

			response = self.app.put('/records/%d' %admin_record_id, headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(404, response.status_code)

	def test_put_user_id_of_record_by_user(self):
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
				"time": "11:30:00",
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)			
			self.assertIsNotNone(response.json['id'])
			record_id = int(response.json['id'])

			payload = json.dumps({
				"date": "2020-01-20",
				"distance": 100,
				"user_id": user_id+1
				})			

			response = self.app.put('/records/%d' %record_id, headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(403, response.status_code)

	def test_put_user_id_of_record_by_admin(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = self.get_user_id('user')

			BaseCase.add_admin(self)
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
				"time": "11:30:00",
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['id'])

			record_id = int(response.json['id'])

			payload = json.dumps({
				"user_id": user_id
				})	

			response = self.app.put('/records/%d' %record_id, headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_id, response.json['user_id'])

	def test_put_wrong_user_id_of_record_by_admin(self):
		with app.app_context():
			BaseCase.add_admin(self)
			admin_id = BaseCase.get_user_id(self, 'admin')
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
				"time": "11:30:00",
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['id'])

			record_id = int(response.json['id'])

			payload = json.dumps({
				"user_id": admin_id + 1
				})	

			response = self.app.put('/records/%d' %record_id, headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(404, response.status_code)