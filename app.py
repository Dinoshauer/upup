from flask import Flask
from api.v1.views import api

app = Flask(__name__)

app.config['TESTING'] = False

app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379
if app.config['TESTING']:
	app.config['REDIS_DB'] = 1
else:
	app.config['REDIS_DB'] = 0

app.register_blueprint(api)

if __name__ == '__main__':
	app.run()  # pragma: no cover
