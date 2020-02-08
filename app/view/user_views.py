from flask import session, current_app, redirect, jsonify, request, render_template
from itsdangerous import URLSafeSerializer

from app.view import bp
from app.model.users import User
from app.model.stocks import Stocks
from app.model.email import send_email
from app.model.token import generate_token, verify_token
from app.model.recaptcha import google_recaptchaV2


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
    print(token)
    user_email = verify_token(token, age=259200, salt='password-reset')
    user = User.get_user_by_email(user_email)
    print(user)
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
        token = generate_token(newuserdata['Email'], salt='email-confirm')
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
        new_user.save()
        new_user_stocks.save()
        
        send_email(sub='InvestmenTracker Account Confirmation Link',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipient=newuserdata['Email'],
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