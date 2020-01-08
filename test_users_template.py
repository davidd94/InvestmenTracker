from app import create_app
from config import Config
from app.model.users import UserCustom

from flask import Flask
from pymongo import MongoClient
import unittest

client = MongoClient()

class TestConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://127.0.0.0:27017'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        print('setting up user test...')
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.db = client.InvestmenTracker['Users']
        self.test_users = ['Davie poo', 'Dennis Afk', 'Gilbert Desmond']
        self.app_context.push()
    
    def tearDown(self):
        print('tearing down tests...')
        self.db.drop()
        self.app_context.pop()

    def test_create_user(self):
        # instantiate users
        new_user1 = User(self.test_users[0], True)
        new_user2 = User(self.test_users[1], True)

        # add users to mongoDB
        new_user1.add_user()
        new_user2.add_user()
        
        self.assertEqual(new_user1.get_self()['Username'], new_user1.username)
        self.assertEqual(new_user2.get_self()['Username'], new_user2.username)

    def test_remove_user(self):
        user = User(self.test_users[0], True)
        user.add_user()
        removed_user = user.remove_user()
        
        self.assertTrue(removed_user)
    
    def test_update_user(self):
        user = User(self.test_users[0], True)
        user.add_user()
        old_username = user.username
        updated_user = user.update_user('New Name')
        check_olduser = User.get_user(old_username, True)

        self.assertTrue(updated_user)
        self.assertTrue(user.get_self())
        self.assertNotEqual(check_olduser, updated_user)


if __name__ == '__main__':
    unittest.main(verbosity=2)