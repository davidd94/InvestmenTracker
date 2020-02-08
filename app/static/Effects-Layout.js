$(document).ready(() => {
    $('.homebutton').on('mouseenter', () => {
        $('.homeicon').css("left", "10px");
        $('.homebutton').css("font-style", "italic");
    });
    $('.homebutton').on('mouseleave', () => {
        $('.homeicon').css("left", "-80px");
        $('.homebutton').css("font-style", "normal");
    });


    $('.newsbutton').on('mouseenter', () => {
        $('.newsicon').css("left", "10px");
        $('.newsbutton').css("font-style", "italic");
    });
    $('.newsbutton').on('mouseleave', () => {
        $('.newsicon').css("left", "-80px");
        $('.newsbutton').css("font-style", "normal");
    });


    $('.educationalbutton').on('mouseenter', () => {
        $('.eduicon').css("left", "10px");
        $('.educationalbutton').css("font-style", "italic");
    });
    $('.educationalbutton').on('mouseleave', () => {
        $('.eduicon').css("left", "-80px");
        $('.educationalbutton').css("font-style", "normal");
    });


    $('.aboutmebutton').on('mouseenter', () => {
        $('.meicon').css("left", "10px");
        $('.aboutmebutton').css("font-style", "italic");
    });
    $('.aboutmebutton').on('mouseleave', () => {
        $('.meicon').css("left", "-80px");
        $('.aboutmebutton').css("font-style", "normal");
    });


    $('.contactme').on('mouseenter', () => {
        $('.contacticon').css("left", "10px");
        $('.contactme').css("font-style", "italic");
    });
    $('.contactme').on('mouseleave', () => {
        $('.contacticon').css("left", "-80px");
        $('.contactme').css("font-style", "normal");
    });

        /* ADDITIONAL FEATURES FROM 'LOGGED IN' EFFECTS */

    $('.personalstockbutton').on('mouseenter', () => {
        $('.stockicon').css("left", "-2px");
        $('.personalstockbutton').css("font-style", "italic");
    });
    $('.personalstockbutton').on('mouseleave', () => {
        $('.stockicon').css("left", "-80px");
        $('.personalstockbutton').css("font-style", "normal");
    });


    $('#profilescroll, .profilearrowicon, .profileusericon').on('click', () => {
        $('.profilescrolldownbox').slideToggle("fast");

        let innercss = $('.profilebox').css("z-index");
        if (innercss === "1000") {
            $('.profilebox').css({"z-index" : "1"});
        } else {
            $('.profilebox').css({"z-index" : "1000"});
            
        };
    });

    
    /*
    $('.profilebox').on('focusout', () => {
        $('.profilescrolldownbox').slideUp("fast");
        $('.profilebox').css({"z-index" : "1"});
    */

    $('.profileinfo').on('click', () => {
        window.location.replace('/userprofile');
        $('.profilescrolldownbox').slideUp("fast");
        $('.profilebox').css({"z-index" : "1"});
    });

    $('.profileportfolio').on('click', () => {
        window.location.replace('/userportfolio');
        $('.profilescrolldownbox').slideUp("fast");
        $('.profilebox').css({"z-index" : "1"});
    });

    $('.profilelogout').on('click', () => {
        $.ajax({
            url: '/loggedout',
            type: 'GET',
            success: function(response) {
                $('.profilescrolldownbox').slideUp("fast");
                $('.profilebox').css({"z-index" : "1"});
                window.location.replace(response);
            }
        });
    });
});