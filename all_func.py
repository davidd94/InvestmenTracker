from flask import render_template, request, redirect, jsonify, url_for, session, current_app
from flask_mail import Message, Mail
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from bson import ObjectId
from bs4 import BeautifulSoup
from itsdangerous import URLSafeTimedSerializer

import random, time
import json, bcrypt, requests, urllib

from flask import Blueprint

bp = Blueprint('all_func', __name__)


""" ******* GLOBAL FUNCTIONS/CLASSES ******* """


class ValidateName(FlaskForm):
    newfirstname = StringField('newfirstname', [validators.InputRequired(message="Need to enter a first name."), validators.Length(min=1,max=20)])
    newlastname = StringField('newlastname', [validators.InputRequired(message="Need to enter a last name."),validators.Length(min=1,max=20)])
    
class ValidateEmail(FlaskForm):
    newemail = StringField('newemail', [validators.InputRequired(), validators.Length(min=1,max=50), validators.Email(message="Please use a valid email address.")])
    confirmemail = StringField('confirmemail', [validators.InputRequired(), validators.Length(min=1,max=50), validators.Email(message="Please confirm with a valid email address."), validators.EqualTo('newemail',message="Your email confirmation doesn't match.")])
    
class ValidatePass(FlaskForm):
    regex = r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$"
    newpw = PasswordField('newpw', [validators.Length(min=5,max=100), validators.InputRequired(message="You must enter a password with 5-15 characters long."), validators.Regexp(regex=regex,message="You must use at least one uppercase, lowercase, number and special character in your password.")])
    confirmnewpw = PasswordField('confirmnewpw', [validators.Length(min=5,max=100), validators.InputRequired(message="You must use at least 1 uppercase, lowercase, number AND special character in your password."), validators.EqualTo('newpw',message="Your passwords don't match.")])



""" ******* SERVER WEBPAGE ROUTING ******* """


@bp.route("/")
def homepage():
    if ('username' in session) and ('firstname' in session):
        return render_template('InvestmenTracker-homepage.html', title=session['username'], name=session['firstname'])
    else:
        return render_template('InvestmenTracker-homepage.html')

@bp.route("/userportfolio")
def userstockportfolio():
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

@bp.route("/userprofile")
def profile():
    if 'username' in session:
        userdb = mongo.db.UserInfo
        finduser = userdb.find_one({'UserName' : session['username']})
        userlastname = finduser['LastName']
        form_name = ValidateName()
        form_email = ValidateEmail()
        form_pass = ValidatePass()

        return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=userlastname, email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass)
    else: 
        return redirect('/')


""" ******* SERVER VERIFICATION REQUESTS ONLY ******* """


@bp.route('/loggedout', methods=["POST"])
def userloggedout():
    session.pop('username', None)
    return ('/')


@bp.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    userdb = mongo.db.UserInfo
    founduserbytoken = userdb.find_one({'Token' : token})
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    if (founduserbytoken != None):
        foundusertoken = founduserbytoken['Token']
        founduserid = founduserbytoken['_id']
        foundverifieduser = founduserbytoken['Verified']
    
        try:
            email = s.loads(token, salt='email-confirm', max_age=259200)
            session['acct_status'] = 'email_confirm'

            if (founduserid and foundverifieduser == False):
                userdb.update_one({'_id' : ObjectId(founduserid)}, {'$set' : {'Verified' : True} } )

                return render_template('InvestmenTracker-emailconfirm.html', acct_status=session['acct_status'])
            else:
                return redirect('/')

        except Exception:
            if (foundverifieduser == False):
                session['acct_status'] = 'email_confirm_exp'
                
                return render_template('InvestmenTracker-emailconfirm.html', acct_status=session['acct_status'], oldtoken=token)
            else:
                return redirect('/')
    else:
        return redirect('/')


