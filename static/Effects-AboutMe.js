$(document).ready(() => {

    /* BEGINNING BIO SECTION */

    $('.learntext, .learnarrow').on('click', () => {
        /* HIDES BACK 'THE BEGINNING' TEXT/ARROWS */
        $('.beginp1, .beginp2').css("left","-800px");
        $('.beginp1, .beginp2').css("font-style","italic");

        $('.learntext, .learnarrow').css("left","-800px");
        $('.learntext').css("font-style","italic");

        /* DISPLAYS 'LEARNING PHASE' TEXT/ARROWS */
        $('.learnp1').css("left","0px");
        $('.learnp1').css("font-style","normal");

        $('.begintext').css("left","13px");
        $('.begintext').css("font-style","normal");
        $('.beginarrow').css("left","7px");

        $('.learntext2').css("left","70px");
        $('.learntext2').css("font-style","normal");
        $('.learntext2').css("pointer-events","auto");
        $('.learnarrow2').css("left","260px");
        $('.learnarrow2').css("pointer-events","auto");
    });

    /* LEARNING PHASE 1 BIO SECTION */

    $('.begintext, .beginarrow').on('click', () => {
        /* DISPLAYS 'THE BEGINNING' TEXT/ARROWS */
        $('.beginp1, .beginp2').css("left","0px");
        $('.beginp1, .beginp2').css("font-style","normal");

        $('.learntext').css("left","40px");
        $('.learnarrow').css("left","200px");
        $('.learntext').css("font-style","normal");

        /* HIDES BACK 'LEARNING PHASE 1' TEXT/ARROWS */
        $('.learnp1').css("left","800px");
        $('.learnp1').css("font-style","italic");

        $('.begintext').css("left","800px");
        $('.begintext').css("font-style","italic");
        $('.beginarrow').css("left","800px");
        $('.learntext2').css("left","400px");
        $('.learntext2').css("font-style","italic");
        $('.learntext2').css("pointer-events","none");
        $('.learnarrow2').css("left","800px");
        $('.learnarrow2').css("pointer-events","none");

    });

    $('.learntext2, .learnarrow2').on('click', () => {
        /* DISPLAYS 'LEARNING PHASE 2' TEXT/ARROWS */
        $('.learn2p1').css("left","0px");
        $('.learn2p1').css("font-style","normal");

        $('.backlearntext').css("left","20px");
        $('.backlearnarrow').css("left","10px");
        $('.backlearntext').css("font-style","normal");
        $('.progtext').css("left","50px");
        $('.progtext').css("font-style","normal");
        $('.progtext').css("pointer-events","auto");
        $('.progarrow').css("left","260px");
        $('.progarrow').css("pointer-events","auto");

        /* HIDES BACK 'LEARNING PHASE 1' TEXT/ARROWS */
        $('.learnp1').css("left","-800px");
        $('.learnp1').css("font-style","italic");

        $('.begintext').css("left","-400px");
        $('.begintext').css("font-style","italic");
        $('.begintext').css("pointer-events","none");
        $('.beginarrow').css("left","-400px");
        $('.beginarrow').css("pointer-events","none");
        $('.learntext2').css("left","-800px");
        $('.learntext2').css("font-style","italic");
        $('.learnarrow2').css("left","-800px");
    });

    /* LEARNING PHASE 2 BIO SECTION */

    $('.backlearnarrow, .backlearntext').on('click', () => {
        /* HIDES 'LEARNING PHASE 2' TEXT/ARROWS */
        $('.learn2p1').css("left","800px");
        $('.learn2p1').css("font-style","italic");

        $('.backlearntext').css("left","800px");
        $('.backlearntext').css("font-style","italic");
        $('.backlearnarrow').css("left","800px");

        $('.progtext').css("left","400px");
        $('.progtext').css("font-style","italic");
        $('.progtext').css("pointer-events","none");
        $('.progarrow').css("left","400px");
        $('.progarrow').css("pointer-events","none");

        /* DISPLAYS 'LEARNING PHASE 1' TEXT/ARROWS */
        $('.learnp1').css("left","0px");
        $('.learnp1').css("font-style","normal");

        $('.begintext').css("left","13px");
        $('.begintext').css("font-style","normal");
        $('.begintext').css("pointer-events","auto");
        $('.beginarrow').css("left","7px");
        $('.beginarrow').css("pointer-events","auto");
        $('.learntext2').css("left","70px");
        $('.learntext2').css("font-style","normal");
        $('.learnarrow2').css("left","260px");
    });

    $('.progarrow, .progtext').on('click', () => {
        /* HIDES 'LEARNING PHASE 2' TEXT/ARROWS */
        $('.learn2p1').css("left","-800px");
        $('.learn2p1').css("font-style","italic");

        $('.backlearntext').css("left","-800px");
        $('.backlearntext').css("font-style","italic");
        $('.backlearntext').css("pointer-events","none");
        $('.backlearnarrow').css("left","-800px");
        $('.backlearnarrow').css("pointer-events","none");
        $('.progtext').css("left","-800px");
        $('.progtext').css("font-style","italic");
        $('.progarrow').css("left","-800px");

        /* DISPLAYS 'PROGRAMMING & FUTURE' TEXT/ARROWS */
        $('.progp1').css("left","0px");
        $('.progp1').css("font-style","normal");
        $('.progp2').css("left","0px");
        $('.progp2').css("font-style","normal");

        $('.backlearntext2').css("left","13px");
        $('.backlearntext2').css("font-style","normal");
        $('.backlearnarrow2').css("left","7px");
    });

    /* PROGRAMMING & FUTURE BIO SECTION */

    $('.backlearnarrow2, .backlearntext2').on('click', () => {
        /* HIDES 'PROGRAMMING & FUTURE' TEXT/ARROWS */
        $('.progp1').css("left","800px");
        $('.progp1').css("font-style","italic");
        $('.progp2').css("left","800px");
        $('.progp2').css("font-style","italic");

        $('.backlearntext2').css("left","800px");
        $('.backlearntext2').css("font-style","italic");
        $('.backlearnarrow2').css("left","800px");

        /* DISPLAYS 'LEARNING PHASE PT2' BIO SECTION */
        $('.learn2p1').css("left","0px");
        $('.learn2p1').css("font-style","normal");

        $('.backlearntext').css("left","20px");
        $('.backlearntext').css("font-style","normal");
        $('.backlearntext').css("pointer-events","auto");
        $('.backlearnarrow').css("left","10px");
        $('.backlearnarrow').css("pointer-events","auto");
        $('.progtext').css("left","50px");
        $('.progtext').css("font-style","normal");
        $('.progarrow').css("left","260px");
    });
});