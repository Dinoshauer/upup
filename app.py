from flask import Flask

from api.v1.views import api

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == '__main__':
	app.run(debug=True)
