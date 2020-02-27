from flask import session, current_app, redirect, jsonify, request, render_template

from app import mongo
from app.view import bp
from app.model.users import User
from app.model.stocks import Stocks
from app.model.email import send_email
from app.model.token import generate_token, verify_token
from app.model.recaptcha import google_recaptchaV2
from app.model.validators import ValidateName, ValidateEmail, ValidatePass


@bp.route('/loginuser', methods=["POST"])
def userloggedin():
    if (request.method == "POST"):
        userloginname = (request.json['loginusername']).lower()
        userloginpw = request.json['loginuserpw']
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

@bp.route('/loggedout', methods=["GET"])
def userloggedout():
    session.clear()
    return '/'

@bp.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    user_email = verify_token(token, age=259200, salt='email-confirm')
    user = User.get_user_by_email(user_email)
    
    if (user):
        if (user['acct_status'] == False):
            user.update(acct_status=True)
            user.reload()
            return render_template('InvestmenTracker-emailconfirm.html', acct_status='email_confirm')
        return redirect('/')
    else:
        return render_template('InvestmenTracker-emailconfirm.html', acct_status='email_confirm_exp')

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
    user_email = verify_token(token, age=259200, salt='password-reset')
    user = User.get_user_by_email(user_email)
    if user:
        acct_status = 'pass_reset'
        return render_template('InvestmenTracker-emailconfirm.html', acct_status=acct_status, useremail=user.email)
    else:
        acct_status = 'pass_reset_exp'
        return render_template('InvestmenTracker-emailconfirm.html', acct_status=acct_status)


@bp.route('/addnewuser', methods=["POST"])
def adduser():
    new_username = (request.json['User Name']).lower()
    new_firstname = (request.json['First Name']).lower()
    new_lastname = (request.json['Last Name']).lower()
    new_hash_password = User.hash_password(request.json['Password'])
    new_email = (request.json['Email']).lower()
    recaptchadata = request.json['Recaptcha']
    
    google_response = google_recaptchaV2(recaptchadata)
    
    find_user = User.get_user_by_username(new_username)
    find_email = User.get_user_by_email(new_email)

    if (google_response['success'] == False):
        return jsonify("Recaptcha authentication failed!")
    elif (find_user):
        return jsonify("Username exists")
    elif (find_email):
        return jsonify("Email exists")
    else:
        token = generate_token(new_email, salt='email-confirm')
        new_user = User(username=new_username,
                        firstname=new_firstname,
                        lastname=new_lastname,
                        password=new_hash_password,
                        email=new_email,
                        token=token)
        new_user_stocks = Stocks(username=new_username,
                                email=new_email)

        validation_error = new_user.validate_self()
        if validation_error:
            return jsonify(validation_error)
        
        # if pass validation, save user to DB
        new_user.connect()
        new_user.save()
        new_user_stocks.save()
        
        send_email(sub='InvestmenTracker Account Confirmation Link',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipient=new_email,
                    email_type='acct_new',
                    token=token)
        
        return jsonify("User created")
    

@bp.route('/passrecovery', methods=['POST'])
def recover():
    email_data = (request.json['forgotemail']).lower()
    user = User.get_user_by_email(email_data)

    if (user):
        token = generate_token(user.email, 'password-reset')
        send_email(sub='InvestmenTracker Account Retrieval - Password Reset',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipient=user.email,
                    email_type='pass_recovery',
                    token=token)
        return "An email has been sent to you for further instructions."
    else:
        return "Invalid email/pw combination!"


@bp.route('/replaceoldpw', methods=['POST'])
def replacepw():
    user = User.get_user_by_email(request.json['useremail'])
    if user:
        new_password = request.json['newpwreset']
        new_hash_password = User.hash_password(new_password)

        user.update(password=new_hash_password)
        user.reload()
        
        if user.password == new_hash_password:
            return ('success')
        return ('error')
    
    return render_template('InvestmenTracker-emailconfirm.html', acct_status='pass_reset_exp')


