from flask import session, current_app
from app.view import bp


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
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = {'secret':'6LfoU3sUAAAAADg2saBK9l2otrKNNNKdCgqV32a9','response': recaptchadata}, timeout=10)
    google_response = json.loads(r.text)    #CONVERTS GOOGLE'S RESPONSE

    if (google_response['success'] == True):
        msg = Message(('InvestmenTracker Feedback from ' + feedbackname),
        sender='investmentracker1@gmail.com',
        recipients=['investmentracker1@gmail.com'])
        
        msg.body = """
        From: %s <%s>
        %s
        """ % (feedbackname, feedbackemail, feedbackcomment)

        mail.send(msg)

        return "Feedback Success"
    else:
        return "Feedback Failure"