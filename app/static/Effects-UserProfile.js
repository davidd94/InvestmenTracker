$(document).ready(() => {

    /* DISPLAYS SUCCESS OR FAIL ICON FOR THE ERROR MESSAGES AFTER 'SAVE' */
    let namevalidation = $('.nameerror')[0].textContent;
    let emailvalidation = $('.emailerror')[0].textContent;
    let passvalidation = $('.passerror')[0].textContent;

    if (namevalidation == "You have left your name empty :(") {
        $('.profileerrorbox li .nameerroricon').css('display','initial');
        $('.nameerroricon')[0].src = "http://localhost:5000/static/failmark.png";
    } else if (namevalidation === "Successfully updated your first name!" || namevalidation == "Successfully updated your last name!" || namevalidation == "Successfully updated your first and last name!") {
        $('.profileerrorbox li .nameerroricon').css('display','initial');
    };

    if (emailvalidation == "You must enter a valid email and/or your emails do not match." || emailvalidation == "That email already exist. Please use another email.") {
        $('.profileerrorbox li .emailerroricon').css('display','initial');
        $('.emailerroricon')[0].src = "http://localhost:5000/static/failmark.png";
    } else if (emailvalidation === "Successfully updated your email address!") {
        $('.profileerrorbox li .emailerroricon').css('display','initial');
    };

    if (passvalidation == "Your password must be a minimum of 5 characters long and contain at least one uppercase, lowercase, number AND special character.") {
        $('.profileerrorbox li .passerroricon').css('display','initial');
        $('.passerroricon')[0].src = "http://localhost:5000/static/failmark.png";
    } else if (passvalidation === "Successfully updated your password!") {
        $('.profileerrorbox li .passerroricon').css('display','initial');
    };


     /* CHANGE EMAIL DISPLAY EFFECTS */
    $('.profilechangeemail').on('click', () => {
        $('.profilechangeemail').css('left','400px');
        $('.profileemailtext').css('left','-200px');
        $('.profileemail').css('left','-200px');
        $('.profilesavesubmit').css('left','0');
        $('.profilenewemail, .profilerenewemail').removeAttr("disabled");
        setTimeout(function() {
            $('.profilenewemailtext').css('display','initial');
            $('.profileemailreq').css('display','initial');
        }, 300);
        setTimeout(function() {
            $('.profilenewemailtext').css('left','0');
        }, 400);
        setTimeout(function() {
            $('.profilerenewemailtext').css('left','0');
            $('.profilerenewemail').css('left','0');
        }, 1200);
    });


    /* CHANGE PASSWORD DISPLAY EFFECTS */
    $('.profilechangepw').on('click', () => {
        $('.profilechangepw').css('left','400px');
        $('.profilenewpasswordtext').css('top','0');
        $('.profilenewpassword').css('top','0');
        $('.profilesavesubmit').css('left','0');
        $('.profilenewpassword, .profilerenewpw').removeAttr("disabled");
        setTimeout(function () {
            $('.profilerenewpwtext').css('left','0');
            $('.profilerenewpw').css('left','0');
        }, 2200);
    });


    /* REMOVING ASTERISK WHEN INPUT FIELDS ARE EMPTY */
    $('.profilenewemail, .profilerenewemail').on('keydown', () => {
        if (($('.profilenewemail')[0].value).length > 0 || ($('.profilerenewemail')[0].value).length > 0) {
            $('.profileemailreq').css('top','0');
            $('.profileemailreq2').css('left','0');
        }
    });
    $('.profilenewemail, .profilerenewemail').on('focusout', () => {
        if (($('.profilenewemail')[0].value).length == 0 && ($('.profilerenewemail')[0].value).length == 0) {
            $('.profileemailreq').css('top','-200px');
            $('.profileemailreq2').css('left','-500px');
        }
    });

    $('.profilenewpassword, .profilerenewpw').on('keydown', () => {
        if (($('.profilenewpassword')[0].value).length > 0 || ($('.profilerenewpw')[0].value).length > 0) {
            $('.profilepwreq').css('top','0');
            $('.profilepwreq2').css('left','0');
        }
    });
    $('.profilenewpassword, .profilerenewpw').on('focusout', () => {
        if (($('.profilenewpassword')[0].value).length == 0 && ($('.profilerenewpw')[0].value).length == 0) {
            $('.profilepwreq').css('top','-300px');
            $('.profilepwreq2').css('left','-300px');
        }
    });


    /* DISPLAY 'SAVE' BUTTON FOR KEYDOWN ON NAMES */
    $('.profilefirstname, .profilelastname').on('keydown', () => {
        $('.profilesavesubmit').css('left','0');
    });


    /* 'SAVE' AND 'CANCEL' ON-CLICK EVENTS */
    $('.profilesavesubmit').on('click', () => {
        $('.profilenewemail, .profilerenewemail').removeAttr("disabled");
        $('.profilenewpassword, .profilerenewpw').removeAttr("disabled");
        $('.profileerrorbox li .nameerroricon').css('display','none');
        $('.profileerrorbox li .emailerroricon').css('display','none');
        $('.profileerrorbox li .passerroricon').css('display','none');
    });

    $('.profilecancelsubmit').on('click',() => {
        window.location.replace('/');
    });
    

    /*  UNFINISHED JQUERY USER INPUT VALIDATION
    $('.profilesavesubmit').on('click', () => {
        let firstname = $('.profilefirstname')[0].value;
        let lastname = $('.profilelastname')[0].value;
        let emailchangechk = $('.profilerenewemail').css('left');

        if (emailchangechk == "0px") {
            let newemail = $('.profilenewemail')[0].value;
            let confirmnewemail = $('.profilerenewemail')[0].value;
            let pwchangechk = $('.profilenewpassword').css('top');
            if (pwchangechk == '0px') {
                let newpw = $('.profilenewpassword')[0].value;
                let confirmnewpw = $('.profilerenewpw')[0].value;

                let updatedata = {'FirstName' : firstname,'LastName' : lastname, 'Email' : UNFINISHED}
                $.ajax({
                    url: '/updateprofileinfo',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(updatedata),
                    success: function(response) {
                        console.log(response);
                    },
                });
            }
        }


        /*
        let emailchangechk = $('.profilerenewemail').css('left');
        if (emailchangechk == '0px') {
            let newemail = $('.profilenewemail')[0].value;
            let confirmnewemail = $('.profilerenewemail')[0].value;
            if (newemail != confirmnewemail) {
                $('.profilenewemail').css('border','0.5px solid red');
                $('.profilerenewemail').css('border','0.5px solid red');
                alert("Your new email address does not match.");
            } else {
                $('.profilenewemail').css('border','none');
                $('.profilerenewemail').css('border','none');
            }
        }
    }) */
})