@bp.route('/reconfirm_email/<oldtoken>', methods=['GET','POST'])
def resend_confirm_link(oldtoken):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    if (request.method == 'GET'):
        userdb = mongo.db.UserInfo
        founduserbytoken = userdb.find_one({'Token' : oldtoken})
        foundusertoken = founduserbytoken['Token']
        founduseremail = founduserbytoken['Email']
        founduserid = founduserbytoken['_id']
        
        if (foundusertoken and founduseremail):
            newtoken = s.dumps(founduseremail, salt='email-confirm')

            userdb.update_one({'_id' : ObjectId(founduserid)}, {
            '$set' : {'Token' : newtoken} } )

            msg = Message(subject='InvestmenTracker Account Confirmation Link Renewal',
            sender='InvestmenTracker1@gmail.com',
            recipients=[founduseremail])
            

            msg.html = """
            <br>
            <br>
            You have requested a new email confirmation link. It will expire in three (3) days.
            <br>
            <br>
            Please follow this new link to activate your account: <a href="http://localhost:5000/confirm_email/%s">Click here to confirm your account</a></p>""" % (newtoken)

            mail.send(msg)

            time.sleep(5)
            return redirect('/')
    
    else:
        return jsonify("There was an error processing the new confirmation link email..."), time.sleep(5), redirect('/')


