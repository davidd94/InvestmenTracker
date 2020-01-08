$(document).ready(() => {

    /* ALL INPUT TEXT CHANGE ON BLUR */

    $('.userinfo, .passwordinfo, .newusername, .newfirstname, .newlastname, .newpassword, .retypenewpw, .newemailaddress, .retypeemail, .forgotlastname, .forgotemailaddress').blur(function() {
        if (($(this)[0].value).length > 0) {
            $(this).css('color','black');
            $(this).css('font-style','normal');
        } else {
            $(this).css('font-style','italic');
        };
    });

    /* STOCK SEARCH DROP DOWN MENU */

    $('#search').on('click', () => {
        $('.searchdropdown').slideToggle(100);
    });

    $('#compare').on('click', () => {
        $("#search").prop('value', 'Compare');
        $('.searchdropdown').toggle();
    });

    $('#none').on('click', () => {
        $("#search").prop('value', 'Stock Search');
        $('.searchdropdown').toggle();
    });

    $('#testing').on('click', () => {
        $("#search").prop('value', 'Testing');
        $('.searchdropdown').toggle();
    });

    $('.searchbox').on('focusout', () => {
        $('.searchdropdown').slideUp("fast");
    });

    /* QUICK STOCK SEARCH TICKER BOX */

    $('.tickerbox').keypress((event) => {
        var key = event.which;
        $tickersearch = ($('.ticker')[0].value).toUpperCase();

        if (key == 13) {
            $('.searchbox').css("grid-row","3 / span 1");
            $('.tickerbox').css("grid-row","3 / span 1");
            $('.quickstockbox').css("visibility","visible");
            $('.quickstockbox').css("grid-row","4 / span 5");
            $('.quickstockbox').css("height","500px");

            $.ajax({
                url: '/scrapingstockdata',
                data: JSON.stringify($tickersearch),
                type: 'POST',
                contentType: 'application/json',
                success: function(response) {
                    if (response) {
                        let pricepercentdiff = ((Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price'])).toFixed(2)
                        let pricepercentdiff2 = (Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price'])

                        $('.quickstockname').text(response['CompanyName']);
                        $('.quickstockticker').text('(' + $tickersearch + ')');
                        $('.quickstockprice').text('$' + response['Price']);
                        if (pricepercentdiff2 > 0) {
                            $('.stockincreasearrow').css('visibility','visible');
                            $('.stockdecreasearrow').css('visibility','hidden');
                            $('.quickstockpricediff').css('color','green');
                            $('.quickstockpricediff').text('+' + pricepercentdiff + ' (+' + response['Change'] + ')');
                        } else if (pricepercentdiff2 < 0) {
                            $('.stockdecreasearrow').css('visibility','visible');
                            $('.stockincreasearrow').css('visibility','hidden');
                            $('.quickstockpricediff').css('color','red');
                            $('.quickstockpricediff').text(pricepercentdiff + ' (' + response['Change'] + ')');
                        } else {
                            $('.stockincreasearrow').css('visibility','hidden');
                            $('.stockdecreasearrow').css('visibility','hidden');
                            $('.quickstockpricediff').css('color','black');
                            $('.quickstockpricediff').text(pricepercentdiff + ' (' + response['Change'] + ')');
                        };

                        $('.Indexname').text(response['Index']);
                        $('.Marketcap').text(response['Market Cap']);
                        $('.Incomeval').text(response['Income']);
                        $('.BVal').text(response['Book/sh']);
                        $('.Cashval').text(response['Cash/sh']);
                        $('.Dividendval').text(response['Dividend']);
                        $('.Dividendperc').text(response['Dividend %']);
                        $('.totalemployees').text(response['Employees']);

                        $('.PEval').text(response['P/E']);
                        $('.PEgrowth').text(response['PEG']);
                        $('.PSval').text(response['P/S']);
                        $('.PBval').text(response['P/B']);
                        $('.PCval').text(response['P/C']);
                        $('.PFCFval').text(response['P/FCF']);
                        $('.debttoeq').text(response['Debt/Eq']);
                        $('.LTdebttoeq').text(response['LT Debt/Eq']);

                        $('.EPS-ttm').text(response['EPS (ttm)']);
                        $('.EPS-EY').text(response['EPS next Y']);
                        $('.EPS-EQ').text(response['EPS next Q']);
                        $('.EPS-GY').text(response['EPS this Y']);
                        $('.EPS-GY2').text(response['EPS next Y']);
                        $('.EPS-G5Y').text(response['EPS next 5Y']);
                        $('.EPS-P5Y').text(response['EPS past 5Y']);
                        $('.Sales-P5Y').text(response['Sales past 5Y']);
                        $('.Sales-GQ').text(response['Sales Q/Q']);
                        $('.EPS-GQ').text(response['EPS Q/Q']);

                        $('.insiderown').text(response['Insider Own']);
                        $('.Insidertrans').text(response['Insider Trans']);
                        $('.Instiown').text(response['Inst Own']);
                        $('.Institrans').text(response['Inst Trans']);
                        $('.ROAval').text(response['ROA']);
                        $('.ROEval').text(response['ROE']);
                        $('.ROIval').text(response['ROI']);
                        $('.Grossmargin').text(response['Gross Margin']);
                        $('.Opermargin').text(response['Oper. Margin']);
                        $('.Profitmargin').text(response['Profit Margin']);

                        if (response == "Failed to find stock/company symbol!" || response == "A problem has occurred with our 'Data Analysis'! Please send a feed back through our Contact Us page.") {
                            $('.quickstockname').text('Company Not Found');
                            $('.quickstockticker').text('????');
                            $('.quickstockprice').text('? (?%)');

                            $('.Indexname').text('-');
                            $('.Marketcap').text('-');
                            $('.Incomeval').text('-');
                            $('.BVal').text('-');
                            $('.Cashval').text('-');
                            $('.Dividendval').text('-');
                            $('.Dividendperc').text('-');
                            $('.totalemployees').text('-');

                            $('.PEval').text('-');
                            $('.PEgrowth').text('-');
                            $('.PSval').text('-');
                            $('.PBval').text('-');
                            $('.PCval').text('-');
                            $('.PFCFval').text('-');
                            $('.debttoeq').text('-');
                            $('.LTdebttoeq').text('-');

                            $('.EPS-ttm').text('-');
                            $('.EPS-EY').text('-');
                            $('.EPS-EQ').text('-');
                            $('.EPS-GY').text('-');
                            $('.EPS-GY2').text('-');
                            $('.EPS-G5Y').text('-');
                            $('.EPS-P5Y').text('-');
                            $('.Sales-P5Y').text('-');
                            $('.Sales-GQ').text('-');
                            $('.EPS-GQ').text('-');

                            $('.insiderown').text('-');
                            $('.Insidertrans').text('-');
                            $('.Instiown').text('-');
                            $('.Institrans').text('-');
                            $('.ROAval').text('-');
                            $('.ROEval').text('-');
                            $('.ROIval').text('-');
                            $('.Grossmargin').text('-');
                            $('.Opermargin').text('-');
                            $('.Profitmargin').text('-');
                            alert(response)
                        }
                    }
                },
            });
        };
    });

    $('.quickstockboxclose').click(() => {
        $('.searchbox').css("grid-row","4 / span 1");
        $('.tickerbox').css("grid-row","4 / span 1");
        $('.quickstockbox').css("grid-row","5 / span 5");
        $('.quickstockbox').css("height","1px");
        $('.quickstockbox').css("visibility","hidden");

        $('.quickstockticker').text('????');
        $('.quickstockprice').text('? (?%)');

        $('.Indexname').text('-');
        $('.Marketcap').text('-');
        $('.Incomeval').text('-');
        $('.BVal').text('-');
        $('.Cashval').text('-');
        $('.Dividendval').text('-');
        $('.Dividendperc').text('-');
        $('.totalemployees').text('-');

        $('.PEval').text('-');
        $('.PEgrowth').text('-');
        $('.PSval').text('-');
        $('.PBval').text('-');
        $('.PCval').text('-');
        $('.PFCFval').text('-');
        $('.debttoeq').text('-');
        $('.LTdebttoeq').text('-');

        $('.EPS-ttm').text('-');
        $('.EPS-EY').text('-');
        $('.EPS-EQ').text('-');
        $('.EPS-GY').text('-');
        $('.EPS-GY2').text('-');
        $('.EPS-G5Y').text('-');
        $('.EPS-P5Y').text('-');
        $('.Sales-P5Y').text('-');
        $('.Sales-GQ').text('-');
        $('.EPS-GQ').text('-');

        $('.insiderown').text('-');
        $('.Insidertrans').text('-');
        $('.Instiown').text('-');
        $('.Institrans').text('-');
        $('.ROAval').text('-');
        $('.ROEval').text('-');
        $('.ROIval').text('-');
        $('.Grossmargin').text('-');
        $('.Opermargin').text('-');
        $('.Profitmargin').text('-');
    });


    /* ALL USER-LOGIN BOX EFFECTS (USER NOT LOGGED IN) */
    $('.createnewuser').on('click', () => {
        $('.newacctbox').removeClass('invisible');
        $('.newacctbox').fadeOut(1);
        $('.newacctbox').fadeIn(1500);
        $('#success2').css('top', '150px');
        $('#incorrlogin').css('top', '150px');
        $('#exname').css('top', '150px');
        $('#exemail').css('top', '150px');
        $('#success').css('top', '150px');
        $('#acctconfirm').css('top', '150px');
        $('#failedloginbox').css('top', '150px');

        $('.newusername')[0].value = $('.userinfo')[0].value;
        $('.passwordinfo')[0].value = '';
    });

    $('.backarrow1').on('click', () => {
        $('.newacctbox').fadeOut(1000);
        $('#exname').css('top', '150px');
        $('#incorrlogin').css('top', '150px');
        $('#exemail').css('top', '150px');
        $('#success').css('top', '150px');
        $('#success2').css('top', '150px');
        $('#acctconfirm').css('top', '150px');
        $('#failedloginbox').css('top', '150px');

        $('.newusername')[0].value = '';
        $('.newfirstname')[0].value = '';
        $('.newlastname')[0].value = '';
        $('.newpassword')[0].value = '';
        $('.retypenewpw')[0].value = '';
        $('.newemailaddress')[0].value = '';
        $('.retypeemail')[0].value = '';
    });


    $('.forgotpw').on('click', () => {
        $('.forgotpwbox').removeClass('invisible');
        $('.forgotpwbox').fadeOut(1);
        $('.forgotpwbox').fadeIn(1500);
        $('#success2').css('top', '150px');
        $('#incorrlogin').css('top', '150px');
        $('#exname').css('top', '150px');
        $('#exemail').css('top', '150px');
        $('#success').css('top', '150px');
        $('#failedloginbox').css('top', '150px');

        $('.userinfo')[0].value = '';
        $('.passwordinfo')[0].value = '';
    });

    $('.backarrow3').on('click', () => {
        $('.forgotpwbox').fadeOut(1000);
        $('#exname').css('top', '150px');
        $('#incorrlogin').css('top', '150px');
        $('#exemail').css('top', '150px');
        $('#success').css('top', '150px');
        $('#success2').css('top', '150px');
        $('#failedloginbox').css('top', '150px');
        $('.forgotlastname')[0].value = '';
        $('.forgotemailaddress')[0].value = '';
    });

    var flag = true;
    $('.loginbox').on('mouseenter', () => {
        if (flag === true) {
            $('.loginbox').animate({
                height: "97%",
            }, 500, function () {
                flag = false;
            });
        }
    });

    $('.loginbox').on('mouseleave', () => {
        if (flag === false) {
            $('.loginbox').animate({
                height: "55%",
            }, 500, function () {
                flag = true;
            });
        }
    });
});