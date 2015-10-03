from sample import db
from flask.ext.sqlalchemy import sqlalchemy
from sqlalchemy.orm import relationship, backref
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    friends = db.Column(db.String, nullable=False)
    fbuserid = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False)
    token = db.Column(db.String, nullable=False)

    def __init__(self,fbuserid,name,friends):
        self.fbuserid = fbuserid
        self.name = name
        self.friends = friends

    def __repr__(self):
        return "username is '%s'" % (self.username)

    # def hash_password(self, password):
    #     self.password_hash = pwd_context.encrypt(password)

    # def verify_password(self, password):
    #     return pwd_context.verify(password, self.password_hash)


class Visited_logs(db.Model):
    __tablename__ = 'visited_logs'

    id = db.Column(db.Integer, primary_key=True)
    fbuserid = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    host = db.Column(db.String, nullable=False)
    # A python datetime object
    starttime = db.Column(db.DateTime, nullable=False)
    endtime = db.Column(db.DateTime, nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)

    # children = relationship('Comments')

    def __init__(self, userid, url, host, starttime, endtime, time_spent):
        self.fbuserid = userid
        self.url = url
        self.host = host
        self.starttime = starttime
        self.endtime = endtime
        self.time_spent = time_spent

    def __repr__(self):
        return "<Url is '%s'" % (self.url)


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    # site_id = db.Column(db.String, db.ForeignKey('visited_logs.id'))
    fbuserid = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    # the other columns are filled with data from the visited table
    url = db.Column(db.String, nullable=False)

    def __init__(self, userid, comment, time, url):
        # self.site_id = site_id
        self.fbuserid = userid
        self.comment = comment
        self.time = time
        self.url = url

    def __repr__(self):
        return "'%s' - '%s'" % (self.comment, self.userid)


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    senderid = db.Column(db.String, nullable=False)
    receiverid = db.Column(db.String, nullable=False)
    messageList = db.Column(db.String, nullable=False)
    seen = db.Column(db.Boolean, nullable=True)
    public = db.Column(db.Boolean, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __init__(self, url, senderid, receiverid, messageList, html, public, time):
        # self.site_id = site_id
        self.messageList = messageList
        self.senderid = senderid
        self.receiverid = receiverid
        self.public = public
        self.time = time
        self.url = url
        self.seen = False

    def __repr__(self):
        return "'%s' by '%s'" % (self.url,self.senderid)