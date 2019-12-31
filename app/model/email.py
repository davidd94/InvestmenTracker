from flask_mail import Message, Mail
from flask import current_app

from app.threads import async_task
from app import mail


@async_task
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(sub, sender, recipient, token, app=None):
    msg = Message(subject=sub,
                    sender=sender,
                    recipients=[recipient])
    
    cur_app = app if app else current_app

    url_domain = ''
    try:
        url_domain = 'https://investmentracker.info/confirm_email' if cur_app.config['TESTING'] is False else 'http://localhost:5000/confirm_email'
    except:
        url_domain = 'http://localhost:5000/confirm_email'

    msg.html = """
    <br>
    <br>
    You have requested a new email confirmation link. It will expire in three (3) days.
    <br>
    <br>
    Please follow this new link to activate your account: <a href="%s/%s">Click here to confirm your account</a></p>""" % (url_domain, token)
    
    send_async_email(cur_app, msg)