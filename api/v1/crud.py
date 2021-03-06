from datetime import datetime
from uuid import uuid4 as uuid
from redis import Redis
from flask import jsonify

class Crud():
	def __init__(self, _REDIS_HOST_, _REDIS_PORT_, _REDIS_DB_, **kwargs):
		self.r = Redis(host=_REDIS_HOST_, port=_REDIS_PORT_, db=_REDIS_DB_)
		self.NOT_FOUND = jsonify({
			'result': False,
			'error': 'Site not found'
		}), 404
		self.site = {
			'id': kwargs.get('id', 'site:%s' % uuid()),
			'method': kwargs.get('method', 'GET'),
			'title': kwargs.get('title'),
			'url': kwargs.get('url'),
			'interval': kwargs.get('interval', 60),
			'timeout': 60,
			'last_run': 'never',
			'added': kwargs.get('added', datetime.now()),
			'active': kwargs.get('active', True)
		}

	def getAll(self):
		keys = self.r.keys('site:*')
		if len(keys) > 0:
			result = [self.r.hgetall(key) for key in keys]
			return jsonify({
				'result': True,
				'message': 'Found %d site(s)' % len(result),
				'sites_found': len(result),
				'data': result
			}), 200
		return self.NOT_FOUND

	def create(self):
		for key, value in self.site.items():
			self.r.hsetnx(self.site['id'], key, value)
		return jsonify({
			'result': True,
			'message': 'Site created.',
			'data': self.r.hgetall(self.site['id'])
		}), 201

	def read(self):
		if self.r.exists(self.site['id']):
			return jsonify({
				'result': True,
				'message': 'Site found.',
				'data': self.r.hgetall(self.site['id'])
			}), 200
		return self.NOT_FOUND

	def update(self):
		if self.r.exists(self.site['id']):
			redis = self.r.hmset(self.site['id'], self.site)
			if redis:
				return jsonify({
					'result': redis,
					'message': 'Site updated.',
					'data': self.r.hgetall(self.site['id'])
				}), 200
			else:
				return self.NOT_FOUND
		return self.NOT_FOUND

	def delete(self):
		if self.r.exists(self.site['id']):
			if self.r.delete(self.site['id']):
				return jsonify({
					'result': True,
					'message': 'Site deleted.'
				}), 200
		return self.NOT_FOUND
