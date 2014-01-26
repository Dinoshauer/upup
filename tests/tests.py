from unittest import TestCase
import json
from datetime import datetime
from redis import Redis
import app

class UpUpTestAppConfigInTesting(TestCase):
	def setUp(self):
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()

	def testConfig(self):
		assert self.app.config['TESTING']
		assert self.app.config['REDIS_DB'] is 1
		assert isinstance(self.app.config['REDIS_DB'], int)
		assert isinstance(self.app.config['REDIS_HOST'], str)
		assert isinstance(self.app.config['REDIS_PORT'], int)

# class UpUpTestAppConfigInProduction(TestCase):
# 	def setUp(self):
# 		self.app = app.app.test_client()

# 	def testConfig(self):
# 		assert not app.config['TESTING']
# 		assert isinstance(app.config['REDIS_DB'], int)
# 		assert isinstance(app.config['REDIS_HOST'], str)
# 		assert isinstance(app.config['REDIS_PORT'], int)

class UpUpTestGettingAllSitesNotFound(TestCase):
	def setUp(self):
		Redis().flushall()
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()

	def testGetAllNotFound(self):
		response = self.app.get('api/v1/jobs')
		r = json.loads(response.data)
		assert not r['result']
		assert 'Site not found' in r['error']
		assert response.status_code == 404

class UpUpTestGettingAllSites(TestCase):
	def setUp(self):
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()
		data = {'method': 'GET', 'title': 'test-site-1', 'url': '127.0.0.1', 'interval': 80}
		response = self.app.post('/api/v1/jobs', data=data)
		self.response_data = json.loads(response.data)['data']
		assert response.status_code == 201

	def tearDown(self):
		response = self.app.delete('/api/v1/jobs/{}'.format(self.response_data['id']))
		assert 'Site deleted.' in json.loads(response.data)['message']
		assert response.status_code == 200

	def testGetAll(self):
		response = self.app.get('/api/v1/jobs')
		assert isinstance(json.loads(response.data), dict)
		assert response.status_code == 200

class UpUpTestGetOneSite(TestCase):
	def setUp(self):
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()
		data = {'method': 'GET', 'title': 'test-site-1', 'url': '127.0.0.1', 'interval': 80}
		response = self.app.post('/api/v1/jobs', data=data)
		self.response_data = json.loads(response.data)['data']
		assert response.status_code == 201

	def tearDown(self):
		response = self.app.delete('/api/v1/jobs/{}'.format(self.response_data['id']))
		assert 'Site deleted.' in json.loads(response.data)['message']
		assert response.status_code == 200

	def testResponse(self):
		response = self.app.get('/api/v1/jobs/{}'.format(self.response_data['id']))
		r = json.loads(response.data)
		assert 'Site found.' in r['message']
		assert r['result']
		assert response.status_code == 200

		assert 'test-site-1' in r['data']['title']
		assert '127.0.0.1' in r['data']['url']
		assert '80' in r['data']['interval']
		assert isinstance(int(r['data']['interval']), int)
		assert 'site:' in r['data']['id']
		assert 'True' in r['data']['active']
		assert 'GET' in r['data']['method']
		assert isinstance(datetime.strptime(r['data']['added'], '%Y-%m-%d %H:%M:%S.%f'), datetime)

	def testReadNotFound(self):
		response = self.app.get('api/v1/jobs/this-is-invalid')
		r = json.loads(response.data)
		assert not r['result']
		assert 'Site not found' in r['error']
		assert response.status_code == 404

class UpUpTestCreateSite(TestCase):
	def setUp(self):
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()
		data = {'method': 'GET', 'title': 'test-site-1', 'url': '127.0.0.1', 'interval': 80}
		response = self.app.post('/api/v1/jobs', data=data)
		self.response_data = json.loads(response.data)['data']
		assert response.status_code == 201

	def tearDown(self):
		response = self.app.delete('/api/v1/jobs/{}'.format(self.response_data['id']))
		assert 'Site deleted.' in json.loads(response.data)['message']
		assert response.status_code == 200

	def testResponse(self):
		r = self.response_data
		assert 'test-site-1' in r['title']
		assert '127.0.0.1' in r['url']
		assert '80' in r['interval']
		assert isinstance(int(r['interval']), int)
		assert 'site:' in r['id']
		assert 'True' in r['active']
		assert 'GET' in r['method']
		assert isinstance(datetime.strptime(r['added'], '%Y-%m-%d %H:%M:%S.%f'), datetime)

	def testMissingKey(self):
		data = {'method': 'GET', 'title': 'test-site-1', 'interval': 80}
		response = self.app.post('/api/v1/jobs', data=data)
		response_data = json.loads(response.data)
		assert response.status_code == 400
		assert not response_data['result']
		assert 'Missing parameter' in response_data['error']

class UpUpTestDeleteSite(TestCase):
	def setUp(self):
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()
		data = {'method': 'GET', 'title': 'test-site-1', 'url': '127.0.0.1', 'interval': 80}
		response = self.app.post('/api/v1/jobs', data=data)
		self.response_data = json.loads(response.data)['data']
		assert response.status_code == 201

	def testDeleteSite(self):
		response = self.app.delete('/api/v1/jobs/{}'.format(self.response_data['id']))
		assert 'Site deleted.' in json.loads(response.data)['message']
		assert response.status_code == 200

	def testDeleteNotFound(self):
		response = self.app.get('api/v1/jobs/this-is-invalid')
		r = json.loads(response.data)
		assert not r['result']
		assert 'Site not found' in r['error']
		assert response.status_code == 404

class UpUpTestUpdateSite(TestCase):
	def setUp(self):
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()
		self.data = {'method': 'GET', 'title': 'test-site-1', 'url': '127.0.0.1', 'interval': 80}
		response = self.app.post('/api/v1/jobs', data=self.data)
		self.response_data = json.loads(response.data)['data']
		assert response.status_code == 201

	def tearDown(self):
		response = self.app.delete('/api/v1/jobs/{}'.format(self.response_data['id']))
		assert 'Site deleted.' in json.loads(response.data)['message']
		assert response.status_code == 200

	def testResponse(self):
		self.data['interval'] = 1000
		response = self.app.put('/api/v1/jobs/{}'.format(self.response_data['id']), data=self.data)
		r = json.loads(response.data)
		assert 'Site updated.' in r['message']
		assert r['result']
		assert response.status_code == 200

		assert '1000' in r['data']['interval']
		assert isinstance(int(r['data']['interval']), int)

	def testUpdateNotFound(self):
		response = self.app.put('api/v1/jobs/this-is-invalid', data=self.data)
		r = json.loads(response.data)
		assert not r['result']
		assert 'Site not found' in r['error']
		assert response.status_code == 404

	def testMissingKey(self):
		data = {'method': 'GET', 'title': 'test-site-1', 'interval': 80}
		response = self.app.put('/api/v1/jobs/{}'.format(self.response_data['id']), data=data)
		response_data = json.loads(response.data)
		assert response.status_code == 400
		assert not response_data['result']
		assert 'Missing parameter' in response_data['error']
