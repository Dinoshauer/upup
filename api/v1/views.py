from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequestKeyError
from crud import Crud

api = Blueprint('api', __name__, url_prefix='/api/v1',)

@api.route('/jobs', methods=['GET'])
def getAll():
	return Crud().getAll()

@api.route('/jobs', methods=['POST'])
def create():
	try:
		site = {
			'method': request.form['method'],
			'interval': request.form['interval'],
			'title': request.form['title'],
			'url': request.form['url']
		}
		return Crud(**site).create()
	except BadRequestKeyError, e:
		return jsonify({
			'result': False,
			'error': 'Missing parameter'
		}), e.code

@api.route('/jobs/<site_id>', methods=['GET'])
def read(site_id):
	return Crud(id=site_id).read()

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
		return Crud(**site).update()
	except BadRequestKeyError, e:
		return jsonify({
			'result': False,
			'error': 'Missing parameter'
		}), e.code

@api.route('/jobs/<site_id>', methods=['DELETE'])
def delete(site_id):
	return Crud(id=site_id).delete()
