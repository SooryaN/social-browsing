from flask import Flask, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

#Creating database object
db = SQLAlchemy(app)


@app.route('/visited', methods=['GET', 'POST'])
def visited():
	if request.method == 'GET':
		visited_url = request.args['page']


if __name__ == '__main__':
	app.run()