@bp.route('/pass_reset/<token>', methods=['GET'])
def password_reset(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset', max_age=1800)
        session['acct_status'] = 'pass_reset'

        return render_template('InvestmenTracker-emailconfirm.html', acct_status=session['acct_status'])
    
    except Exception:
        session['acct_status'] = 'pass_reset_exp'
        return render_template('InvestmenTracker-emailconfirm.html', acct_status=session['acct_status'])



""" ******* SERVER TO DATABASE REQUESTS ******* """



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


@bp.route('/loginuser', methods=["POST"])
def userloggedin():
    if (request.method == "POST"):
        userloginname = request.json['loginusername']
        userloginpw = request.json['loginuserpw']
        finduser = mongo.db.UserInfo
        founduser = finduser.find_one({'UserName' : userloginname})

        if (founduser):
            userloginfirstname = founduser['FirstName']
            userloginlastname = founduser['LastName']
            userloginemail = founduser['Email']
            founduserstatus = founduser['Verified']
            founduserid = founduser['_id']
            founduserlogins = founduser['Login_attempts']
            userpwchk = bcrypt.checkpw(userloginpw.encode('utf-8'), founduser['Password'])

            if (userpwchk == False):
                founduserlogins += 1
                if (founduserlogins > 10):
                    return "Exceeded failed login attempts!"
                while (founduserlogins <= 15):
                    finduser.update_one({'_id' : ObjectId(founduserid)}, {'$set' : {'Login_attempts' : founduserlogins} } )
                    return "Invalid username/password!"
        else:
            return "Invalid username/password!"
        

        if (founduserlogins > 10):
            return "Exceeded failed login attempts!"
        elif (userloginname == founduser['UserName'] and userpwchk and founduserlogins <= 10):
            if (founduserstatus == False):
                return "Please confirm your account before logging in."
            session['username'] = userloginname
            session['firstname'] = userloginfirstname
            session['lastname'] = userloginlastname
            session['email'] = userloginemail
            finduser.update_one({'UserName' : userloginname}, {'$set' : {'Login_attempts' : 0}})
            return jsonify("You have successfully logged in!")
        

        return "Invalid username/password!"


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


@bp.route('/storestockinfo',methods=['POST'])
def storestocks():
    stockname = request.json['Stock']
    stockdate = request.json['Date']
    username = session['username']

    userstockdb = mongo.db.UserStocks
    finduser = userstockdb.find_one({'UserName' : username})
    stockliblength = len(finduser['StockLib'])
    foundexistingstock = False

    for count in range(stockliblength):    #LOOPS EACH USER'S STOCK IN LIBRARY TO FIND ANY DUPLICATES
        findexistingstock = finduser['StockLib'][count]['StockSym']
        if (findexistingstock == stockname):
            foundexistingstock = True
            return jsonify("You already have that stock in your portfolio!")
    
    if (foundexistingstock == False and stockliblength < 10):
        userstockdb.update_one({'UserName' : username}, {'$push' : {'StockLib' : {'StockSym': stockname, 'StockData': {'Date': stockdate, 'PurchaseCost': 0, 'Quantity': 0, 'Notes': ''}}}})
        return jsonify("You have successfully added a stock!")
    elif (stockliblength >= 10):
        return jsonify("You have reached your maximum of 10 stocks in your portfolio! The stock info will only be displayed temporarily. The limit will increase in future updates.")
    elif (finduser == None):
        return jsonify("No user info has been found!")
    
    return jsonify("ERROR: FAILED TO ADD STOCK!")


@bp.route('/deletestockinfo', methods=['POST'])
def deletestocks():
    stockname = request.json
    username = session['username']

    userstockdb = mongo.db.UserStocks
    finduser = userstockdb.find_one({'UserName' : username})
    stockliblength = len(finduser['StockLib'])
    foundexistingstock = False
    
    for count in range(stockliblength):    #LOOPS EACH USER'S STOCK IN LIBRARY TO LOCATE THE SPECIFIC GIVEN STOCK NAME
        findexistingstock = finduser['StockLib'][count]['StockSym']
        if (findexistingstock == stockname):
            foundexistingstock = True
            stockid = count
    
    if (foundexistingstock == True):
        userstockdb.update_one({'UserName' : username}, {'$pull' : {'StockLib' : {'StockSym' : stockname}}})
        return jsonify("You have successfully deleted a stock!")
    elif (finduser == None):
        return jsonify("No user info has been found!")
    
    return jsonify("Deleted temporary stock info!")


@bp.route('/retrievestockinfo', methods=['GET'])
def getstocks():
    if 'username' in session:
        username = session['username']
        userstockdb = mongo.db.UserStocks
        finduser = userstockdb.find_one({'UserName' : username})
        stocklib = finduser['StockLib']

        return jsonify(stocklib)


@bp.route('/updatestockinfo', methods=['POST'])
def updatestocks():
    username = session['username']
    stockname = request.json['Stock']
    edittype = request.json['EditType']
    updatevalue = request.json['Value']
    
    userstockdb = mongo.db.UserStocks
    finduser = userstockdb.find_one({'UserName' : username})
    stockliblength = len(finduser['StockLib'])

    for count in range(stockliblength):    #LOOPS EACH USER'S STOCK IN LIBRARY TO FIND THE DESIRED STOCK
        findexistingstock = finduser['StockLib'][count]['StockSym']
        if (findexistingstock == stockname):
            stocknum = count
            
    if (finduser):
        if (edittype == "Date"):
            userstockdb.update_one({'UserName' : username}, {'$set' : {('StockLib.' + str(stocknum) + '.StockData.Date') :  updatevalue}})
            return "Date updated!!"
        elif (edittype == "PurchaseCost"):
            userstockdb.update_one({'UserName' : username}, {'$set' : {('StockLib.' + str(stocknum) + '.StockData.PurchaseCost') :  float(updatevalue)}})
            return "Purchase Cost updated!!"
        elif (edittype == "Quantity"):
            userstockdb.update_one({'UserName' : username}, {'$set' : {('StockLib.' + str(stocknum) + '.StockData.Quantity') :  float(updatevalue)}})
            return "Quantity updated!!"
        elif (edittype == "Notes"):
            userstockdb.update_one({'UserName' : username}, {'$set' : {('StockLib.' + str(stocknum) + '.StockData.Notes') :  updatevalue}})
            return "Notes updated!!"
    else:
        return jsonify("NO STOCK INFO WAS UPDATED!")
    
    return jsonify("ERROR UPDATING STOCK INFO!")


@bp.route('/updateprofileinfo', methods=['POST'])
def updateinfo():
    try:
        username = session['username']
        oldfirstname = session['firstname']
        oldlastname = session['lastname']
        oldemail = session['email']
        updatefirstname = request.form['newfirstname']
        updatelastname = request.form['newlastname']
        updateemail = (request.form['newemail']).lower()
        confirmemail = (request.form['confirmemail']).lower()
        updatepw = request.form['newpw']
        confirmpw = request.form['confirmnewpw']

        userdb = mongo.db.UserInfo
        finduser = userdb.find_one({'UserName' : username})

        formname = ValidateName(request.form)
        formemail = ValidateEmail(request.form)
        formpass = ValidatePass(request.form)

        form_name = ValidateName()
        form_email = ValidateEmail()
        form_pass = ValidatePass()

        if (updatefirstname == "" and updatelastname == ""):
            form_name_error = "You have left your name empty :("
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error)

        if (updatefirstname or updatelastname):     #VALIDATES IF NAME CHANGE OCCURS
            if formname.validate():
                if (oldfirstname == updatefirstname and oldlastname == updatelastname):     #NO NAME CHANGES MADE
                    if (formname.errors):
                        form_name_error = formname.errors
                    else:
                        form_name_error = ""
                elif (oldfirstname != updatefirstname and oldlastname == updatelastname):       #FIRST NAME CHANGES MADE
                    if (formname.errors):
                        form_name_error = formname.errors
                    else:
                        userdb.update_one({'UserName' : username}, {'$set': {'FirstName' : updatefirstname}})
                        session['firstname'] = updatefirstname
                        form_name_error = "Successfully updated your first name!"
                elif (oldfirstname == updatefirstname and oldlastname != updatelastname):       #LAST NAME CHANGES MADE
                    if (formname.errors):
                        form_name_error = formname.errors
                    else:
                        userdb.update_one({'UserName' : username}, {'$set': {'LastName' : updatelastname}})
                        session['lastname'] = updatelastname
                        form_name_error = "Successfully updated your last name!"
                elif (oldfirstname != updatefirstname and oldlastname != updatelastname):       #FIRST AND LAST NAME CHANGES MADE
                    if (formname.errors):
                        form_name_error = formname.errors
                    else:
                        userdb.update_one({'UserName' : username}, {'$set': {'FirstName' : updatefirstname}})
                        userdb.update_one({'UserName' : username}, {'$set': {'LastName' : updatelastname}})
                        session['firstname'] = updatefirstname
                        session['lastname'] = updatelastname
                        form_name_error = "Successfully updated your first and last name!"
            else:
                form_name_error = "You have left your name empty :("
                return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error)

        if (confirmemail):       #VALIDATES IF EMAIL CHANGE OCCURS
            if formemail.validate():
                finduserbyemail = userdb.find_one({'Email' : confirmemail})
                if (finduserbyemail):
                    form_email_error = "That email already exist. Please use another email."
                    return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error)
                else:
                    userdb.update_one({'UserName' : username}, {'$set': {'Email' : confirmemail}})
                    session['email'] = confirmemail
                    form_email_error = "Successfully updated your email address!"
            else:
                form_email_error = "You must enter a valid email and/or your emails do not match."
                return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error)

        if (confirmpw):          #VALIDATES IF PASSWORD CHANGE OCCURS
            if formpass.validate():
                hashupdatedpass = bcrypt.hashpw(confirmpw.encode('utf-8'), bcrypt.gensalt())
                userdb.update_one({'UserName' : username}, {'$set': {'Password' : hashupdatedpass}})
                form_pass_error = "Successfully updated your password!"
            else:
                form_pass_error = "Your password must be a minimum of 5 characters long and contain at least one uppercase, lowercase, number AND special character."
                if (confirmemail):
                    return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error, form_pass_error=form_pass_error)
                else:
                    return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_pass_error=form_pass_error)
        
        if (updatefirstname or updatelastname) and confirmemail and confirmpw:      #DISPLAYS SUCCESS/ERROR MSG BASED ON WHAT IS UPDATED
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error, form_pass_error=form_pass_error)
        elif (updatefirstname or updatelastname) and confirmemail:
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error)
        elif (updatefirstname or updatelastname) and confirmpw:
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_pass_error=form_pass_error)
        elif (updatefirstname or updatelastname):
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], username=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error)
        else:
            return redirect('/')
    
    except Exception:
        return redirect('/')



