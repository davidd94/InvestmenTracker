import random
import os
import urllib
import sys
import time
from datetime import datetime

from flask import Flask, render_template, request, redirect, Response, jsonify, url_for, session, flash
from flask_mail import Message, Mail
from flask_wtf import FlaskForm, RecaptchaField
from flask_recaptcha import ReCaptcha
from flask_pymongo import PyMongo
from itsdangerous import URLSafeTimedSerializer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bson import ObjectId
from bs4 import BeautifulSoup

import json
import bcrypt
import requests


app = Flask(__name__)


""" ******* MONGODB ATLAS (CLOUD) DATABASE CONNECTION ******* """

app.config['SECRET_KEY'] = os.urandom(24)
app.config['MONGO_DBNAME'] = 'InvestmenTracker'
app.config['MONGO_URI'] = 'mongodb+srv://davidd9:mouse312@cluster0-liqmz.gcp.mongodb.net/InvestmenTracker?retryWrites=true'

mongo = PyMongo(app)


""" ******* GOOGLE RECAPTCHA VERIFICATION KEYS ******* """

app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfoU3sUAAAAAGhGo6pBHk6kdmKb197mHdESWc6v'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfoU3sUAAAAADg2saBK9l2otrKNNNKdCgqV32a9'

recaptcha = ReCaptcha(app)


""" ******* FLASK-MAIL EMAIL SETUP USING GMAIL ******* """

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'investmentracker1@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mouse31@'

mail = Mail(app)


s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


""" ******* GLOBAL VARIABLES (USER INFO) ******* """





""" ******* SERVER WEBPAGE ROUTING ******* """


@app.route("/")
def homepage():
    if ('username' in session) and ('firstname' in session):
        return render_template('InvestmenTracker-homepage.html', title=session['username'], name=session['firstname'])
    else:
        return render_template('InvestmenTracker-homepage.html')

@app.route("/userportfolio")
def userstockportfolio():
    if 'username' in session:
        return render_template('InvestmenTracker-userportfolio.html', title=session['username'])
    else:
        return redirect('/')

@app.route("/aboutme")
def aboutme():
    if 'username' in session:
        return render_template('InvestmenTracker-aboutme.html', title=session['username'])
    else:
        return render_template('InvestmenTracker-aboutme.html')

@app.route("/contactme")
def contact():
    if 'username' in session:
        return render_template('InvestmenTracker-contact.html', title=session['username'], username=session['firstname'], useremail=session['email'])
    else:
        return render_template('InvestmenTracker-contact.html')


""" ******* SERVER VERIFICATION REQUESTS ONLY ******* """


@app.route('/loggedout', methods=["POST"])
def userloggedout():
    session.pop('username', None)
    return ('/')


@app.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    userdb = mongo.db.UserInfo
    founduserbytoken = userdb.find_one({'Token' : token})
    if (founduserbytoken != None):
        foundusertoken = founduserbytoken['Token']
        founduserid = founduserbytoken['_id']
        foundverifieduser = founduserbytoken['Verified']
    
        try:
            email = s.loads(token, salt='email-confirm', max_age=259200)
            session['acct_status'] = 'email_confirm'

            if (founduserid and foundverifieduser == False):
                userdb.update_one({'_id' : ObjectId(founduserid)}, {'$set' : {'Verified' : True} } )

                return render_template('investmentracker-acctchanges.html', acct_status=session['acct_status'])
            else:
                return redirect('/')

        except Exception:
            if (foundverifieduser == False):
                session['acct_status'] = 'email_confirm_exp'
                
                return render_template('investmentracker-acctchanges.html', acct_status=session['acct_status'], oldtoken=token)
            else:
                return redirect('/')
    else:
        return redirect('/')


@app.route('/reconfirm_email/<oldtoken>', methods=['GET','POST'])
def resend_confirm_link(oldtoken):
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


@app.route('/pass_reset/<token>', methods=['GET'])
def password_reset(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=1800)
        session['acct_status'] = 'pass_reset'

        return render_template('investmentracker-acctchanges.html', acct_status=session['acct_status'])
    
    except Exception:
        session['acct_status'] = 'pass_reset_exp'
        return render_template('investmentracker-acctchanges.html', acct_status=session['acct_status'])



""" ******* SERVER TO DATABASE REQUESTS ******* """



@app.route("/sendfeedback", methods=['POST'])
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


@app.route('/loginuser', methods=["POST"])
def userloggedin():
    if (request.method == "POST"):
        userloginname = request.json['loginusername']
        userloginpw = request.json['loginuserpw']
        finduser = mongo.db.UserInfo
        founduser = finduser.find_one({'UserName' : userloginname})

        if (founduser):
            userloginfirstname = founduser['FirstName']
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
            session['email'] = userloginemail
            return jsonify("You have successfully logged in!")
        

        return "Invalid username/password!"


@app.route('/addnewuser', methods=["POST"])
def adduser():
    newuserdata = {}
    senddataback = ""

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
            'StockLib' : [{'StockSym' : "", 'StockData' : {"Date" : "", "PurchaseCost" : 0, "Quantity" : 0, "Notes" : ""}},],
            'maxct' : 0,
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
    

@app.route('/passrecovery', methods=['POST'])
def recover():
    userdb = mongo.db.UserInfo
    finduserbyemail = userdb.find_one({'Email' : request.json['forgotemail']})

    forgotlastnameinfo = request.json['forgotlastname']
    forgotemailinfo = request.json['forgotemail']

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


@app.route('/replaceoldpw',methods=['POST'])
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
        return render_template('investmentracker-acctchanges.html', acct_status=session['acct_status'])


@app.route('/storestockinfo',methods=['POST'])
def storestocks():
    stockname = request.json
    print(stockname)
    username = session['username']
    print(username)

    userstockdb = mongo.db.UserStocks
    finduser = userstockdb.find_one({'UserName' : username})
    print(finduser)
    existingstock = finduser['StockSym']
    print(existingstock)
    stockliblength = len(existingstock)
    print(stockliblength)
    adduserstock = finduser.update_one({'UserName' : username}, {
        '$set' : {'StockInfo.StockSym' : stockname}
    })

    if (finduser):
        if (existingstock):
            return jsonify("You already have that stock in your profile!")
        else:
            adduserstock
            return jsonify("You have successfully added a stock!")
    elif (finduser == None):
        return jsonify("No user stock info has been found!")
    
    return jsonify("FAILED TO ADD STOCK INFO SOMEWHERE")



""" ******* SERVER WEB SCRAPING ******* """



@app.route('/scrapingdata', methods=['POST'])
def webscrape():
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




""" *** GOOGLE'S RECAPTCHA VERIFICATION ***

@app.route('/recaptcha', methods=['POST'])
def recaptchachk():
    gg123 = request.form['g-recaptcha-response']
    print(gg123)
    return jsonify('well this works...')

"""



if __name__ == "__main__":
    app.run(debug=True)


