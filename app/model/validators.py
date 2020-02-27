from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


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
