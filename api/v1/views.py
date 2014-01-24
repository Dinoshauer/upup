from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import BadRequestKeyError
from crud import Crud

_REDIS_HOST_ = current_app['REDIS_HOST']
_REDIS_PORT_ = current_app['REDIS_PORT']
_REDIS_DB_ = current_app['REDIS_DB']

api = Blueprint('api', __name__, url_prefix='/api/v1',)

@api.route('/jobs', methods=['GET'])
def getAll():
	return Crud(_REDIS_HOST_, _REDIS_PORT_, _REDIS_DB_, ).getAll()

@api.route('/jobs', methods=['POST'])
def create():
	try:
		site = {
			'method': request.form['method'],
			'interval': request.form['interval'],
			'title': request.form['title'],
			'url': request.form['url']
		}
		return Crud(_REDIS_HOST_, _REDIS_PORT_, _REDIS_DB_, **site).create()
	except BadRequestKeyError, e:
		return jsonify({
			'result': False,
			'error': 'Missing parameter'
		}), e.code

@api.route('/jobs/<site_id>', methods=['GET'])
def read(site_id):
	return Crud(_REDIS_HOST_, _REDIS_PORT_, _REDIS_DB_, id=site_id).read()

@api.route('/jobs/<site_id>', methods=['PUT'])
def update(site_id):
	try:
		site = {
			'id': site_id,
			'method': request.form['method'],
			'interval': request.form['interval'],
			'title': request.form['title'],
			'url': request.form['url']
		}
		return Crud(_REDIS_HOST_, _REDIS_PORT_, _REDIS_DB_, **site).update()
	except BadRequestKeyError, e:
		return jsonify({
			'result': False,
			'error': 'Missing parameter'
		}), e.code

@api.route('/jobs/<site_id>', methods=['DELETE'])
def delete(site_id):
	return Crud(_REDIS_HOST_, _REDIS_PORT_, _REDIS_DB_, id=site_id).delete()
