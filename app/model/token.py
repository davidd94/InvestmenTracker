from itsdangerous import TimedSerializer
from flask import current_app


def generate_token(unique_data, salt='default-salt'):
    s = TimedSerializer(current_app.config['SECRET_KEY'] if current_app else 'test-secret-salt')
    token = s.dumps(unique_data, salt=salt)
    return token

def verify_token(token, age=0, salt='default-salt'):
    s = TimedSerializer(current_app.config['SECRET_KEY'] if current_app else 'test-secret-salt')
    email = s.loads(token, salt=salt, max_age=age)
    return email