import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class DeleteRecordsTest(BaseCase):

# /records/all
	def test_delete_records_all_by_none(self):
		with app.app_context():
			response = self.app.delete('/records/all')
			self.assertEqual(401, response.status_code)

	def test_delete_records_all_by_user(self):
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

			response = self.app.delete('/records/all', headers={"Authorization":authorization})
			self.assertEqual(403, response.status_code)

	def test_delete_records_by_admin(self):
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

			response = self.app.delete('/records/all', headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['count'])

# /records
	def test_delete_records_by_user(self):
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

			response = self.app.delete('/records', headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['count'])

			response = self.app.get('/records', headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(0, response.json['_meta']['total_items'])

	def test_delete_records_by_none(self):
		with app.app_context():
			response = self.app.delete('/records')
			self.assertEqual(401, response.status_code)

# /records/<id>
	def test_delete_records_id_by_user(self):
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

			response = self.app.delete('/records/%d' %record_id, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(record_id, response.json['id'])

			response = self.app.get('/records/%d' %record_id, headers={"Authorization":authorization})
			self.assertEqual(404, response.status_code)

			response = self.app.delete('/records/%d' %admin_record_id, headers={"Authorization":authorization})
			self.assertEqual(404, response.status_code)

	def test_delete_records_id_by_admin(self):
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

			user_record_id = int(response.json['id'])

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

			response = self.app.delete('/records/%d' %record_id, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(record_id, response.json['id'])

			response = self.app.delete('/records/%d' %user_record_id, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_record_id, response.json['id'])

			response = self.app.get('/records/all', headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(0, response.json['_meta']['total_items'])

