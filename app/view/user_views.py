from flask import session, current_app, redirect
from itsdangerous import URLSafeSerializer

from app.view.home_views import homepage
from app.controller import bp
from app.model.users import User
from app.model.email import send_email


@bp.route('/loginuser', methods=["POST"])
def userloggedin():
    if (request.method == "POST"):
        userloginname = request.json['loginusername']
        userloginpw = request.json['loginuserpw']
        User.connect()
        finduser = User.objects(username=userloginname).first()

        if (finduser):
            userpwchk = User.hash_password(userloginpw)

            if (userpwchk == finduser['password'] and finduser['failed_login'] < 10):
                if (finduser['acct_status'] == False):
                    return "Please confirm your account before logging in."
                session['username'] = finduser['username']
                session['firstname'] = finduser['firstname']
                session['lastname'] = finduser['lastname']
                session['email'] = finduser['email']
                finduser['failed_login'] = 0
                finduser.save()
                return jsonify("You have successfully logged in!")
            elif (userpwchk != finduser['password']):
                finduser['failed_login'] += 1
                finduser.save()
                if (finduser['failed_login'] == 10):
                    return "Exceeded failed login attempts!"
                return "Invalid username/password!"        

        return "Invalid username/password!"

@bp.route('/loggedout', methods=["POST"])
def userloggedout():
    session.pop('username', None)
    redirect('/')

@bp.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    user = User.objects(token=token).first()
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    if (user):
        try:
            email = s.loads(token, salt='email-confirm', max_age=259200)

            if (user['acct_status'] == False):
                user['acct_status'] = True
                user.save()
                return render_template('InvestmenTracker-emailconfirm.html', acct_status=user['acct_status'])
            else:
                return redirect('/')

        except Exception:
            if (user['acct_status'] == False):
                return render_template('InvestmenTracker-emailconfirm.html', acct_status=user['acct_status'], oldtoken=token)
            else:
                return redirect('/')
    else:
        return redirect('/')


@bp.route('/reconfirm_email/<oldtoken>', methods=['GET','POST'])
def resend_confirm_link(oldtoken):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    if (request.method == 'GET'):
        user = User.objects(token=oldtoken).first()
        usertoken = user['token']
        useremail = user['email']

        if (usertoken and useremail):
            newtoken = s.dumps(useremail, salt='email-confirm')

            user['token'] = newtoken
            user.save()

            send_email(subject='InvestmenTracker Account Confirmation Link Renewal',
                        sender=current_app.config['MAIL_USERNAME'],
                        recipient=useremail)

            time.sleep(5)
            return redirect('/')
    else:
        return jsonify("There was an error processing the new confirmation link email..."), time.sleep(5), redirect('/')


