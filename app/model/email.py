from flask_mail import Message, Mail
from flask import current_app, render_template, session

from app.threads import async_task
from app import mail


@async_task
def __send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(sub, sender, recipient, email_type, token=None, app=None, **kwargs):
    msg = Message(subject=sub,
                    sender=sender,
                    recipients=[recipient])
    
    """ current_app is a proxy app...
    to get the actual app object, you MUST USE _get_current_object() """
    cur_app = app if app else current_app._get_current_object()
    email_html = email_type or None
    user = session if cur_app is current_app else None
    url_domain = 'https://investmentracker.info/confirm_email' if cur_app.config['TESTING'] is False \
                                                                else 'http://localhost:5000/confirm_email'
    
    if email_type is 'acct_new':
        email_html = 'emails/acct_new.html'
        msg.html = render_template(email_html, user=user, url_domain=url_domain, token=token)
    elif email_type is 'acct_confirm':
        email_html = 'emails/acct_confirm.html'
        msg.html = render_template(email_html, user=user, url_domain=url_domain, token=token)
    elif email_type is 'pass_recovery':
        email_html = 'emails/pass_recovery.html'
        msg.html = render_template(email_html, user=user, url_domain=url_domain, token=token)
    elif email_type is 'feedback':
        email_html = 'emails/feedback.html'
        msg.html = render_template(email_html, user=kwargs)
    else:
        email_html = 'emails/default.html'
        msg.html = render_template(email_html)
    
    __send_async_email(cur_app, msg)