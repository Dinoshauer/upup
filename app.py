from flask import Flask

from api.v1.views import api

app = Flask(__name__)

app['REDIS_HOST'] = 'localhost'
app['REDIS_PORT'] = 6479
app['REDIS_DB'] = 0

app.register_blueprint(api)

if __name__ == '__main__':
	app.run(debug=True)
