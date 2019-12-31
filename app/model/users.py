from app import mongo
from pymongo import MongoClient
from mongoengine import Document, StringField, IntField, BooleanField, connect
import os, hashlib, string, random


class User(Document):
    def __init__(self, *args, **kwargs):
        self.salt = None
        super().__init__(*args, **kwargs)
        
    meta = {'collection': 'test_users'}
    username = StringField(required=True, max_length=30, unique=True)
    firstname = StringField(max_length=50)
    lastname = StringField(max_length=50)
    email = StringField(required=True, max_length=50, unique=True)
    password = StringField(required=True, max_length=200)
    failed_login = IntField(min_value=0, max_value=10, default=0)
    acct_status = BooleanField(default=False)
    token = StringField(default=None, max_length=200)

    @classmethod
    def connect(cls, test=False):
        if test is False:
            connect(os.environ.get('MONGO_URI'))
        else:
            connect('InvestmenTracker')
    
    @staticmethod
    def random_salt_generator(stringLength=10):
        """Generate a random string of letters, digits and special characters """

        string_parameters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(string_parameters) for i in range(stringLength))

    @staticmethod
    def hash_password(password, algorithm='sha256'):
        ALGORITHM_MD5 = "md5"
        ALGORITHM_SHA1 = "sha1"
        ALGORITHM_SHA256 = "sha256"
        ALGORITHM_SHA512 = "sha512"
        salt = os.environ.get('SECRET_KEY') or 'non-secret-key-for-testing'

        if algorithm == ALGORITHM_SHA1:
            return hashlib.sha1((salt + password).encode('utf-8')).hexdigest()
        elif algorithm == ALGORITHM_MD5:
            return hashlib.md5((salt + password).encode('utf-8')).hexdigest()
        elif algorithm == ALGORITHM_SHA256:
            return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        elif algorithm == ALGORITHM_SHA512:
            return hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
        raise ValueError('Unsupported hash type %s' % algorithm)
        

class UserCustom:
    def __init__(self, username, test=False):
        self.username = username
        #self.firstname = firstname
        #self.users = []
        self.test = test
        self.db = mongo.InvestmenTracker['Users'] if test is False else \
                    MongoClient().InvestmenTracker['test_users']

    def get_self(self):
        return self.db.find_one({'Username': self.username}) \
            if self.db.find_one({'Username': self.username}) \
            else False

    def add_user(self):
        if self.get_self() is False:
            return self.db.insert_one({'Username': self.username})
        else:
            return False
        
    def remove_user(self):
        if self.get_self():
            return self.db.find_one_and_delete({'Username': self.username})
        else:
            return False

    def update_user(self, username):
        if self.get_self():
            updated_user = self.db.find_one_and_update({'Username': self.username}, { '$set': {'Username': username} })
            self.username = username
            return updated_user
        else:
            return False
        
    @staticmethod
    def get_user(username, test=False):
        db = mongo.InvestmenTracker['Users'] if test is False else \
                    MongoClient().InvestmenTracker['test_users']
        return db.find_one({'Username': username}) \
                    if db.find_one({'Username': username}) \
                    else False

    user_prop = property(get_self, update_user, remove_user)