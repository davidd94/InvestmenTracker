import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
    MONGO_URI = os.environ.get('MONGO_URI')

    RECAPTCHA_ENABLED = True
    RECAPTCHA_PUBLIC_KEY = '6LfoU3sUAAAAAGhGo6pBHk6kdmKb197mHdESWc6v'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'investmentracker1@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    