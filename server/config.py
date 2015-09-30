class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = '\tq\xe2\xed\xce\xe7\xaclh{[\xdc\x8c\x01d\xd9\xa5\xe8\x93\xed\xed\xfb\xce\x12'
	SQLALCHEMY_DATABASE_URI = 'sqlite://data.db'

class DevelopmentConfig(BaseConfig):
	DEBUG = True
