from app import create_app
from config import Config
from app.model.users import User

from flask import Flask
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
    
    def tearDown(self):
        print('tearing down tests...')
        self.db.drop()
        self.app_context.pop()

    def test_create_user(self):
        # setup user variables
        username1, email1, password1 = self.test_users[0]['username'], self.test_users[0]['email'], self.test_users[0]['password']
        firstname1, lastname1 = self.test_users[0]['firstname'], self.test_users[0]['lastname']
        
        username2, email2, password2 = self.test_users[1]['username'], self.test_users[1]['email'], self.test_users[1]['password']
        firstname2, lastname2 = self.test_users[1]['firstname'], self.test_users[1]['lastname']

        # instantiate users
        new_user1 = User(username=username1, firstname=firstname1, lastname=lastname1, email=email1, password=password1)
        new_user2 = User(username=username2, firstname=firstname2, lastname=lastname2, email=email2, password=password2)

        # connects to mongoDB
        User.connect(True)

        # add users to mongoDB
        new_user1.save()
        new_user2.save()

        # search for newly added users
        found_user1 = User.objects(username=username1).first()
        found_user2 = User.objects(username=username2).first()
        
        self.assertEqual(found_user1['username'], username1)
        self.assertEqual(found_user2['username'], username2)

    def test_update_user(self):
        new_user = User(username=self.test_users[0]['username'],
                        firstname=self.test_users[0]['firstname'],
                        lastname=self.test_users[0]['lastname'],
                        email=self.test_users[0]['email'],
                        password=self.test_users[0]['password'])
        User.connect(True)
        new_user.save()
        user = User.objects(username=self.test_users[0]['username']).first()
        updated_user = None
        old_username = None
        updated_username = 'N/A'
        
        if user:
            old_username = user['username']
            user.update(username='testingNewUsername')
            user.reload()
            updated_username = user['username']
            updated_user = User.objects(username=updated_username).first()
        self.assertNotEqual(old_username, updated_username)
        self.assertIsNotNone(updated_user)

    def test_hash_pass(self):
        password1 = self.test_users[0]['password']
        password2 = self.test_users[0]['password']

        hash_func = User.hash_password
        hash_pass1 = User.hash_password(password1, algorithm='sha256')
        hash_pass2 = User.hash_password(password2, algorithm='sha256')

        salt = os.environ.get('SECRET_KEY') or 'non-secret-key-for-testing'
        check_hash_pass1 = hashlib.sha256((salt + password1).encode('utf-8')).hexdigest()
        check_hash_pass2 = hashlib.sha256((salt + password2).encode('utf-8')).hexdigest()
        
        self.assertEqual(hash_pass1, check_hash_pass1)
        self.assertEqual(hash_pass2, check_hash_pass2)

    def test_user_login(self):
        # create new user
        hash_password = User.hash_password(self.test_users[0]['password'])
        updated_user = None
        #print(hash_password)
        new_user = User(username=self.test_users[0]['username'],
                        firstname=self.test_users[0]['firstname'],
                        lastname=self.test_users[0]['lastname'],
                        email=self.test_users[0]['email'],
                        password=hash_password)
        User.connect(True)
        new_user.save()

        # retreive user data for pass validation
        user = User.objects(username=self.test_users[0]['username']).first()
        user_hash_password = user['password']

        # unhash pass
        

        # test failed login attempts
        for i in range(0, 10):
            user['failed_login'] += 1
            user.save()
            updated_user = User.objects(username=user['username']).first()
            # checks for updated user data in DB
            self.assertLessEqual(updated_user['failed_login'], 10)
            # checks current user object data
            self.assertLessEqual(user['failed_login'], 10)
        
        # test acct confirmation status
        self.assertFalse(user['acct_status'])
        user['acct_status'] = True
        user.save()
        updated_user = User.objects(username=user['username']).first()
        self.assertTrue(user['acct_status'])
        self.assertTrue(updated_user['acct_status'])

        self.assertEqual(user_hash_password, hash_password)

    def test_user_confirmation(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)