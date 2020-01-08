from flask import session, current_app, render_template, request
from app.model.email import send_email
from app.model.feedback import FeedbackModel
from app.model.recaptcha import google_recaptchaV2
from app.view import bp
import json, requests, os


@bp.route("/")
def homepage():
    if ('username' in session) and ('firstname' in session):
        return render_template('InvestmenTracker-homepage.html', title=session['username'], name=session['firstname'])
    else:
        return render_template('InvestmenTracker-homepage.html')

@bp.route("/userportfolio")
def userportfolio():
    if 'username' in session:
        return render_template('InvestmenTracker-userportfolio.html', title=session['username'])
    else:
        return redirect('/')

@bp.route("/financialnews")
def financials():
    if 'username' in session:
        return render_template('InvestmenTracker-news.html', title=session['username'], username=session['firstname'])
    else:
        return render_template('InvestmenTracker-news.html')

@bp.route("/educationaltools")
def edutools():
    if 'username' in session:
        return render_template('InvestmenTracker-educationaltools.html', title=session['username'], username=session['firstname'])
    else:
        return render_template('InvestmenTracker-educationaltools.html')

@bp.route("/aboutme")
def aboutme():
    if 'username' in session:
        return render_template('InvestmenTracker-aboutme.html', title=session['username'])
    else:
        return render_template('InvestmenTracker-aboutme.html')

@bp.route("/contactme")
def contact():
    if 'username' in session:
        return render_template('InvestmenTracker-contact.html', title=session['username'], username=session['firstname'], useremail=session['email'])
    else:
        return render_template('InvestmenTracker-contact.html')

@bp.route("/sendfeedback", methods=['POST'])
def feedback():
    feedbackname = request.json['FirstName']
    feedbackemail = request.json['Email']
    feedbackcomment = request.json['Feedback']
    recaptchadata = request.json['Recaptcha']
    google_response = google_recaptchaV2(recaptchadata)

    if (google_response['success'] == True):
        subject = f'InvestmenTracker Feedback from {feedbackname}'
        sender = current_app.config['MAIL_USERNAME']
        recipient = current_app.config['MAIL_USERNAME']
        
        # SAVE TO DB
        feedback_data = FeedbackModel(email=feedbackemail,
                                        firstname=feedbackname,
                                        feedback=feedbackcomment)
        
        validation_errors = feedback_data.validate_self()
        if validation_errors:
            return str(validation_errors)
        else:
            feedback_data.connect()
            feedback_data.save()
            send_email(subject, sender, recipient, 'feedback',
                        firstname=feedbackname,
                        email=feedbackemail,
                        feedback=feedbackcomment)
            
            return "Feedback Success"
    
    return "Feedback Failure"