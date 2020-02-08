$(document).ready(() => {

    /* PASSWORD RESET EFFECTS */
    $('.newpassinfo').blur(function() {
        if (($(this)[0].value).length > 0) {
            $(this).css('color','black');
            $(this).css('font-style','normal');
        } else {
            $(this).css('font-style','italic');
        };
    });

    $('#newpwsubmit').on('click', (event) => {
        let newpassword = document.getElementsByClassName('newpassinfo')[0].value;
        let renewpass = document.getElementsByClassName('retypenewpassinfo')[0].value;
        let email = $('#useremail')[0].value;
        
        if (newpassword.length < 5 || (specialCharChk(newpassword) === false) || (hasLowerCase(newpassword) === false) || (hasUpperCase(newpassword) === false)) {
            $('.newpassinfo').css("border","1px solid red");
            alert("Please use at least one special character, one UPPERcase letter and one lowercase letter for your password!");
            event.preventDefault();
        } else {
            $('.newpassinfo').css("border","1px solid black");
            var new_pw_verif = 1;
        };

        if (renewpass.length === 0 || renewpass !== newpassword) {
            $('.retypenewpassinfo').css("border","1px solid red");
            alert("Please retype your new password correctly!");
            event.preventDefault();
        } else {
            $('.retypenewpassinfo').css("border","1px solid black");
            var retypenewpwverified = 1;
            var data = {
                'useremail' : email,
                'newpwreset' : renewpass
            };

            if (new_pw_verif == 1 && retypenewpwverified == 1) {
                $.ajax({
                url: '/replaceoldpw',
                data: JSON.stringify(data),
                contentType: 'application/json',
                type: 'POST',
                success: function(response) {
                    $('.newpasstext').css('visibility','hidden');
                    $('.newpassinfo').css('visibility','hidden');
                    $('.retypenewpasstext').css('visibility','hidden');
                    $('.retypenewpassinfo').css('visibility','hidden');
                    $('#onclicknewpw').css('visibility','hidden');
                    $('.shownewpwtxt').css('visibility','hidden');
                    $('#newpwsubmit').css('visibility','hidden');
                    $('.newpwsuccessmsg').css('visibility','visible');
                    if (response == 'error') {
                        alert('There was an error updating your password! Please send a feedback through our contact us page.');
                    } else if (response == 'success') {
                        $('.newpwsuccessmsg').delay(7000).queue( (next) => {
                            window.location.replace('/');
                            next();
                            });
                        }
                    }
                });
            }
        }
    });

    /* CONFIRMING EMAIL EFFECTS */
    $('.reconfirmemailmsg2').on('click', () => {
        $('.reconfirmemailmsg').css('display','none');
        $('.reconfirmemailmsg2').css('display','none');
        $('.reconfirmemailmsg3').css('visibility','visible');
    });
});



/* HIDE/SHOW NEW PASSWORD */

function hideNewPW() {
    var x = document.getElementById("hiddennewpw");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    };
};

/* VERIFYING SPECIAL CHARACTERS WITHIN USER'S NEW PW */

function specialCharChk(stringinput) {
    return RegExp(/[~`!@#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/).test(stringinput);
};

function hasLowerCase(stringinput) {
    return (/[a-z]/.test(stringinput));
};

function hasUpperCase(stringinput) {
    return (/[A-Z]/.test(stringinput));
};