@bp.route('/userprofile')
def profile():
    try:
        if 'username' in session:
            userdb = mongo.db.Users
            finduser = userdb.find_one({'username': session['username']})
            userlastname = finduser['lastname']
            form_name = ValidateName()
            form_email = ValidateEmail()
            form_pass = ValidatePass()
        
            return render_template('InvestmenTracker-userprofile.html', title=session['username'],
                                                                        firstname=finduser['firstname'],
                                                                        lastname=userlastname,
                                                                        email=session['email'],
                                                                        form_name=form_name,
                                                                        form_email=form_email,
                                                                        form_pass=form_pass)
    except:
        return redirect('/')
    

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

        userdb = mongo.db.Users
        finduser = userdb.find_one({'Username' : username})

        formname = ValidateName(request.form)
        formemail = ValidateEmail(request.form)
        formpass = ValidatePass(request.form)

        form_name = ValidateName()
        form_email = ValidateEmail()
        form_pass = ValidatePass()

        if (updatefirstname == "" and updatelastname == ""):
            form_name_error = "You have left your name empty :("
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error)

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
                        userdb.update_one({'username' : username}, {'$set': {'firstname' : updatefirstname}})
                        session['firstname'] = updatefirstname
                        form_name_error = "Successfully updated your first name!"
                elif (oldfirstname == updatefirstname and oldlastname != updatelastname):       #LAST NAME CHANGES MADE
                    if (formname.errors):
                        form_name_error = formname.errors
                    else:
                        userdb.update_one({'username' : username}, {'$set': {'lastname' : updatelastname}})
                        session['lastname'] = updatelastname
                        form_name_error = "Successfully updated your last name!"
                elif (oldfirstname != updatefirstname and oldlastname != updatelastname):       #FIRST AND LAST NAME CHANGES MADE
                    if (formname.errors):
                        form_name_error = formname.errors
                    else:
                        userdb.update_one({'username' : username}, {'$set': {'firstname' : updatefirstname}})
                        userdb.update_one({'username' : username}, {'$set': {'lastname' : updatelastname}})
                        session['firstname'] = updatefirstname
                        session['lastname'] = updatelastname
                        form_name_error = "Successfully updated your first and last name!"
            else:
                form_name_error = "You have left your name empty :("
                return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error)

        if (confirmemail):       #VALIDATES IF EMAIL CHANGE OCCURS
            if formemail.validate():
                finduserbyemail = userdb.find_one({'email' : confirmemail})
                if (finduserbyemail):
                    form_email_error = "That email already exist. Please use another email."
                    return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error)
                else:
                    userdb.update_one({'username' : username}, {'$set': {'email' : confirmemail}})
                    session['email'] = confirmemail
                    form_email_error = "Successfully updated your email address!"
            else:
                form_email_error = "You must enter a valid email and/or your emails do not match."
                return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error)

        if (confirmpw):          #VALIDATES IF PASSWORD CHANGE OCCURS
            if formpass.validate():
                hashupdatedpass = bcrypt.hashpw(confirmpw.encode('utf-8'), bcrypt.gensalt())
                userdb.update_one({'username' : username}, {'$set': {'password' : hashupdatedpass}})
                form_pass_error = "Successfully updated your password!"
            else:
                form_pass_error = "Your password must be a minimum of 5 characters long and contain at least one uppercase, lowercase, number AND special character."
                if (confirmemail):
                    return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error, form_pass_error=form_pass_error)
                else:
                    return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_pass_error=form_pass_error)
        
        if (updatefirstname or updatelastname) and confirmemail and confirmpw:      #DISPLAYS SUCCESS/ERROR MSG BASED ON WHAT IS UPDATED
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error, form_pass_error=form_pass_error)
        elif (updatefirstname or updatelastname) and confirmemail:
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_email_error=form_email_error)
        elif (updatefirstname or updatelastname) and confirmpw:
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error, form_pass_error=form_pass_error)
        elif (updatefirstname or updatelastname):
            return render_template('InvestmenTracker-userprofile.html', title=session['username'], firstname=session['firstname'], lastname=session['lastname'], email=session['email'], form_name=form_name, form_email=form_email, form_pass=form_pass, form_name_error=form_name_error)
        else:
            return redirect('/')
    
    except Exception:
        return redirect('/')