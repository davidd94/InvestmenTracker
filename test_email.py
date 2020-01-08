from app import create_app, mail
from config import Config
from app.model.users import User
from app.model.email import send_email

from flask import Flask
from flask_mail import Message
import unittest, os


class TestConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://127.0.0.0:27017'

class EmailModelCase(unittest.TestCase):
    def setUp(self):
        print('setting up email test...')
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.test_users = [
            {'username': 'Daviepoo', 'firstname': 'Davie', 'lastname': 'poo', 'email': 'random1@gg.com', 'password': 'pass1'},
            {'username': 'Bert', 'firstname': 'Gilbert', 'lastname': 'Quemuel', 'email': 'random2@gg.com', 'password': 'pass2'},
            {'username': 'Wambulance', 'firstname': 'Dennis', 'lastname': 'Menace', 'email': 'random3@gg.com', 'password': 'pass3'}
            ]
        self.app_context.push()
    
    def tearDown(self):
        print('tearing down tests...')
        self.app_context.pop()

    def test_send_email(self):
        subject1 = 'Unit testing email func'
        subject2 = 'Unit testing built-in func'
        sender = self.app.config['MAIL_USERNAME']
        recipient = self.app.config['MAIL_USERNAME']
        acct_type = 'acct_new'
        test_token = 'this-is-just-a-test-token-for-unittest'

        with mail.record_messages() as outbox:
            # test imported send async email func
            send_email(sub=subject1,
                        sender=sender,
                        recipient=recipient,
                        email_type=acct_type, 
                        token=test_token,
                        app=self.app)

            # test lib built-in func
            mail.send_message(subject=subject2,
                                sender=sender,
                                body='test body text',
                                recipients=[recipient])
            
            self.assertEqual(len(outbox), 2)
            self.assertEqual(outbox[0].subject, subject1)
            self.assertEqual(outbox[1].subject, subject2)


if __name__ == '__main__':
    unittest.main(verbosity=2)