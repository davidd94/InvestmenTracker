    /* CREATE ACCT - POST-VERIFICATION VARIABLES TO BE SENT TO SERVER-SIDE */

let verifiedusername = "";
let verifiedfirstname = "";
let verifiedlastname = "";
let verifiednewemail = "";
let verifiednewpassword = "";
let verifiedcaptcha = "";

    /* FRONT-END USER SUBMITTAL VERIFICATIONS */

$(document).ready(() => {

        /* USER LOG-IN VERIFICATION */

    $('.submitbutton').on('click', () => {
        let username = document.getElementsByClassName('userinfo')[0].value;
        let userpw = document.getElementsByClassName('passwordinfo')[0].value;
        let sendlogindata = {'loginusername' : username, 'loginuserpw' : userpw};
        $('#incorrlogin').css('top', '150px');
        $('#failedloginbox').css('top', '150px');
        $('#acctconfirm').css('top', '150px');

        if (username.length === 0) {
            $('.userinfo').css("border","1px solid red");
        } else {
            $('.userinfo').css("border","1px solid black");
        };

        if (userpw.length === 0) {
            $('.passwordinfo').css("border","1px solid red");
        } else {
            $('.passwordinfo').css("border","1px solid black");
        };

        if (username.length > 0 && userpw.length > 0) {
            $.ajax({
                url: '/loginuser',
                data: JSON.stringify(sendlogindata),
                contentType: 'application/json',
                type: 'POST',
                success: function(response) {
                    if (response === "Invalid username/password!") {
                        $('#incorrlogin').css('top', '46px');
                        $('#acctconfirm').css('top', '150px');
                        $('.userinfo').css("border","1px solid red");
                        $('.passwordinfo').css("border","1px solid red");
                        $('#exname').css('top', '150px');
                        $('#exemail').css('top', '150px');
                        $('#success').css('top', '150px');
                        $('#success2').css('top', '150px');
                        $('#failedloginbox').css('top', '150px');
                        $('#hiddenpw')[0].value = '';
                    } else if (response === "Please confirm your account before logging in.") {
                        $('#acctconfirm').css('top', '46px');
                        $('#incorrlogin').css('top', '150px');
                        $('.userinfo').css("border","1px solid black");
                        $('.passwordinfo').css("border","1px solid black");
                        $('#exname').css('top', '150px');
                        $('#exemail').css('top', '150px');
                        $('#success').css('top', '150px');
                        $('#success2').css('top', '150px');
                        $('#failedloginbox').css('top', '150px');
                        $('#hiddenpw')[0].value = '';
                    } else if (response === "Exceeded failed login attempts!") {
                        $('#failedloginbox').css('top', '46px');
                        $('#incorrlogin').css('top', '150px');
                        $('#acctconfirm').css('top', '150px');
                        $('.userinfo').css("border","1px solid red");
                        $('.passwordinfo').css("border","1px solid red");
                        $('#exname').css('top', '150px');
                        $('#exemail').css('top', '150px');
                        $('#success').css('top', '150px');
                        $('#success2').css('top', '150px');
                        $('#hiddenpw')[0].value = '';
                    } else if (response === "You have successfully logged in!") {
                        window.location.replace('/')
                    } else {
                        alert("SOMETHING WENT WRONG!")
                    }
                }
            });
        }
    });

    $('.passwordinfo').on('keyup', (event) => {
        if (event.which == 13) {
            let username = document.getElementsByClassName('userinfo')[0].value;
            let userpw = document.getElementsByClassName('passwordinfo')[0].value;
            let sendlogindata = {'loginusername' : username, 'loginuserpw' : userpw};
            $('#incorrlogin').css('top', '150px');
            $('#failedloginbox').css('top', '150px');

            if (username.length === 0) {
                $('.userinfo').css("border","1px solid red");
            } else {
                $('.userinfo').css("border","1px solid black");
            };

            if (userpw.length === 0) {
                $('.passwordinfo').css("border","1px solid red");
            } else {
                $('.passwordinfo').css("border","1px solid black");
            };

            if (username.length > 0 && userpw.length > 0) {
                $.ajax({
                    url: '/loginuser',
                    data: JSON.stringify(sendlogindata),
                    contentType: 'application/json',
                    type: 'POST',
                    success: function(response) {
                        if (response === "Invalid username/password!") {
                            $('#incorrlogin').css('top', '46px');
                            $('#acctconfirm').css('top', '150px');
                            $('.userinfo').css("border","1px solid red");
                            $('.passwordinfo').css("border","1px solid red");
                            $('#exname').css('top', '150px');
                            $('#exemail').css('top', '150px');
                            $('#success').css('top', '150px');
                            $('#success2').css('top', '150px');
                            $('#failedloginbox').css('top', '150px');
                            $('#hiddenpw')[0].value = '';
                        } else if (response === "Please confirm your account before logging in.") {
                            $('#acctconfirm').css('top', '46px');
                            $('#incorrlogin').css('top', '150px');
                            $('.userinfo').css("border","1px solid black");
                            $('.passwordinfo').css("border","1px solid black");
                            $('#exname').css('top', '150px');
                            $('#exemail').css('top', '150px');
                            $('#success').css('top', '150px');
                            $('#success2').css('top', '150px');
                            $('#failedloginbox').css('top', '150px');
                            $('#hiddenpw')[0].value = '';
                        } else if (response === "Exceeded failed login attempts!") {
                            $('#failedloginbox').css('top', '46px');
                            $('#incorrlogin').css('top', '150px');
                            $('#acctconfirm').css('top', '150px');
                            $('.userinfo').css("border","1px solid red");
                            $('.passwordinfo').css("border","1px solid red");
                            $('#exname').css('top', '150px');
                            $('#exemail').css('top', '150px');
                            $('#success').css('top', '150px');
                            $('#success2').css('top', '150px');
                            $('#hiddenpw')[0].value = '';
                        } else if (response === "You have successfully logged in!") {
                            window.location.replace('/')
                        } else {
                            alert("SOMETHING WENT WRONG!")
                        }
                    }
                });
            }
        }
    });

        /* CREATE NEW ACCOUNT VERIFICATION */

    $('.newacctsubmit').on('click', (event) => {
        let username = document.getElementsByClassName('newusername')[0].value.toLowerCase();
        let firstname = document.getElementsByClassName('newfirstname')[0].value;
        let lastname = document.getElementsByClassName('newlastname')[0].value;
        let newemail = (document.getElementsByClassName('newemailaddress')[0].value).toLowerCase();
        let renewemail = (document.getElementsByClassName('retypeemail')[0].value).toLowerCase();
        let newpassword = document.getElementsByClassName('newpassword')[0].value;
        let renewpass = document.getElementsByClassName('retypenewpw')[0].value;
        let captchachk = grecaptcha.getResponse();

        /* RESET USER INPUT IF PREVIOUS POST FAILED VERIFICATION PROCESS */
        verifiedusername = "";
        verifiedfirstname = "";
        verifiedlastname = "";
        verifiednewemail = "";
        verifiednewpassword = "";
        verifiedcaptcha = "";

        if (username.length < 5 || username.length > 15 || (specialCharChk(username))) {
            $('.newusername').css("border","1px solid red");
            alert("Please input a valid user name with 5-15 (non-special) characters or less!");
            event.preventDefault();
        } else {
            $('.newusername').css("border","1px solid black");
            verifiedusername = username;
        };

        if (firstname.length === 0) {
            $('.newfirstname').css("border","1px solid red");
            event.preventDefault();
        } else {
            $('.newfirstname').css("border","1px solid black");
            verifiedfirstname = firstname;
        };

        if (lastname.length === 0) {
            $('.newlastname').css("border","1px solid red");
            event.preventDefault();
        } else {
            $('.newlastname').css("border","1px solid black");
            verifiedlastname = lastname;
        };

        if (newemail.length === 0 || (newemail.indexOf('@') === -1) || (newemail.indexOf('.') === -1)) {
            $('.newemailaddress').css("border","1px solid red");
            alert("You must use a real email address!");
            event.preventDefault();
        } else {
            $('.newemailaddress').css("border","1px solid black");
        };

        if (renewemail.length === 0 || renewemail !== newemail) {
            $('.retypeemail').css("border","1px solid red");
            alert("Your email does not match!");
            event.preventDefault();
        } else {
            $('.retypeemail').css("border","1px solid black");
            verifiednewemail = renewemail;
        };

        if (newpassword.length < 5 || (specialCharChk(newpassword) === false) || (hasLowerCase(newpassword) === false) || (hasUpperCase(newpassword) === false) || (numbersChk(newpassword) === false)) {
            $('.newpassword').css("border","1px solid red");
            alert("Please use at least ONE UPPERcase letter, lowercase letter, number and special character for your password!");
            event.preventDefault();
        } else {
            $('.newpassword').css("border","1px solid black");
        };

        if (renewpass.length === 0 || renewpass !== newpassword) {
            $('.retypenewpw').css("border","1px solid red");
            alert("Please retype your new password correctly!");
            event.preventDefault();
        } else {
            $('.retypenewpw').css("border","1px solid black");
            verifiednewpassword = renewpass;
        };

        if (captchachk == "" || captchachk.length === 0) {
            $('.recaptcha').css("border","1px solid red");
            alert("We need to verify if you're a robot or not!")
            event.preventDefault();
        } else {
            $('.recaptcha').css("border","1px solid black");
            verifiedcaptcha = captchachk;
        };

        /* COMPILING USER'S INPUT AFTER COMPLETELY PASSING FRONTEND VERIFICATIONS */
        
        if (verifiedusername.length > 5 && verifiedfirstname.length > 0 && verifiedlastname.length > 0 && verifiednewpassword.length > 0 && verifiednewemail.length > 0 && verifiedcaptcha.length > 0) {
            
            let verifiedData = {
                'User Name': verifiedusername,
                'First Name': verifiedfirstname,
                'Last Name': verifiedlastname,
                'Password': verifiednewpassword,
                'Email': verifiednewemail,
                'Recaptcha': verifiedcaptcha
            };
            
            
            $.ajax({
                url: '/addnewuser',
                data: JSON.stringify(verifiedData),
                contentType: 'application/json',
                type: 'POST',
                success: function(auth){
                    if (auth === '1') {
                        $('#success').css('top', '46px');
                        $('#incorrlogin').css('top', '150px');
                        $('#exemail').css('top', '150px');
                        $('#exname').css('top', '150px');
                        $('.newusername, .newfirstname, .newlastname, #newpwhide, #newrepwhide, .newemailaddress, .retypeemail').val("")
                        $('.newusername').css("border","1px solid black");
                        $('.newemailaddress').css("border","1px solid black");
                    } else if (auth === '2') {
                        $('#exname').css('top', '46px');
                        $('.newusername').css("border","1px solid red");
                        $('#incorrlogin').css('top', '150px');
                        $('#exemail').css('top', '150px');
                        $('#success').css('top', '150px');
                    } else if (auth === '3') {
                        $('#exemail').css('top', '46px');
                        $('.newemailaddress').css("border","1px solid red");
                        $('#incorrlogin').css('top', '150px');
                        $('#exname').css('top', '150px');
                        $('#success').css('top', '150px');
                    } else if (auth === 'Recaptcha authentication failed!') {
                        alert(auth);
                    }
                    else {
                        alert("SOMETHING WENT WRONG. PLEASE SEND A FEEDBACK THROUGH OUR CONTACT US PAGE.")
                    }
                }
            });
        };
    });


        /* PASSWORD RETRIEVAL VERIFICATION */

    $('.forgotacctsubmit').on('click', (event) => {
        let forgotlast = document.getElementsByClassName('forgotlastname')[0].value;
        let forgotemail = (document.getElementsByClassName('forgotemailaddress')[0].value).toLowerCase();
        let forgotcap = document.getElementsByClassName('g-recaptcha-response')[1].value;

        if (forgotlast.length === 0) {
            $('.forgotlastname').css("border","1px solid red");
            event.preventDefault();
        } else {
            $('.forgotlastname').css("border","1px solid black");
        };

        if (forgotemail.length === 0 || (forgotemail.indexOf('@') === -1) || (forgotemail.indexOf('.') === -1)) {
            $('.forgotemailaddress').css("border","1px solid red");
            event.preventDefault();
        } else {
            $('.forgotemailaddress').css("border","1px solid black");
        };

        if (forgotcap == "") {
            $('.recaptcha2').css("border","1px solid red");
            event.preventDefault();
        } else {
            $('.recaptcha2').css("border","1px solid black");
        };

        if (forgotlast.length === 0 || forgotemail.length === 0 || (forgotemail.indexOf('@') === -1) || (forgotemail.indexOf('.') === -1) || (forgotcap == "")) {
            event.preventDefault();
        } else {
            let userforgotpwinfo = {"forgotlastname" : forgotlast, "forgotemail" : forgotemail};
            $.ajax({
                url: '/passrecovery',
                data: JSON.stringify(userforgotpwinfo),
                contentType: 'application/json',
                type: 'POST',
                success: function(response) {
                    if (response === "Invalid email/pw combination!") {
                        $('#incorrlogin').css('top', '46px');
                        $('.forgotlastname').css("border","1px solid red");
                        $('.forgotemailaddress').css("border","1px solid red");
                        $('#exname').css('top', '150px');
                        $('#exemail').css('top', '150px');
                        $('#success').css('top', '150px');
                        $('#success2').css('top', '150px');
                    } else if (response === "An email has been sent to you for further instructions.") {
                        $('#success2').css('top', '46px');
                        $('#incorrlogin').css('top', '150px');
                        $('.forgotlastname').css("border","1px solid black");
                        $('.forgotemailaddress').css("border","1px solid black");
                        $('#exname').css('top', '150px');
                        $('#exemail').css('top', '150px');
                        $('#success').css('top', '150px');
                        $('.forgotlastname, .forgotemailaddress').val("");
                    } else {
                        alert("Something went wrong!");
                    }
                }
            });
        };
    });

});



    /* SHOW-HIDE USER'S PASSWORD INPUT */

function hideLoginPW() {
    var x = document.getElementById("hiddenpw");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    };
};

function hideNewPW() {
    var x = document.getElementById("newpwhide");
    var y = document.getElementById("newrepwhide");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    };
    if (y.type === "password") {
        y.type = "text";
    } else {
        y.type = "password";
    };
};


    /* VERIFYING SPECIAL CHARACTERS WITHIN USER'S INPUT */

function specialCharChk(stringinput) {
    return RegExp(/[~`!@#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/).test(stringinput);
};

function numbersChk(stringinput) {
    return (/[0-9]/.test(stringinput));
}

function hasLowerCase(stringinput) {
    return (/[a-z]/.test(stringinput));
};

function hasUpperCase(stringinput) {
    return (/[A-Z]/.test(stringinput));
};
