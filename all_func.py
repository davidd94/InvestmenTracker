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
