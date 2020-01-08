from flask import session, current_app, redirect, jsonify
from itsdangerous import URLSafeSerializer

from app.view.home_views import homepage
from app.controller import bp
from app.model.users import User
from app.model.email import send_email
from app.model.token import generate_token, verify_token
from app.model.recaptcha import google_recaptchaV2


@bp.route('/loginuser', methods=["POST"])
def userloggedin():
    if (request.method == "POST"):
        userloginname = request.json['loginusername']
        userloginpw = request.json['loginuserpw']
        User.connect()
        finduser = User.get_user_by_username(userloginname)

        if (finduser):
            hash_password = User.hash_password(userloginpw)

            if (hash_password == finduser['password'] and finduser['failed_login'] < 10):
                if (finduser['acct_status'] == False):
                    return "Please confirm your account before logging in."
                session['username'] = finduser['username']
                session['firstname'] = finduser['firstname']
                session['lastname'] = finduser['lastname']
                session['email'] = finduser['email']
                finduser['failed_login'] = 0
                finduser.save()
                return jsonify("You have successfully logged in!")
            elif (hash_password != finduser['password']):
                if (finduser['failed_login'] >= 10):
                    return "Exceeded failed login attempts!"
                finduser['failed_login'] += 1
                finduser.save()
                return "Invalid username/password!"        

        return "Invalid username/password!"

@bp.route('/loggedout', methods=["POST"])
def userloggedout():
    session.pop('username', None)
    redirect('/')

@bp.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    user_email = verify_token(token, age=259200, salt='email-confirm')
    user = User.objects(email=user_email).first()

    if (user):
        if (user['acct_status'] == False):
            user.update(acct_status=True)
            user.reload()
            return render_template('InvestmenTracker-emailconfirm.html', acct_status='email_confirm')
        return redirect('/')
    
    user = User.objects(token=token).first()
    if (user):
        return render_template('InvestmenTracker-emailconfirm.html', acct_status='email_confirm_exp')
    return redirect('/')

@bp.route('/reconfirm_email/<oldtoken>', methods=['GET','POST'])
def resend_confirm_link(oldtoken):
    if (request.method == 'GET'):
        user = User.get_user_by_token(oldtoken)

        if (user):
            new_token = generate_token(user.email, salt='email-confirm')
            user['token'] = new_token
            user.save()

            send_email(subject='InvestmenTracker Account Confirmation Link Renewal',
                        sender=current_app.config['MAIL_USERNAME'],
                        recipient=user.email)

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
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    if request.method == "POST":
        newuserdata['User Name'] = request.json['User Name']
        newuserdata['First Name'] = request.json['First Name']
        newuserdata['Last Name'] = request.json['Last Name']
        newuserdata['Password'] = User.hash_password(request.json['Password'])
        newuserdata['Email'] = request.json['Email']
        recaptchadata = request.json['Recaptcha']
        
        google_response = google_recaptchaV2(recaptchadata)

        #userdb = mongo.db.UserInfo
        stockdb = mongo.db.UserStocks
        find_user = User.objects(username=request.json['User Name']).first()
        find_email = userdb.find_one({'Email' : newuserdata['Email']})

        if (find_user):
            return jsonify("Username exists")
        elif (find_email):
            return jsonify("Email exists")
        elif (google_response['success'] == False):
            return jsonify("Recaptcha authentication failed!")
        else:
            token = generate_token(newuserdata['Email'], salt='email-confirm')
            new_user = User(username=newuserdata['User Name'],
                            firstname=newuserdata['First Name'],
                            lastname=newuserdata['Last Name'],
                            password=newuserdata['Password'],
                            email=newuserdata['Email'],
                            token=token)
            validation_error = new_user.validate_self()

            if validation_error:
                return jsonify(validation_error)
            
            new_user.save()

            """
            stockdb.insert_one({
                'UserName' : newuserdata['User Name'],
                'Email' : newuserdata['Email'],
                'StockLib' : [],
            })"""
            
            send_email(sub='InvestmenTracker Account Confirmation Link',
                        sender=current_app.config['MAIL_USERNAME'],
                        recipient=newuserdata['Email'],
                        email_type='acct_new',
                        token=token)
            
            return jsonify("User created")
    

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