@bp.route('/pass_reset/<token>', methods=['GET'])
def password_reset(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset', max_age=1800)
        acct_status = 'pass_reset'

        return render_template('InvestmenTracker-emailconfirm.html', acct_status=acct_status)
    
    except Exception:
        acct_status = 'pass_reset_exp'
        return render_template('InvestmenTracker-emailconfirm.html', acct_status=acct_status)


@bp.route('/addnewuser', methods=["POST"])
def adduser():
    newuserdata = {}
    senddataback = ""
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    if request.method == "POST":
        hashpass = bcrypt.hashpw(request.json['Password'].encode('utf-8'), bcrypt.gensalt())
        newuserdata['User Name'] = request.json['User Name']
        newuserdata['First Name'] = request.json['First Name']
        newuserdata['Last Name'] = request.json['Last Name']
        newuserdata['Password'] = hashpass
        newuserdata['Email'] = request.json['Email']
        recaptchadata = request.json['Recaptcha']

        #2ND RECAPTCHA AUTHENTICATION (NOT REQUIRED) AS JAVASCRIPT AUTH SHOULD BE SUFFICIENT ENOUGH
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = {'secret':'6LfoU3sUAAAAADg2saBK9l2otrKNNNKdCgqV32a9','response': recaptchadata}, timeout=10)
        google_response = json.loads(r.text)    #CONVERTS GOOGLE'S RESPONSE

    userdb = mongo.db.UserInfo
    stockdb = mongo.db.UserStocks
    finduser = userdb.find_one({'UserName' : newuserdata['User Name']})
    findemail = userdb.find_one({'Email' : newuserdata['Email']})

    if (finduser):
        senddataback = "2"
        return jsonify(senddataback)
    elif (findemail):
        senddataback = "3"
        return jsonify(senddataback)
    elif (google_response['success'] == False):     #2ND RECAPTCHA AUTHENTICATION (NOT REQUIRED)
        return jsonify("Recaptcha authentication failed!")
    else:
        token = s.dumps(newuserdata['Email'], salt='email-confirm')
        userdb.insert_one({
            'UserName' : newuserdata['User Name'],
            'FirstName' : newuserdata['First Name'],
            'LastName' : newuserdata['Last Name'],
            'Password' : newuserdata['Password'],
            'Email' : newuserdata['Email'],
            'Verified' : False,
            'Token' : token,
            'Login_attempts': 0,
            })
        stockdb.insert_one({
            'UserName' : newuserdata['User Name'],
            'Email' : newuserdata['Email'],
            'StockLib' : [],
        })
        

        msg = Message(subject='InvestmenTracker Account Confirmation Link',
        sender='InvestmenTracker1@gmail.com',
        recipients=[newuserdata['Email']])
        

        msg.html = """
        <p>Mr./Ms./Mrs. %s<br>
        <br>
        Welcome! Thank you for signing up. I hope you will enjoy my simplistic stock portfolio manager.
        For any issues or questions, please feel free to use the "Contact Me" page.
        <br>
        <br>
        Please follow this link to activate your account: <a href="http://localhost:5000/confirm_email/%s">Click here to confirm your account</a></p>""" % (newuserdata['Last Name'], token)

        mail.send(msg)

        senddataback = "1"
        return jsonify(senddataback)
    

@bp.route('/passrecovery', methods=['POST'])
def recover():
    userdb = mongo.db.UserInfo
    finduserbyemail = userdb.find_one({'Email' : request.json['forgotemail']})

    forgotlastnameinfo = request.json['forgotlastname']
    forgotemailinfo = request.json['forgotemail']

    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    if (finduserbyemail):
        founduserlastname = finduserbyemail['LastName']
        founduseremail = finduserbyemail['Email']
        foundusername = finduserbyemail['UserName']
        founduserid = finduserbyemail['_id']
    else:
        return "Invalid email/pw combination!"




    if ((forgotlastnameinfo).lower() == founduserlastname.lower() and forgotemailinfo.lower() == founduseremail.lower()):
        userdb.update_one({'_id' : ObjectId(founduserid)}, {'$set' : {'Login_attempts' : 0} } )
        token = s.dumps(founduseremail, salt='password-reset')
        session['username'] = foundusername

        msg = Message(subject='InvestmenTracker Account Retrieval - Password Reset Link',
        sender='InvestmenTracker1@gmail.com',
        recipients=[founduseremail])
        

        msg.html = """
        <p>Mr./Ms./Mrs. %s<br>
        <br>
        Please reset your password with the link below.<br>
        <br>
        <br>
        Password Confirmation Link: <a href="http://localhost:5000/pass_reset/%s">Click here to confirm your account</a></p>""" % (founduserlastname, token)

        mail.send(msg)

        return "An email has been sent to you for further instructions."
    else:
        return "Invalid email/pw combination!"


@bp.route('/replaceoldpw',methods=['POST'])
def replacepw():
    try:
        user_name = session['username']
        userdb = mongo.db.UserInfo
        finduserbyusername = userdb.find_one({'UserName' : user_name})
        founduserid = finduserbyusername['_id']
        founduserpass = finduserbyusername['Password']

        if (finduserbyusername):
            newuserpw = (request.json['newpwreset'])
            hashnewpass = bcrypt.hashpw(newuserpw.encode('utf-8'), bcrypt.gensalt())
            
            userdb.update_one({'_id' : ObjectId(founduserid)}, {
                '$set' : {'Password' : hashnewpass} } )

            return ('success')
        
        return ('error')
    
    except Exception:
        session['acct_status'] = 'pass_reset'
        return render_template('InvestmenTracker-emailconfirm.html', acct_status=session['acct_status'])