""" ******* SERVER WEB SCRAPING ******* """


@bp.route('/scrapingstockdata', methods=['POST'])
def stockscrape():
    try:
        tickersearch = request.json
        finvizstocks = "https://finviz.com/quote.ashx?t=" + tickersearch
        page = urllib.request.urlopen(finvizstocks)
        soup = BeautifulSoup(page, "html.parser")


        scrapeddata = {}
        
        scrapedstockinfo = soup.find_all("td",class_="snapshot-td2-cp")
        refinedstockinfo = []
        scrapedstockvalue = soup.find_all("td",class_="snapshot-td2")
        refinedstockvalue = []
        scrapedstockname = soup.find_all("a",class_="tab-link")
        refinedstocknamelist = []
        stockname = ""
        
        for a in scrapedstockname:         #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
            for b in a:
                for text in b:
                    if (len(text) > 1):
                        refinedstocknamelist.append(text)
        
        if (len(refinedstocknamelist) == 3):        #SAFEGUARDING AGAINST CHANGES IN STOCK COMPANMY NAME
            stockname = refinedstocknamelist[2]
            

        if (len(scrapedstockinfo) != 72 or len(scrapedstockvalue) != 72 ):   #SAFEGUARDING AGAINST ANY CHANGES MADE BY THE DATA-SCRAPED WEB DEV THAT WILL BREAK/INACCURATELY DISPLAY THE DATA ON MY WEBSITE 
            return jsonify("A problem has occurred with our 'Data Analysis'! Please send a feed back through our Contact Us page.")

        for eachtd in scrapedstockinfo:
            for text in eachtd:             #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
                refinedstockinfo.append(text)

        for eachtd in scrapedstockvalue:
            for eachb in eachtd:            #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
                spanlist = eachb.find_all('span')       #A FEW 'SPAN' HTML ELEMENTS THAT NEEDED TO BE EXTRACTED SEPARATELY
                smalllist = eachb.find_all('small')     #A SINGLE 'SMALL' HTML ELEMENT THAT NEEDED TO BE EXTRACTED SEPARATELY
                if (smalllist):
                    for small in smalllist:
                            for innersmalltext in small:    #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
                                refinedstockvalue.append(innersmalltext)
                for text in eachb:
                    if (text == '-' and len(text) == 1):    #FOR ANY NON-VALUES, MUST REPLACE WITH '-'
                        refinedstockvalue.append('-')
                    elif (len(text) == 1):            #CHECKING TO SEE IF FEW VALUES ARE STILL IN THEIR HTML FORMAT WHICH REQUIRES ADDITIONAL EXTRACTION METHODS
                        for span in spanlist:
                            for innerspantext in span:      #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
                                refinedstockvalue.append(innerspantext)
                    else:
                        refinedstockvalue.append(text)
        
        
        #COMBINING THE TWO NEWLY EXTRACTED LIST INTO ONE DICTIONARY TO BE USED
        for i in range(len(refinedstockvalue)):
            scrapeddata[refinedstockinfo[i]] = refinedstockvalue[i]
        
        scrapeddata['CompanyName'] = stockname

        return jsonify(scrapeddata)

    except Exception:
        return jsonify("Failed to find stock/company symbol!")
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")

