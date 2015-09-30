from app import db

from flask.ext.sqlalchemy import sqlalchemy


class Visited(db.Model):
	__tablename__ = 'visited'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.String, nullable=False)
	url = db.Column(db.String, nullable=False)
	host = db.Column(db.String, nullable=False)
	#A python datetime object
	time = db.Column(db.DateTime, nullable=False)

	def __init__(self, userid, url, host, time):
		self.userid = userid
		self.url = url
		self.host = host
		self.time = time

	def __repr__(self):
		return "<Url is '%s'" % (self.url)

class Comments(db.Model):
	__tablename__ = 'comments'

	id = db.Column(db.Integer, primary_key=True)
	comment = db.Column(db.String, nullable=False)
	time = db.Column(db.DateTime, nullable=False)
	#the other columns are filled with data from the visited table
	url = db.Column(db.String, nullable=False)