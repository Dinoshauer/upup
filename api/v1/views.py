from flask import Blueprint
from crud import Crud

api = Blueprint('api', __name__, url_prefix='/api/v1',)

@api.route('/jobs', methods=['GET'])
def getAll():
	return Crud().getAll()

@api.route('/jobs', methods=['POST'])
def create():
	return Crud(something='foo').create()

@api.route('/jobs/<site_id>', methods=['GET'])
def read(site_id):
	return Crud(id=site_id).read()

@api.route('/jobs/<site_id>', methods=['PUT'])
def update(site_id):
	return Crud(id=site_id, something_else='bar', something='baz').update()

@api.route('/jobs/<site_id>', methods=['DELETE'])
def delete(site_id):
	return Crud(id=site_id).delete()
