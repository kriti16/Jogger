import json
import unittest

from app import app
from app.database.models import User
from app.api.roles import ROLES
from tests.base_case import BaseCase
from flask import jsonify

class ReadUsersTest(BaseCase):

	def test_read_all_users_by_none(self):
		with app.app_context():
			response = self.app.get('/api/users/all')
			self.assertEqual(400, response.status_code)

	def test_read_all_users_by_user(self):
		with app.app_context():
			BaseCase.add_user(self)
			payload = json.dumps({
				"username": "user",
				"password": "user"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.get('/api/users/all', headers={"Authorization":authorization})
			self.assertEqual(403, response.status_code)

	def test_read_all_users_by_user_manager(self):
		with app.app_context():
			BaseCase.add_user(self)
			BaseCase.add_user_manager(self)
			payload = json.dumps({
				"username": "manager",
				"password": "manager"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			response = self.app.get('/api/users/all', headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['_meta']['total_items'])

	def test_read_all_filtered_users_by_user_manager(self):
		with app.app_context():
			BaseCase.add_user(self)
			BaseCase.add_user_manager(self)
			payload = json.dumps({
				"username": "manager",
				"password": "manager"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			q = "role=1"
			response = self.app.get('/api/users/all?filter=%s' %q, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['_meta']['total_items'])

	def test_read_all_filtered_users_by_user_manager(self):
		with app.app_context():
			BaseCase.add_user(self)
			BaseCase.add_user_manager(self)
			BaseCase.add_admin(self)
			payload = json.dumps({
				"username": "manager",
				"password": "manager"
				})

			response = self.app.post('/api/auth', headers={"Content-Type": "application/json"}, data=payload)

			self.assertEqual(201, response.status_code)
			self.assertIsNotNone(response.json['access_token'])

			authorization = "Bearer "+ response.json['access_token']

			q = "role>0"
			response = self.app.get('/api/users/all?filter=%s' %q, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['_meta']['total_items'])

	def test_read_user_id_by_none(self):
		with app.app_context():
			BaseCase.add_user(self)
			response = self.app.get('/api/users/1')
			self.assertEqual(400, response.status_code)

	def test_read_user_id_by_user(self):
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

			response = self.app.get('/api/users/%d' %manager_id, headers={"Authorization":authorization})
			self.assertEqual(403, response.status_code)

	def test_read_user_id_self_by_user(self):
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

			response = self.app.get('/api/users/%d' %user_id, headers={"Authorization":authorization})
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_id, response.json['id'])
			self.assertEqual('user', response.json['username'])

	def test_read_user_id_by_user_manager(self):
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

			response = self.app.get('/api/users/%d' %user_id, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_id, response.json['id'])
			self.assertEqual('user', response.json['username'])

	def test_read_user_id_by_admin(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
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

			response = self.app.get('/api/users/%d' %user_id, headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(user_id, response.json['id'])
			self.assertEqual('user', response.json['username'])

			response = self.app.get('/api/users/%d' %manager_id, headers={"Authorization":authorization})

			self.assertEqual(200, response.status_code)
			self.assertEqual(manager_id, response.json['id'])
			self.assertEqual('manager', response.json['username'])

# POSTS_PER_PAGE = 2
	def test_pagination_read_all_users_by_admin(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
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

			response = self.app.get('/api/users/all?page=1', headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['_meta']['total_items'])
			self.assertEqual(1, response.json['_meta']['page'])
			self.assertEqual(2, response.json['_meta']['per_page'])
			self.assertEqual(2, response.json['_meta']['total_pages'])
			self.assertEqual('admin', response.json['items'][0]['username'])
			self.assertEqual('manager', response.json['items'][1]['username'])
			self.assertTrue('next_page' in response.json)
			self.assertTrue('prev_page' not in response.json)
			page = int(response.json['next_page'])

			response = self.app.get('/api/users/all?page=%d' %page, headers={"Authorization":authorization})

			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['_meta']['total_items'])
			self.assertEqual(2, response.json['_meta']['page'])
			self.assertEqual('user', response.json['items'][0]['username'])
			self.assertTrue('next_page' not in response.json)
			self.assertTrue('prev_page' in response.json)
			self.assertEqual(1, response.json['prev_page'])

			page += 1
			response = self.app.get('/api/users/all?page=%d' %page, headers={"Authorization":authorization})

			self.assertEqual(200, response.status_code)
			self.assertEqual(0, response.json['_meta']['total_items'])


	def test_pagination_read_all_filtered_users_by_admin(self):
		with app.app_context():
			BaseCase.add_user(self)
			user_id = BaseCase.get_user_id(self, 'user')
			
			payload = json.dumps({
				"username": "test2",
				"password": "test2",
				"email": "test2@example.com"
				})

			response = self.app.post('/api/users', headers={"Content-Type": "application/json"}, data=payload)
			self.assertEqual(201, response.status_code)

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

			response = self.app.get('/api/users/all?page=1', headers={"Authorization":authorization})
			
			self.assertEqual(200, response.status_code)
			self.assertEqual(2, response.json['_meta']['total_items'])
			self.assertEqual('admin', response.json['items'][0]['username'])
			self.assertEqual('manager', response.json['items'][1]['username'])
			self.assertTrue('next_page' in response.json)
			self.assertTrue('prev_page' not in response.json)

			q = "role!=2"
			response = self.app.get('/api/users/all?page=2&filter=%s' %q, headers={"Authorization":authorization})

			self.assertEqual(200, response.status_code)
			self.assertEqual(1, response.json['_meta']['total_items'])
			self.assertEqual('user', response.json['items'][0]['username'])
			self.assertTrue('next_page' not in response.json)
			self.assertTrue('prev_page' in response.json)
			self.assertEqual(1, response.json['prev_page'])

			page = 3
			response = self.app.get('/api/users/all?page=%d&filter=%s' %(page,q), headers={"Authorization":authorization})

			self.assertEqual(200, response.status_code)
			self.assertEqual(0, response.json['_meta']['total_items'])