@bp.route('/scrapinggurunews', methods=['GET'])
def gurunews():
    gurunews = "https://www.gurufocus.com/news.php?cat=guru&n=100"
    page = urllib.request.urlopen(gurunews)
    soup = BeautifulSoup(page, "html.parser")

    articletitle = soup.find_all("a",class_="articletitle")
    articledate = soup.find_all("div",class_="date")
    compilednewsdata = {}
    
    count = 0
    for eacha in articletitle:
        newstitle = eacha.get_text()
        newslink = 'https://www.gurufocus.com' + eacha.get('href')

        compilednewsdata[str(count)] = {'Title' : newstitle, 'Link' : newslink}
        count += 1
    
    count2 = 0
    for div in articledate:
        rawnewsdate = div.get_text()
        newsdate = rawnewsdate.split('-',2)
        refinednewsdate = newsdate[0]
        
        rawstocktick = newsdate[len(newsdate) - 1]
        rawstockticksplit = rawstocktick.split('-')
        rawstocktick2 = rawstockticksplit[0]
        rawstocksplit2 = rawstocktick2.split('\n')
        refinedstocktick = ' '.join(rawstocksplit2)

        stockcheck = refinedstocktick.split(' ')
        if (stockcheck[1] == "Stocks:"):
            compilednewsdata[str(count2)]['Stocks'] = refinedstocktick
        else:
            compilednewsdata[str(count2)]['Stocks'] = ""

        compilednewsdata[str(count2)]['Date'] = refinednewsdate
        count2 += 1
    
    if (count == count2):    #SAFEGUARD IF WEBSITE WAS MODIFIED THUS DATA WILL NOT BE ALIGNED
        return jsonify(compilednewsdata)
    else:
        return jsonify("There was an error retrieving GuruFocus news.")
