from pymongo import MongoClient
from flask_pymongo import PyMongo


class User:
    def __init__(self, username, test=False):
        self.user = username
        self.users = []
        self.test = test
        self.db = MongoClient().InvestmenTracker.test_users if test else \
                    PyMongo().InvestmenTracker.Users

    def get_user(self):
        return True if self.db.find_one({'Username': self.user}) else False

    def add_user(self):
        self.db.insert_one({'Username': self.user})
        
    def remove_user(self):
        pass