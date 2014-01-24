from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import BadRequestKeyError
from crud import Crud

api = Blueprint('api', __name__, url_prefix='/api/v1',)

@api.route('/jobs', methods=['GET'])
def getAll():
	return Crud(current_app.config['REDIS_HOST'], current_app.config['REDIS_PORT'], current_app.config['REDIS_DB'], ).getAll()

@api.route('/jobs', methods=['POST'])
def create():
	try:
		site = {
			'method': request.form['method'],
			'interval': request.form['interval'],
			'title': request.form['title'],
			'url': request.form['url']
		}
		return Crud(current_app.config['REDIS_HOST'], current_app.config['REDIS_PORT'], current_app.config['REDIS_DB'], **site).create()
	except BadRequestKeyError, e:
		return jsonify({
			'result': False,
			'error': 'Missing parameter'
		}), e.code

@api.route('/jobs/<site_id>', methods=['GET'])
def read(site_id):
	return Crud(current_app.config['REDIS_HOST'], current_app.config['REDIS_PORT'], current_app.config['REDIS_DB'], id=site_id).read()

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
		return Crud(current_app.config['REDIS_HOST'], current_app.config['REDIS_PORT'], current_app.config['REDIS_DB'], **site).update()
	except BadRequestKeyError, e:
		return jsonify({
			'result': False,
			'error': 'Missing parameter'
		}), e.code

@api.route('/jobs/<site_id>', methods=['DELETE'])
def delete(site_id):
	return Crud(current_app.config['REDIS_HOST'], current_app.config['REDIS_PORT'], current_app.config['REDIS_DB'], id=site_id).delete()
