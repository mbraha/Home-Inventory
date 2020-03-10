import os


class Config(object):
    '''
    Configuration of application, default is for DEVELOPMENT
    '''
    DEBUG = True

    # Set URI, the location of the app's database
    MONGO_URI = os.environ.get('DATABASE_URL') or \
        'mongodb://' + 'localhost:27017'

    # JWT, hopefully an easy way to do auth
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # Force JWT requests to be done through cookies
    JWT_TOKEN_LOCATION = ['cookies']
    # Sent over Https if True
    JWT_COOKIE_SECURE = False
    # Max age
    JWT_SESSION_COOKIE = 60 * 60 * 24 * 1