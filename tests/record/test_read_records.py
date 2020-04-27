import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class ReadRecordsTest(BaseCase):

# /records/all
	def test_read_records_all_by_none(self):
		with app.app_context():
			response = self.app.get('/records/all')
			self.assertEqual(401, response.status_code)

	def test_read_records_all_by_user(self):
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

			response = self.app.get('/records/all', headers={"Authorization":authorization})
			self.assertEqual(403, response.status_code)

# RECORDS_PER_PAGE = 2
	def test_pagination_default_read_records_by_admin(self):
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
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)			

			response = self.app.get('/records/all', headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['_meta']['total_items'])

# RECORDS_PER_PAGE = 2
	def test_pagination_read_records_by_admin(self):
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

			payload = json.dumps({
				"date": "2020-01-02",
				"distance": 100,
				"time": 3600,
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
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)			

			response = self.app.get('/records/all', headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['_meta']['total_items'])
			self.assertTrue(response.json['items'][0]['date'] >= response.json['items'][1]['date'])
			self.assertTrue('next_page' in response.json)
			self.assertTrue('prev_page' not in response.json)
			page = int(response.json['next_page'])

			response = self.app.get('/records/all?page=%d' %page, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['_meta']['total_items'])
			self.assertTrue('next_page' not in response.json)
			self.assertTrue('prev_page' in response.json)
			self.assertEqual(1, response.json['prev_page'])

			page += 1
			response = self.app.get('/records/all?page=%d' %page, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(0, response.json['_meta']['total_items'])

# /records
	def test_read_records_by_user(self):
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
				"time": 3600,
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
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)		
			record_1_id = response.json['id']	

			payload = json.dumps({
				"date": "2020-01-02",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)		
			record_2_id = response.json['id']

			payload = json.dumps({
				"date": "2020-01-01",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)		
			record_3_id = response.json['id']	

			response = self.app.get('/records', headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['_meta']['total_items'])
			self.assertEqual(record_2_id, response.json['items'][0]['id'])
			self.assertEqual(record_1_id, response.json['items'][1]['id'])
			self.assertTrue('next_page' in response.json)
			page = response.json['next_page']

			response = self.app.get('/records?page=%d' %page, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['_meta']['total_items'])
			self.assertEqual(record_3_id, response.json['items'][0]['id'])
			self.assertTrue('next_page' not in response.json)

			page += 1
			response = self.app.get('/records?page=%d' %page, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(0, response.json['_meta']['total_items'])

	def test_read_records_by_none(self):
		with app.app_context():
			response = self.app.get('/records')
			self.assertEqual(401, response.status_code)

# /records/<id>
	def test_read_records_id_by_user(self):
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
				"time": 3600,
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
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)			
			self.assertIsNotNone(response.json['id'])
			record_id = int(response.json['id'])

			response = self.app.get('/records/%d' %record_id, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(record_id, response.json['id'])

			response = self.app.get('/records/%d' %admin_record_id, headers={"Authorization":authorization})
			self.assertEqual(404, response.status_code)

	def test_read_records_id_by_admin(self):
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
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)			
			self.assertIsNotNone(response.json['id'])
			record_id = int(response.json['id'])

			response = self.app.get('/records/%d' %record_id, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(record_id, response.json['id'])

			response = self.app.get('/records/%d' %user_record_id, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_record_id, response.json['id'])

	def test_read_filtered_records_by_admin(self):
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
				"date": "2020-04-24",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['id'])

			record_id_24 = int(response.json['id'])

			payload = json.dumps({
				"date": "2020-04-25",
				"distance": 1500,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['id'])

			record_id_25 = int(response.json['id'])

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
				"date": "2020-04-01",
				"distance": 1000,
				"time": 5000,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)			
			self.assertIsNotNone(response.json['id'])
			admin_record_id = int(response.json['id'])

			q = "(time>=5000 or (date>'2020-04-01' and distance>=1500))"
			response = self.app.get('/records/all?filter=%s' %q, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['_meta']['total_items'])
			self.assertEqual(record_id_25, response.json['items'][0]['id'])
			self.assertEqual(admin_record_id, response.json['items'][1]['id'])
			self.assertTrue('next_page' not in response.json)
			self.assertTrue('prev_page' not in response.json)


	def test_read_filtered_records_by_user(self):
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
				"date": "2020-04-01",
				"distance": 1000,
				"time": 5000,
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
				"date": "2020-04-24",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['id'])

			record_id_24 = int(response.json['id'])

			payload = json.dumps({
				"date": "2020-04-25",
				"distance": 1500,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['id'])

			record_id_25 = int(response.json['id'])

			q = "(time>5000 or (date>'2020-04-01' and distance!=1500))"
			response = self.app.get('/records?filter=%s' %q, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['_meta']['total_items'])
			self.assertEqual(record_id_24, response.json['items'][0]['id'])
			self.assertTrue('next_page' not in response.json)
			self.assertTrue('prev_page' not in response.json)

	def test_pagination_read_filtered_records_by_admin(self):
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
				"date": "2020-04-24",
				"distance": 1000,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['id'])

			record_id_24 = int(response.json['id'])

			payload = json.dumps({
				"date": "2020-04-25",
				"distance": 1500,
				"time": 3600,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['id'])

			record_id_25 = int(response.json['id'])

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
				"date": "2020-04-01",
				"distance": 1000,
				"time": 5000,
				"latitude": 51.5,
				"longitude": 0.127
				})

			response = self.app.post('/records', headers={"Content-Type": "application/json", "Authorization":authorization}, data=payload)
			self.assertEqual(201, response.status_code)			
			self.assertIsNotNone(response.json['id'])
			admin_record_id = int(response.json['id'])

			q = "time=5000 or date>'2020-04-01' or distance<1500"
			response = self.app.get('/records/all?filter=%s&page=1' %q, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['_meta']['total_items'])
			self.assertEqual(record_id_25, response.json['items'][0]['id'])
			self.assertEqual(record_id_24, response.json['items'][1]['id'])
			self.assertEqual(2, response.json['next_page'])
			self.assertTrue('prev_page' not in response.json)

			q = "time=5000 or date>'2020-04-01' or distance<1500"
			response = self.app.get('/records/all?filter=%s&page=2' %q, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['_meta']['total_items'])
			self.assertEqual(admin_record_id, response.json['items'][0]['id'])
			self.assertTrue('next_page' not in response.json)
			self.assertEqual(1, response.json['prev_page'])
