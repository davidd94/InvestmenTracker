$(document).ready(() => {
    $('.contactmesubmit').on('click', (event) => {
        let feedbackname = $('.contactmename').val();
        let feedbackemail = $('.contactmeemail').val();
        let feedbacktext = $('.contactmefeedback').val();
        let captchachk = grecaptcha.getResponse();

        if (feedbackemail.length > 0 && (feedbackemail.indexOf('@') !== -1) && (feedbackemail.indexOf('.') !== -1)) {
            $('.contactmeemail').css("border","1px solid black");
            $('.contactemailerror').css("font-style","italic");
            $('.contactemailerror').hide();
            $('.contactemailerror').css("margin","60px -195px 0 0");
        } else {
            $('.contactmeemail').css("border","3px solid red");
            $('.contactemailerror').show();
            $('.contactemailerror').css("font-style","italic");
            $('.contactemailerror').css("margin","60px 10px 0 0");
            $('.contactemailerror').delay(900).queue( (next) => {
                $('.contactemailerror').css("font-style","normal");
                next();
            event.preventDefault();
            });
        };

        if (feedbacktext.length > 0) {
            $('.contactmefeedback').css("border","0");
        } else {
            $('.contactmefeedback').css("border","2px solid red");
            event.preventDefault();
        }

        if (captchachk.length > 0) {
            $('.contactrecaptchabox').css("border","0");
        } else {
            $('.contactrecaptchabox').css("border","2px solid red");
            event.preventDefault();
        };

        /*  DECIDED TO SEND FEEDBACK FROM HTML FORM DIRECTLY TO PYTHON FLASK FOR PRACTICE. USED THIS ONLY FOR CSS FEATURES */

        if (feedbackemail.length > 0 && (feedbackemail.indexOf('@') !== -1) && (feedbackemail.indexOf('.') !== -1) && feedbacktext.length > 0 && captchachk.length > 0) {
            let feedbackdata = {'FirstName' : feedbackname, 'Email' : feedbackemail, 'Feedback' : feedbacktext, 'Recaptcha': captchachk}
            $.ajax({
                url: '/sendfeedback',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(feedbackdata),
                success: function(response) {
                    $('.commentboxpic').hide();
                    $('.contactmenametext').hide();
                    $('.contactmename').hide();
                    $('.contactmeemailtext').hide();
                    $('.contactmeemail').hide();
                    $('.contactemailerror').hide();
                    $('.contactmefeedback').hide();
                    $('.contactmesubmit').hide();
                    $('.contactrecaptchabox').hide();
                    if (response == "Feedback Success") {
                        $('.feedbackresponsebox').css('visibility','visible');
                        $('.feedbackresponse').css('visibility','visible');
                        $('.contactmeheader').delay(10000).queue( (next) => {
                            window.location.replace('/');
                            next();
                        });
                    } else if (response == "Feedback Failure") {
                        $('.feedbackresponsebox').css('visibility','visible');
                        $('.feedbackresponse2').css('visibility','visible');
                        $('.contactmeheader').delay(10000).queue( (next) => {
                            window.location.replace('/');
                            next();
                        });
                    }
                }
            })
        } else {
            event.preventDefault();
        }
    });
});