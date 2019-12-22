from app import create_app
from config import Config
from app.model.users import User

from flask import Flask
from pymongo import MongoClient
import unittest

client = MongoClient()

class TestConfig(Config):
    TESTING = True
    MONGO_URI = 'http://localhost:27017'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        print('setting up user test...')
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.db = client.InvestmenTracker['test_users']
        self.test_users = ['Davie poo', 'Dennis Afk', 'Gilbert Desmond']
        self.app_context.push()
    
    def tearDown(self):
        print('tearing down tests...')
        self.db.test_users.drop()
        self.app_context.pop()

    def test_create_user(self):
        # instantiate users
        new_user1 = User(self.test_users[0], True)
        new_user2 = User(self.test_users[1], True)

        # add users to mongoDB
        new_user1.add_user()
        new_user2.add_user()

        # fetching saved user data from DB
        user1 = self.db.find_one({'Username': self.test_users[0]})
        user2 = self.db.find_one({'Username': self.test_users[1]})
        
        self.assertEqual(user1['Username'], new_user1.user)
        self.assertEqual(user2['Username'], new_user2.user)

    def test_remove_user(self):
        user = User(self.test_users[0], True)
        user.remove_user()
        check_user = user.get_user()

        self.assertTrue(check_user)
    

if __name__ == '__main__':
    unittest.main(verbosity=2)