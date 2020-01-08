from app import create_app
from config import Config
from app.model.users import User
from app.model.recaptcha import google_recaptchaV2

from flask import Flask
from random import randint
from pymongo import MongoClient
import unittest, hashlib, os

client = MongoClient()

class TestConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://127.0.0.0:27017'

class UserDocModelCase(unittest.TestCase):
    def setUp(self):
        print('setting up user doc test...')
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.db = client.InvestmenTracker['test_users']
        self.test_users = [
            {'username': 'Daviepoo', 'firstname': 'Davie', 'lastname': 'poo', 'email': 'random1@gg.com', 'password': 'pass1'},
            {'username': 'Bert', 'firstname': 'Gilbert', 'lastname': 'Quemuel', 'email': 'random2@gg.com', 'password': 'pass2'},
            {'username': 'Wambulance', 'firstname': 'Dennis', 'lastname': 'Menace', 'email': 'random3@gg.com', 'password': 'pass3'}
            ]
        self.app_context.push()
        User.connect(True)
    
    def tearDown(self):
        print('tearing down tests...')
        self.db.drop()
        self.app_context.pop()
        User.disconnect()

    def create_user(self):
        hash_password = User.hash_password(self.test_users[0]['password'])
        new_user = new_user = User(username=self.test_users[0]['username'],
                            firstname=self.test_users[0]['firstname'],
                            lastname=self.test_users[0]['lastname'],
                            email=self.test_users[0]['email'],
                            password=hash_password)
        
        new_user.switch_collection('test_users')
        new_user.save()

        return new_user

    def create_random_user(self):
        user_number = len(self.test_users) - 1
        hash_password = User.hash_password(self.test_users[randint(0, user_number)]['password'])

        new_random_user = User(username=self.test_users[randint(0, user_number)]['username'],
                        firstname=self.test_users[randint(0, user_number)]['firstname'],
                        lastname=self.test_users[randint(0, user_number)]['lastname'],
                        email=self.test_users[randint(0, user_number)]['email'],
                        password=hash_password)
        
        new_random_user.switch_collection('test_users')
        new_random_user.save()

        return new_random_user

    def test_create_user(self):
        # instantiate user
        new_user = self.create_user()
        # search for newly added user
        found_user = self.db.find_one_and_delete({'username': new_user.username})
        # test
        self.assertEqual(found_user['username'], new_user.username)

        # instantiate random user
        new_random_user = self.create_random_user()
        # search for newly added random user
        found_random_user = self.db.find_one({'username': new_random_user.username})
        # test
        self.assertEqual(found_random_user['username'], new_random_user.username)

    def test_update_user(self):
        new_user = self.create_user()
        
        found_user = self.db.find_one({'username': new_user.username})
        updated_user = None
        old_username = None
        updated_username = 'N/A'
        
        if found_user:
            old_username = found_user['username']
            new_user.update(username='testingNewUsername')
            new_user.reload()
            updated_username = new_user.username
            updated_user = self.db.find_one({'username': new_user.username})
        
        self.assertNotEqual(old_username, updated_username)
        self.assertIsNotNone(updated_user)

    def test_hash_pass(self):
        password1 = self.test_users[0]['password']
        password2 = self.test_users[0]['password']

        hash_pass1 = User.hash_password(password1, algorithm='sha256')
        hash_pass2 = User.hash_password(password2, algorithm='sha256')

        salt = os.environ.get('SECRET_KEY') or 'non-secret-key-for-testing'
        check_hash_pass1 = hashlib.sha256((salt + password1).encode('utf-8')).hexdigest()
        check_hash_pass2 = hashlib.sha256((salt + password2).encode('utf-8')).hexdigest()
        
        self.assertEqual(hash_pass1, check_hash_pass1)
        self.assertEqual(hash_pass2, check_hash_pass2)
        

if __name__ == '__main__':
    unittest.main(verbosity=2)