$(document).ready(() => {
    function webscrapeportfolio(stock) {    /*FUNCTION TO ALLOW SIMULTANEOUS APPLICATION OF (WEBSCRAPE) AJAX DATA TO EACH INDIVIDUAL DYNAMIC HTML ROWS */
        $.ajax({
            url: '/scrapingstockdata',
            data: JSON.stringify(stock),
            type: 'POST',
            contentType: 'application/json',
            success: function(response) {
                if (response) {
                    let pricediff = (Number(response['Price']) - Number(response['Prev Close'])).toFixed(2);
                    let pricepercentdiff = ((Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price'])).toFixed(2);
                    let pricepercentdiff2 = (Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price']);
                    
                    let currentprice = Number(response['Price']);
                    let purchase = Number($('#purchasetext' + stock)[0].textContent);
                    let quantity = Number($('#quantitytext' + stock)[0].textContent);
                    let totalgains = Number(((currentprice - purchase) * quantity).toFixed(2));
                    let gainsperc = Number(((currentprice - purchase) / currentprice * 100).toFixed(2));

                    if (pricepercentdiff2 > 0) {
                        $('#createdchange' + stock).css('color','green');
                    } else if (pricepercentdiff2 < 0) {
                        $('#createdchange' + stock).css('color','red');
                    } else {
                        $('#createdchange' + stock).css('color','black');
                    };

                    if (totalgains > 0) {
                        $('#createdgains' + stock).css('color','green');
                    } else if (totalgains < 0) {
                        $('#createdgains' + stock).css('color','red');
                    } else {
                        $('#createdgains' + stock).css('color','black');
                    };

                    if (gainsperc > 0) {
                        $('#createdgains2' + stock).css('color','green');
                    } else if (gainsperc < 0) {
                        $('#createdgains2' + stock).css('color','red');
                    } else {
                        $('#createdgains2' + stock).css('color','black');
                    };


                    $('#createdcompname' + stock).text(response['CompanyName']);
                    $('#createdprice' + stock).text(currentprice);
                    $('#createdchange' + stock).text(pricediff + " ( " + pricepercentdiff + "% )");
                    $('#createdshsfloat' + stock).text(response['Shs Float']);
                    $('#createdshsouts' + stock).text(response['Shs Outstand']);
                    $('#createdvolume' + stock).text(response['Volume']);

                    $('#createdgains' + stock).text('$ ' + totalgains);
                    $('#createdgains2' + stock).text(gainsperc + ' %');

                    if (response == "Failed to find stock/company symbol!" || response == "A problem has occurred with our 'Data Analysis'! Please send a feed back through our Contact Us page.") {
                        $('#createdcompname' + stock).text('N/A');
                        $('#createdprice' + stock).text('N/A');
                        $('#createdchange' + stock).text('N/A');
                        $('#createdshsfloat' + stock).text('N/A');
                        $('#createdshsouts' + stock).text('N/A');
                        $('#createdvolume' + stock).text('N/A');
                    }

                }
            },
        });
    }
    $.ajax({   /* AUTOMATICALLY LOADS USER'S PERSONAL STOCK INFO */
        url: '/retrievestockinfo',
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            let stockliblength = response.length;
            let allstocks = [];

            for (i = 0 ; i < stockliblength ; i++) {
                let stocklib = response[i];
                let stockticker = stocklib['StockSym'];
                allstocks.push(stockticker);

                let stockdate = stocklib['StockData']['Date'];
                let purchase = Number(stocklib['StockData']['PurchaseCost']);
                let quantity = Number(stocklib['StockData']['Quantity']);
                let totalval = (purchase * quantity).toFixed(2);
                let notes = stocklib['StockData']['Notes'];

                if (totalval > 0) {
                    $('#createdtotal' + stockticker).css('color','green');
                } else if (totalval < 0) {
                    $('#createdtotal' + stockticker).css('color','red');
                } else {
                    $('#createdtotal' + stockticker).css('color','black');
                };
                
                
                    /* AUTOFILLED LEFT TABLE DATA */
                $('.lefttab').append(($('<tr>')
                    .attr('id',('lefttabrow' + stockticker))
                    .attr('class','lefttabrow')
                    .append($('<td>')
                        .attr('id', ('createdstock' + stockticker))
                        .attr('class', 'createdstock')
                        .text(stockticker)
                        .append($('<button>')
                            .attr('id',('deleteicon' + stockticker))
                            .attr('class','deleteicon')
                            .attr('input','button')
                        )
                    )
                    .append($('<td>')
                        .attr('id', ('createdcompname' + stockticker))
                        .attr('class', 'createdcompname')
                    )
                    .append($('<td>')
                        .attr('id', ('createdprice' + stockticker))
                        .attr('class', 'createdprice')
                    )
                    .append($('<td>')
                        .attr('id', ('createdchange' + stockticker))
                        .attr('class', 'createdchange')
                    )
                    .append($('<td>')
                        .attr('id', ('createdshsfloat' + stockticker))
                        .attr('class', 'createdshsfloat')
                    )
                    .append($('<td>')
                        .attr('id', ('createdshsouts' + stockticker))
                        .attr('class', 'createdshsouts')
                    )
                    .append($('<td>')
                        .attr('id', ('createdvolume' + stockticker))
                        .attr('class', 'createdvolume')
                    )
                )
                );

                /* AUTOFILLED RIGHT TABLE DATA */

                var $currentDate = new Date();
                var $year = $currentDate.getFullYear();
                var $month = $currentDate.getMonth()+1;
                var $day = $currentDate.getDate();
                var presentdate = ($year + 1) + '-' + $month + '-' + $day;

                $('.righttab').append($('<tr>')
                    .attr('id',('righttabrow' + stockticker))
                    .attr('class','createdrightrow')
                    .append($('<td>')
                        .attr('id', ('createddate' + stockticker))
                        .attr('class', 'createddate')
                        .append($('<button>')
                            .attr('id',('dateicon' + stockticker))
                            .attr('class','dateicon')
                            .attr('input','button')
                        )
                        .append($('<p>').text(stockdate).attr('class','datetext').attr('id','datetext' + stockticker))
                        .append($('<input>')
                            .attr('type','date')
                            .attr('id',('dateinput' + stockticker))
                            .attr('class','dateinput')
                            .attr('max',presentdate)
                        )
                    )
                
                /* EMPTY/USER FILLED RIGHT TABLE DATA */
                    .append($('<td>')
                        .attr('id', ('createpurchase' + stockticker))
                        .attr('class', 'createpurchase')
                        .append($('<button>')
                                .attr('id',('purchaseicon' + stockticker))
                                .attr('class','purchaseicon')
                                .attr('input','button')
                        )
                        .append($('<p>').text(purchase).attr('class','purchasetext').attr('id','purchasetext' + stockticker))
                        .append($('<input>')
                            .attr('type','number')
                            .attr('id',('purchaseinput' + stockticker))
                            .attr('class','purchaseinput')
                        )
                    )
                    .append($('<td>')
                        .attr('id', ('createquantity' + stockticker))
                        .attr('class', 'createquantity')
                        .append($('<button>')
                            .attr('id',('quantityicon' + stockticker))
                            .attr('class','quantityicon')
                            .attr('input','button')
                        )
                        .append($('<p>').text(quantity).attr('class','quantitytext').attr('id','quantitytext' + stockticker))
                        .append($('<input>')
                            .attr('type','number')
                            .attr('id',('quantityinput' + stockticker))
                            .attr('class','quantityinput')
                        )
                    )
                    .append($('<td>')
                        .attr('id', ('createdtotal' + stockticker))
                        .attr('class', 'createdtotal')
                        .text(totalval)
                    )
                    .append($('<td>')
                        .attr('id', ('createdgains' + stockticker))
                        .attr('class', 'createdgains')
                        .text('$')
                    )
                    .append($('<td>')
                        .attr('id', ('createdgains2' + stockticker))
                        .attr('class', 'createdgains2')
                        .text('%')
                    )
                    .append($('<td>')
                        .attr('id', ('createnotes' + stockticker))
                        .attr('class', 'createnotes')
                        .append($('<button>')
                            .attr('id',('notesicon' + stockticker))
                            .attr('class','notesicon')
                            .attr('input','button')
                        )
                        .append($('<p>').text(notes).attr('class','notestext').attr('id','notestext' + stockticker))
                        .append($('<input>')
                            .attr('type','text')
                            .attr('id',('notesinput' + stockticker))
                            .attr('class','notesinput')
                            .attr('maxlength','20')
                        )
                    )
                );

            };
            
            /* LOOP TO SIMULTANEOUSLY EXECUTE FUNCTION */
            for (i = 0 ; i < allstocks.length ; i++ ) {
                let specificstock = allstocks[i];
                webscrapeportfolio(specificstock);
            };
        },
    });


    /* ADD ROWS ON CLICK */
    $('#addstockbutton').on('click', () => {
        var addstock = $('#addstockbox')[0].value;
        var numofrows = ($('.lefttabrow')).length;

        if (addstock == "") {
            alert("You must insert a valid stock ticker!")
        } else if (numofrows < 15) {
            try {       /* 'TRY' METHOD USED TO AVOID USERS DUPLICATING STOCK INPUTS */
                if ($('#createdstock' + addstock)[0].innerText != addstock) { /* THROWS AN ERROR FOR FIRST STOCK ADD CAUSE THERE IS NO STOCK TO VERIFY FROM. THUS 'CATCH' METHOD WAS REQUIRED */
                    $('#addstockbox')[0].value = "";

                        /* AUTOFILLED LEFT TABLE DATA */
                    $('.lefttab').append(($('<tr>')
                        .attr('id',('lefttabrow' + addstock))
                        .attr('class','lefttabrow')
                        .append($('<td>')
                            .attr('id', ('createdstock' + addstock))
                            .attr('class', 'createdstock')
                            .text(addstock)
                            .append($('<button>')
                                .attr('id',('deleteicon' + addstock))
                                .attr('class','deleteicon')
                                .attr('input','button')
                            )
                        )
                        .append($('<td>')
                            .attr('id', ('createdcompname' + addstock))
                            .attr('class', 'createdcompname')
                        )
                        .append($('<td>')
                            .attr('id', ('createdprice' + addstock))
                            .attr('class', 'createdprice')
                        )
                        .append($('<td>')
                            .attr('id', ('createdchange' + addstock))
                            .attr('class', 'createdchange')
                        )
                        .append($('<td>')
                            .attr('id', ('createdshsfloat' + addstock))
                            .attr('class', 'createdshsfloat')
                        )
                        .append($('<td>')
                            .attr('id', ('createdshsouts' + addstock))
                            .attr('class', 'createdshsouts')
                        )
                        .append($('<td>')
                            .attr('id', ('createdvolume' + addstock))
                            .attr('class', 'createdvolume')
                        )
                    )
                    );

                            /* AUTOFILLED RIGHT TABLE DATA */

                    var $currentDate = new Date();
                    var $year = $currentDate.getFullYear();
                    var $month = $currentDate.getMonth()+1;
                    var $day = $currentDate.getDate();
                    var $fullDate = $month + "/" + $day + "/" + $year;
                    var presentdate = ($year + 1) + '-' + $month + '-' + $day;

                    $('.righttab').append($('<tr>')
                        .attr('id',('righttabrow' + addstock))
                        .attr('class','createdrightrow')
                        .append($('<td>')
                            .attr('id', ('createddate' + addstock))
                            .attr('class', 'createddate')
                            .append($('<button>')
                                .attr('id',('dateicon' + addstock))
                                .attr('class','dateicon')
                                .attr('input','button')
                            )
                            .append($('<p>').text($fullDate).attr('class','datetext').attr('id','datetext' + addstock))
                            .append($('<input>')
                                .attr('type','date')
                                .attr('id',('dateinput' + addstock))
                                .attr('class','dateinput')
                                .attr('max',presentdate)
                            )
                        )
                    
                    /* EMPTY/USER FILLED RIGHT TABLE DATA */
                        .append($('<td>')
                            .attr('id', ('createpurchase' + addstock))
                            .attr('class', 'createpurchase')
                            .append($('<button>')
                                    .attr('id',('purchaseicon' + addstock))
                                    .attr('class','purchaseicon')
                                    .attr('input','button')
                            )
                            .append($('<p>').text('-').attr('class','purchasetext').attr('id','purchasetext' + addstock))
                            .append($('<input>')
                                .attr('type','number')
                                .attr('id',('purchaseinput' + addstock))
                                .attr('class','purchaseinput')
                            )
                        )
                        .append($('<td>')
                            .attr('id', ('createquantity' + addstock))
                            .attr('class', 'createquantity')
                            .append($('<button>')
                                .attr('id',('quantityicon' + addstock))
                                .attr('class','quantityicon')
                                .attr('input','button')
                            )
                            .append($('<p>').text('-').attr('class','quantitytext').attr('id','quantitytext' + addstock))
                            .append($('<input>')
                                .attr('type','number')
                                .attr('id',('quantityinput' + addstock))
                                .attr('class','quantityinput')
                            )
                        )
                        .append($('<td>')
                            .attr('id', ('createdtotal' + addstock))
                            .attr('class', 'createdtotal')
                        )
                        .append($('<td>')
                            .attr('id', ('createdgains' + addstock))
                            .attr('class', 'createdgains')
                        )
                        .append($('<td>')
                            .attr('id', ('createdgains2' + addstock))
                            .attr('class', 'createdgains2')
                        )
                        .append($('<td>')
                            .attr('id', ('createnotes' + addstock))
                            .attr('class', 'createnotes')
                            .append($('<button>')
                                .attr('id',('notesicon' + addstock))
                                .attr('class','notesicon')
                                .attr('input','button')
                            )
                            .append($('<p>').text('-').attr('class','notestext').attr('id','notestext' + addstock))
                            .append($('<input>')
                                .attr('type','text')
                                .attr('id',('notesinput' + addstock))
                                .attr('class','notesinput')
                                .attr('maxlength','20')
                            )
                        )
                    );


                        /* WEBSCRAPE FOR DATA */

                    $.ajax({
                        url: '/scrapingstockdata',
                        data: JSON.stringify(addstock),
                        type: 'POST',
                        contentType: 'application/json',
                        success: function(response) {
                            if (response) {
                                let pricediff = (Number(response['Price']) - Number(response['Prev Close'])).toFixed(2);
                                let pricepercentdiff = ((Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price'])).toFixed(2);
                                let pricepercentdiff2 = (Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price']);

                                if (pricepercentdiff2 > 0) {
                                    $('#createdchange' + addstock).css('color','green');
                                } else if (pricepercentdiff2 < 0) {
                                    $('#createdchange' + addstock).css('color','red');
                                } else {
                                    $('#createdchange' + addstock).css('color','black');
                                };

                                $('#createdcompname' + addstock).text(response['CompanyName']);
                                $('#createdprice' + addstock).text(response['Price']);
                                $('#createdchange' + addstock).text("$" + pricediff + " (" + pricepercentdiff + "%)");
                                $('#createdshsfloat' + addstock).text(response['Shs Float']);
                                $('#createdshsouts' + addstock).text(response['Shs Outstand']);
                                $('#createdvolume' + addstock).text(response['Volume']);

                                if (response == "Failed to find stock/company symbol!" || response == "A problem has occurred with our 'Data Analysis'! Please send a feed back through our Contact Us page.") {
                                    $('#createdcompname' + addstock).text('N/A');
                                    $('#createdprice' + addstock).text('N/A');
                                    $('#createdchange' + addstock).text('N/A');
                                    $('#createdshsfloat' + addstock).text('N/A');
                                    $('#createdshsouts' + addstock).text('N/A');
                                    $('#createdvolume' + addstock).text('N/A');
                                    alert(response);
                                }
                            }
                        },
                    });


                        /* SEND STOCK TICKER TO BE STORED IN DB */
                    let sendstockdata = {'Stock' : addstock, 'Date' : $fullDate};
                    $.ajax({
                        url: '/storestockinfo',
                        data: JSON.stringify(sendstockdata),
                        contentType: 'application/json',
                        type: 'POST',
                        success: function(response) {
                        },
                    });
                } else {
                    alert("You already have that stock in your portfolio.")
                }
            } catch(e) /* CATCHES THE FIRST STOCK ADDED ERROR */ {
                $('#addstockbox')[0].value = "";
                $('.lefttab').append(($('<tr>')
                    .attr('id',('lefttabrow' + addstock))
                    .attr('class','lefttabrow')
                    .append($('<td>')
                        .attr('id', ('createdstock' + addstock))
                        .attr('class', 'createdstock')
                        .text(addstock)
                        .append($('<button>')
                            .attr('id',('deleteicon' + addstock))
                            .attr('class','deleteicon')
                            .attr('input','button')
                        )
                    )
                    .append($('<td>')
                        .attr('id', ('createdcompname' + addstock))
                        .attr('class', 'createdcompname')
                    )
                    .append($('<td>')
                        .attr('id', ('createdprice' + addstock))
                        .attr('class', 'createdprice')
                    )
                    .append($('<td>')
                        .attr('id', ('createdchange' + addstock))
                        .attr('class', 'createdchange')
                    )
                    .append($('<td>')
                        .attr('id', ('createdshsfloat' + addstock))
                        .attr('class', 'createdshsfloat')
                    )
                    .append($('<td>')
                        .attr('id', ('createdshsouts' + addstock))
                        .attr('class', 'createdshsouts')
                    )
                    .append($('<td>')
                        .attr('id', ('createdvolume' + addstock))
                        .attr('class', 'createdvolume')
                    )
                )
                );

                        /* AUTOFILLED RIGHT TABLE DATA */

                var $currentDate = new Date();
                var $year = $currentDate.getFullYear();
                var $month = $currentDate.getMonth()+1;
                var $day = $currentDate.getDate();
                var $fullDate = $month + "/" + $day + "/" + $year;
                var presentdate = ($year + 1) + '-' + $month + '-' + $day;

                $('.righttab').append($('<tr>')
                    .attr('id',('righttabrow' + addstock))
                    .attr('class','createdrightrow')
                    .append($('<td>')
                        .attr('id', ('createddate' + addstock))
                        .attr('class', 'createddate')
                        .append($('<button>')
                            .attr('id',('dateicon' + addstock))
                            .attr('class','dateicon')
                            .attr('input','button')
                        )
                        .append($('<p>').text($fullDate).attr('class','datetext').attr('id','datetext' + addstock))
                        .append($('<input>')
                            .attr('type','date')
                            .attr('id',('dateinput' + addstock))
                            .attr('class','dateinput')
                            .attr('max',presentdate)
                        )
                    )
                
                /* EMPTY/USER FILLED RIGHT TABLE DATA */
                    .append($('<td>')
                        .attr('id', ('createpurchase' + addstock))
                        .attr('class', 'createpurchase')
                        .append($('<button>')
                                .attr('id',('purchaseicon' + addstock))
                                .attr('class','purchaseicon')
                                .attr('input','button')
                        )
                        .append($('<p>').text('-').attr('class','purchasetext').attr('id','purchasetext' + addstock))
                        .append($('<input>')
                            .attr('type','number')
                            .attr('id',('purchaseinput' + addstock))
                            .attr('class','purchaseinput')
                        )
                    )
                    .append($('<td>')
                        .attr('id', ('createquantity' + addstock))
                        .attr('class', 'createquantity')
                        .append($('<button>')
                            .attr('id',('quantityicon' + addstock))
                            .attr('class','quantityicon')
                            .attr('input','button')
                        )
                        .append($('<p>').text('-').attr('class','quantitytext').attr('id','quantitytext' + addstock))
                        .append($('<input>')
                            .attr('type','number')
                            .attr('id',('quantityinput' + addstock))
                            .attr('class','quantityinput')
                        )
                    )
                    .append($('<td>')
                        .attr('id', ('createdtotal' + addstock))
                        .attr('class', 'createdtotal')
                    )
                    .append($('<td>')
                        .attr('id', ('createdgains' + addstock))
                        .attr('class', 'createdgains')
                    )
                    .append($('<td>')
                        .attr('id', ('createdgains2' + addstock))
                        .attr('class', 'createdgains2')
                    )
                    .append($('<td>')
                        .attr('id', ('createnotes' + addstock))
                        .attr('class', 'createnotes')
                        .append($('<button>')
                            .attr('id',('notesicon' + addstock))
                            .attr('class','notesicon')
                            .attr('input','button')
                        )
                        .append($('<p>').text('-').attr('class','notestext').attr('id','notestext' + addstock))
                        .append($('<input>')
                            .attr('type','text')
                            .attr('id',('notesinput' + addstock))
                            .attr('class','notesinput')
                            .attr('maxlength','20')
                        )
                    )
                );


                    /* WEBSCRAPE FOR DATA */

                $.ajax({
                    url: '/scrapingstockdata',
                    data: JSON.stringify(addstock),
                    type: 'POST',
                    contentType: 'application/json',
                    success: function(response) {
                        if (response) {
                            let pricediff = (Number(response['Price']) - Number(response['Prev Close'])).toFixed(2);
                            let pricepercentdiff = ((Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price'])).toFixed(2);
                            let pricepercentdiff2 = (Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price']);

                            if (pricepercentdiff2 > 0) {
                                $('#createdchange' + addstock).css('color','green');
                            } else if (pricepercentdiff2 < 0) {
                                $('#createdchange' + addstock).css('color','red');
                            } else {
                                $('#createdchange' + addstock).css('color','black');
                            };

                            $('#createdcompname' + addstock).text(response['CompanyName']);
                            $('#createdprice' + addstock).text(response['Price']);
                            $('#createdchange' + addstock).text("$" + pricediff + " (" + pricepercentdiff + "%)");
                            $('#createdshsfloat' + addstock).text(response['Shs Float']);
                            $('#createdshsouts' + addstock).text(response['Shs Outstand']);
                            $('#createdvolume' + addstock).text(response['Volume']);

                            if (response == "Failed to find stock/company symbol!" || response == "A problem has occurred with our 'Data Analysis'! Please send a feed back through our Contact Us page.") {
                                $('#createdcompname' + addstock).text('N/A');
                                $('#createdprice' + addstock).text('N/A');
                                $('#createdchange' + addstock).text('N/A');
                                $('#createdshsfloat' + addstock).text('N/A');
                                $('#createdshsouts' + addstock).text('N/A');
                                $('#createdvolume' + addstock).text('N/A');
                                alert(response);
                            }
                        }
                    },
                });

                    /* SEND STOCK TICKER TO BE STORED IN DB */
                let sendstockdata = {'Stock' : addstock, 'Date' : $fullDate};
                $.ajax({
                    url: '/storestockinfo',
                    data: JSON.stringify(sendstockdata),
                    contentType: 'application/json',
                    type: 'POST',
                    success: function(response) {
                    },
                });

            }
        } else {
            alert("You are not allowed to add anymore temporary stock info.");
        }
    });


    /* STOCK ADD THROUGH KEYPRESS (ENTER) */
    $('#addstockbox').on('keydown', (event) => {
        var addstock = $('#addstockbox')[0].value;
        var numofrows = ($('.lefttabrow')).length;
        let keysenter = event.which;
        if (keysenter == 13 && addstock != "" && numofrows < 15) {
            try {       /* 'TRY' METHOD USED TO AVOID USERS DUPLICATING STOCK INPUTS */
                if ($('#createdstock' + addstock)[0].innerText != addstock) { /* THROWS AN ERROR FOR FIRST STOCK ADD CAUSE THERE IS NO STOCK TO VERIFY FROM. THUS 'CATCH' METHOD WAS REQUIRED */
                    $('#addstockbox')[0].value = "";
                        /* AUTOFILLED LEFT TABLE DATA */
                    $('.lefttab').append(($('<tr>')
                        .attr('id',('lefttabrow' + addstock))
                        .attr('class','lefttabrow')
                        .append($('<td>')
                            .attr('id', ('createdstock' + addstock))
                            .attr('class', 'createdstock')
                            .text(addstock)
                            .append($('<button>')
                                .attr('id',('deleteicon' + addstock))
                                .attr('class','deleteicon')
                                .attr('input','button')
                            )
                        )
                        .append($('<td>')
                            .attr('id', ('createdcompname' + addstock))
                            .attr('class', 'createdcompname')

                        )
                        .append($('<td>')
                            .attr('id', ('createdprice' + addstock))
                            .attr('class', 'createdprice')

                        )
                        .append($('<td>')
                            .attr('id', ('createdchange' + addstock))
                            .attr('class', 'createdchange')

                        )
                        .append($('<td>')
                            .attr('id', ('createdshsfloat' + addstock))
                            .attr('class', 'createdshsfloat')

                        )
                        .append($('<td>')
                            .attr('id', ('createdshsouts' + addstock))
                            .attr('class', 'createdshsouts')

                        )
                        .append($('<td>')
                            .attr('id', ('createdvolume' + addstock))
                            .attr('class', 'createdvolume')

                        )
                    )
                    );

                            /* AUTOFILLED RIGHT TABLE DATA */

                    var $currentDate = new Date();
                    var $year = $currentDate.getFullYear();
                    var $month = $currentDate.getMonth()+1;
                    var $day = $currentDate.getDate();
                    var $fullDate = $month + "/" + $day + "/" + $year;
                    var presentdate = ($year + 1) + '-' + $month + '-' + $day;

                    $('.righttab').append($('<tr>')
                        .attr('id',('righttabrow' + addstock))
                        .attr('class','createdrightrow')
                        .append($('<td>')
                            .attr('id', ('createddate' + addstock))
                            .attr('class', 'createddate')
                            .append($('<button>')
                                .attr('id',('dateicon' + addstock))
                                .attr('class','dateicon')
                                .attr('input','button')
                            )
                            .append($('<p>').text($fullDate).attr('class','datetext').attr('id','datetext' + addstock))
                            .append($('<input>')
                                .attr('type','date')
                                .attr('id',('dateinput' + addstock))
                                .attr('class','dateinput')
                                .attr('max',presentdate)
                            )
                        )
                    
                    /* EMPTY/USER FILLED RIGHT TABLE DATA */
                        .append($('<td>')
                            .attr('id', ('createpurchase' + addstock))
                            .attr('class', 'createpurchase')
                            .append($('<button>')
                                    .attr('id',('purchaseicon' + addstock))
                                    .attr('class','purchaseicon')
                                    .attr('input','button')
                            )
                            .append($('<p>').text('-').attr('class','purchasetext').attr('id','purchasetext' + addstock))
                            .append($('<input>')
                                .attr('type','number')
                                .attr('id',('purchaseinput' + addstock))
                                .attr('class','purchaseinput')
                            )
                        )
                        .append($('<td>')
                            .attr('id', ('createquantity' + addstock))
                            .attr('class', 'createquantity')
                            .append($('<button>')
                                .attr('id',('quantityicon' + addstock))
                                .attr('class','quantityicon')
                                .attr('input','button')
                            )
                            .append($('<p>').text('-').attr('class','quantitytext').attr('id','quantitytext' + addstock))
                            .append($('<input>')
                                .attr('type','number')
                                .attr('id',('quantityinput' + addstock))
                                .attr('class','quantityinput')
                            )
                        )
                        .append($('<td>')
                            .attr('id', ('createdtotal' + addstock))
                            .attr('class', 'createdtotal')
                        )
                        .append($('<td>')
                            .attr('id', ('createdgains' + addstock))
                            .attr('class', 'createdgains')

                        )
                        .append($('<td>')
                            .attr('id', ('createdgains2' + addstock))
                            .attr('class', 'createdgains2')

                        )
                        .append($('<td>')
                            .attr('id', ('createnotes' + addstock))
                            .attr('class', 'createnotes')
                            .append($('<button>')
                                .attr('id',('notesicon' + addstock))
                                .attr('class','notesicon')
                                .attr('input','button')
                            )
                            .append($('<p>').text('-').attr('class','notestext').attr('id','notestext' + addstock))
                            .append($('<input>')
                                .attr('type','text')
                                .attr('id',('notesinput' + addstock))
                                .attr('class','notesinput')
                                .attr('maxlength','20')
                            )
                        )
                    );

                        /* WEBSCRAPE FOR DATA */
                    $.ajax({
                        url: '/scrapingstockdata',
                        data: JSON.stringify(addstock),
                        type: 'POST',
                        contentType: 'application/json',
                        success: function(response) {
                            if (response) {
                                let pricediff = (Number(response['Price']) - Number(response['Prev Close'])).toFixed(2);
                                let pricepercentdiff = ((Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price'])).toFixed(2);
                                let pricepercentdiff2 = (Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price']);

                                if (pricepercentdiff2 > 0) {
                                    $('#createdchange' + addstock).css('color','green');
                                } else if (pricepercentdiff2 < 0) {
                                    $('#createdchange' + addstock).css('color','red');
                                } else {
                                    $('#createdchange' + addstock).css('color','black');
                                };

                                $('#createdcompname' + addstock).text(response['CompanyName']);
                                $('#createdprice' + addstock).text(response['Price']);
                                $('#createdchange' + addstock).text("$" + pricediff + " (" + pricepercentdiff + "%)");
                                $('#createdshsfloat' + addstock).text(response['Shs Float']);
                                $('#createdshsouts' + addstock).text(response['Shs Outstand']);
                                $('#createdvolume' + addstock).text(response['Volume']);

                                if (response == "Failed to find stock/company symbol!" || response == "A problem has occurred with our 'Data Analysis'! Please send a feed back through our Contact Us page.") {
                                    $('#createdcompname' + addstock).text('N/A');
                                    $('#createdprice' + addstock).text('N/A');
                                    $('#createdchange' + addstock).text('N/A');
                                    $('#createdshsfloat' + addstock).text('N/A');
                                    $('#createdshsouts' + addstock).text('N/A');
                                    $('#createdvolume' + addstock).text('N/A');
                                    alert(response);
                                }
                            }
                        },
                    });

                        /* SEND STOCK TICKER TO BE STORED IN DB */
                    let sendstockdata = {'Stock' : addstock, 'Date' : $fullDate};
                    $.ajax({
                        url: '/storestockinfo',
                        data: JSON.stringify(sendstockdata),
                        contentType: 'application/json',
                        type: 'POST',
                        success: function(response) {
                        },
                    });
                } else {
                    alert("You already have that stock in your portfolio.")
                }
            } catch(e) /* CATCHES THE FIRST STOCK ADDED ERROR */ {
                $('#addstockbox')[0].value = "";
                $('.lefttab').append(($('<tr>')
                    .attr('id',('lefttabrow' + addstock))
                    .attr('class','lefttabrow')
                    .append($('<td>')
                        .attr('id', ('createdstock' + addstock))
                        .attr('class', 'createdstock')
                        .text(addstock)
                        .append($('<button>')
                            .attr('id',('deleteicon' + addstock))
                            .attr('class','deleteicon')
                            .attr('input','button')
                        )
                    )
                    .append($('<td>')
                        .attr('id', ('createdcompname' + addstock))
                        .attr('class', 'createdcompname')
                    )
                    .append($('<td>')
                        .attr('id', ('createdprice' + addstock))
                        .attr('class', 'createdprice')
                    )
                    .append($('<td>')
                        .attr('id', ('createdchange' + addstock))
                        .attr('class', 'createdchange')
                    )
                    .append($('<td>')
                        .attr('id', ('createdshsfloat' + addstock))
                        .attr('class', 'createdshsfloat')
                    )
                    .append($('<td>')
                        .attr('id', ('createdshsouts' + addstock))
                        .attr('class', 'createdshsouts')
                    )
                    .append($('<td>')
                        .attr('id', ('createdvolume' + addstock))
                        .attr('class', 'createdvolume')
                    )
                )
                );

                        /* AUTOFILLED RIGHT TABLE DATA */

                var $currentDate = new Date();
                var $year = $currentDate.getFullYear();
                var $month = $currentDate.getMonth()+1;
                var $day = $currentDate.getDate();
                var $fullDate = $month + "/" + $day + "/" + $year;
                var presentdate = ($year + 1) + '-' + $month + '-' + $day;

                $('.righttab').append($('<tr>')
                    .attr('id',('righttabrow' + addstock))
                    .attr('class','createdrightrow')
                    .append($('<td>')
                        .attr('id', ('createddate' + addstock))
                        .attr('class', 'createddate')
                        .append($('<button>')
                            .attr('id',('dateicon' + addstock))
                            .attr('class','dateicon')
                            .attr('input','button')
                        )
                        .append($('<p>').text($fullDate).attr('class','datetext').attr('id','datetext' + addstock))
                        .append($('<input>')
                            .attr('type','date')
                            .attr('id',('dateinput' + addstock))
                            .attr('class','dateinput')
                            .attr('max',presentdate)
                        )
                    )
                
                /* EMPTY/USER FILLED RIGHT TABLE DATA */
                    .append($('<td>')
                        .attr('id', ('createpurchase' + addstock))
                        .attr('class', 'createpurchase')
                        .append($('<button>')
                                .attr('id',('purchaseicon' + addstock))
                                .attr('class','purchaseicon')
                                .attr('input','button')
                        )
                        .append($('<p>').text('-').attr('class','purchasetext').attr('id','purchasetext' + addstock))
                        .append($('<input>')
                            .attr('type','number')
                            .attr('id',('purchaseinput' + addstock))
                            .attr('class','purchaseinput')
                        )
                    )
                    .append($('<td>')
                        .attr('id', ('createquantity' + addstock))
                        .attr('class', 'createquantity')
                        .append($('<button>')
                            .attr('id',('quantityicon' + addstock))
                            .attr('class','quantityicon')
                            .attr('input','button')
                        )
                        .append($('<p>').text('-').attr('class','quantitytext').attr('id','quantitytext' + addstock))
                        .append($('<input>')
                            .attr('type','number')
                            .attr('id',('quantityinput' + addstock))
                            .attr('class','quantityinput')
                        )
                    )
                    .append($('<td>')
                        .attr('id', ('createdtotal' + addstock))
                        .attr('class', 'createdtotal')
                    )
                    .append($('<td>')
                        .attr('id', ('createdgains' + addstock))
                        .attr('class', 'createdgains')
                    )
                    .append($('<td>')
                        .attr('id', ('createdgains2' + addstock))
                        .attr('class', 'createdgains2')
                    )
                    .append($('<td>')
                        .attr('id', ('createnotes' + addstock))
                        .attr('class', 'createnotes')
                        .append($('<button>')
                            .attr('id',('notesicon' + addstock))
                            .attr('class','notesicon')
                            .attr('input','button')
                        )
                        .append($('<p>').text('-').attr('class','notestext').attr('id','notestext' + addstock))
                        .append($('<input>')
                            .attr('type','text')
                            .attr('id',('notesinput' + addstock))
                            .attr('class','notesinput')
                            .attr('maxlength','20')
                        )
                    )
                );

                    /* WEBSCRAPE FOR DATA */
                $.ajax({
                    url: '/scrapingstockdata',
                    data: JSON.stringify(addstock),
                    type: 'POST',
                    contentType: 'application/json',
                    success: function(response) {
                        if (response) {
                            let pricediff = (Number(response['Price']) - Number(response['Prev Close'])).toFixed(2);
                            let pricepercentdiff = ((Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price'])).toFixed(2);
                            let pricepercentdiff2 = (Number(response['Price']) - Number(response['Prev Close'])) / Number(response['Price']);

                            if (pricepercentdiff2 > 0) {
                                $('#createdchange' + addstock).css('color','green');
                            } else if (pricepercentdiff2 < 0) {
                                $('#createdchange' + addstock).css('color','red');
                            } else {
                                $('#createdchange' + addstock).css('color','black');
                            };

                            $('#createdcompname' + addstock).text(response['CompanyName']);
                            $('#createdprice' + addstock).text(response['Price']);
                            $('#createdchange' + addstock).text("$" + pricediff + " (" + pricepercentdiff + "%)");
                            $('#createdshsfloat' + addstock).text(response['Shs Float']);
                            $('#createdshsouts' + addstock).text(response['Shs Outstand']);
                            $('#createdvolume' + addstock).text(response['Volume']);

                            if (response == "Failed to find stock/company symbol!" || response == "A problem has occurred with our 'Data Analysis'! Please send a feed back through our Contact Us page.") {
                                $('#createdcompname' + addstock).text('N/A');
                                $('#createdprice' + addstock).text('N/A');
                                $('#createdchange' + addstock).text('N/A');
                                $('#createdshsfloat' + addstock).text('N/A');
                                $('#createdshsouts' + addstock).text('N/A');
                                $('#createdvolume' + addstock).text('N/A');
                                alert(response);
                            }
                        }
                    },
                });

                    /* SEND STOCK TICKER TO BE STORED IN DB */
                let sendstockdata = {'Stock' : addstock, 'Date' : $fullDate};
                $.ajax({
                    url: '/storestockinfo',
                    data: JSON.stringify(sendstockdata),
                    contentType: 'application/json',
                    type: 'POST',
                    success: function(response) {
                    },
                });
            }
        } else if (keysenter == 13 && addstock == "" && numofrows < 15) {
            alert("You must insert a valid stock ticker!")
        } else if (keysenter == 13 && numofrows > 14) {
            alert("You are not allowed to add anymore temporary stock info.");
        }
    });


    /* ADD BUTTON ON LONGER HOVER VERSION. USED FOR JQUERY PRACTICE */
    $('#addstockbutton').hover( () => {
        $('#addstockbutton').css('opacity','1');
    }, () => {
        $('#addstockbutton').css('opacity','0.5');
    });


    /* DELETE ICONS (LEFT TAB ONLY) ON HOVERING */
    $('.lefttab').on('mouseenter','td', (event) => {
        if ($(event.currentTarget)[0].firstElementChild) {
            let specificbutton = $(event.currentTarget)[0].firstElementChild.id;
            $('#' + specificbutton).css('opacity', '1');
        }
    });
    $('.lefttab').on('mouseleave','td', (event) => {
        if ($(event.currentTarget)[0].firstElementChild) {
            let specificbutton = $(event.currentTarget)[0].firstElementChild.id;
            $('#' + specificbutton).css('opacity', '0.30');
        }
    });


    /* DELETE ROWS */
    $('.lefttab').on('click','button', (event) => {
        let stockname = event.target.parentElement.textContent;
        let determineleftrow = $(event.target).parent().parent();
        let determinerightrow = $('#righttabrow' + stockname);
        determineleftrow.remove();
        determinerightrow.remove();

        $.ajax({
            url: '/deletestockinfo',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(stockname),
            success: function(response) {
            },
        })
    });


    /* EDIT ICONS (RIGHT TAB ONLY) ON HOVERING EFFECTS */
    $('.righttab').on('mouseenter','td', (event) => {
        let createchk = $(event.currentTarget)[0].className;
        let rightrowindex = $(event.target)[0].parentElement.rowIndex;
        if (rightrowindex != undefined) {
            let stockname = $('.createdstock')[(rightrowindex - 1)].textContent;
            if (createchk === "createddate") {
                let specificbutton = '#dateicon' + stockname;
                $(specificbutton).css('opacity', '1');
            } else if (createchk === "createpurchase") {
                let specificbutton = '#purchaseicon' + stockname;
                $(specificbutton).css('opacity', '1');
            } else if (createchk === "createquantity") {
                let specificbutton = '#quantityicon' + stockname;
                $(specificbutton).css('opacity', '1');
            } else if (createchk === "createnotes") {
                let specificbutton = '#notesicon' + stockname;
                $(specificbutton).css('opacity', '1');
            } else if (createchk === "editicon") {
                $('#editicon' + stockname).css('opacity', '1');
            } else {
                null
            }
        }
    });

    $('.righttab').on('mouseleave','td', (event) => {
        let createchk = $(event.currentTarget)[0].className;
        let rightrowindex = $(event.target)[0].parentElement.rowIndex;
        if (rightrowindex != undefined) {
            let stockname = $('.createdstock')[(rightrowindex - 1)].textContent;
            if (createchk === "createddate") {
                let specificbutton = '#dateicon' + stockname;
                $(specificbutton).css('opacity', '0');
            } else if (createchk === "createpurchase") {
                let specificbutton = '#purchaseicon' + stockname;
                $(specificbutton).css('opacity', '0');
            } else if (createchk === "createquantity") {
                let specificbutton = '#quantityicon' + stockname;
                $(specificbutton).css('opacity', '0');
            } else if (createchk === "createnotes") {
                let specificbutton = '#notesicon' + stockname;
                $(specificbutton).css('opacity', '0');
            } else if (createchk === "editicon") {
                $('#editicon' + stockname).css('opacity', '0');
            } else {
                $('.righttab button').css('opacity', '0');
            }
        }
    });


    /* ON-CLICK TO EDIT */
    $('.righttab').on('click','button', (event) => {
        let targeticon = event.target.className;
        let targeticonid = event.target.id;
        let inputid = event.target.nextSibling.nextSibling.id;
        let inputvalue = event.target.nextSibling.nextSibling.value;
        let inputlength = inputvalue.length;
        let textid = event.target.nextSibling.id;
        let inputvischk = $('#' + inputid).css('display');

        if (targeticon === "dateicon") {
            $('#' + targeticonid).css('display','none');
            let dateinputsplit = inputvalue.split('-');
            let dateinputreformat = dateinputsplit[1] + '/' + dateinputsplit[2] + '/' + dateinputsplit[0]

            if (inputvischk == "none") {
                $('#' + textid).css('display','none');
                $('#' + inputid).css('display','initial');
            } /*else {      REMOVED THIS FEATURE
                $('#' + inputid).css('display','none');
                if (dateinputreformat == "undefined/undefined/") {
                    $('#' + textid).css('left','35px');
                    $('#' + textid).css('display','initial');
                } else {
                    $('#' + textid).text(dateinputreformat);
                    $('#' + textid).css('display','initial');
                }
            } */
        } else if (targeticon === "purchaseicon") {
            $('#' + targeticonid).css('display','none');
            
            if (inputvischk == "none") {
                $('#' + textid).css('display','none');
                $('#' + inputid).css('display','initial');
            } /*else {      REMOVED FEATURE
                if (inputlength > 8) {
                    alert("There is a max of 8 digits for the Purchase Cost.");
                    $('#' + textid).css('display','initial');
                    $('#' + inputid).css('display','none');
                    $('#' + inputid)[0].value = "";
                } else if (inputlength > 0 && inputlength <= 8) {
                    $('#' + textid).text(inputvalue);
                    $('#' + textid).css('display','initial');
                    $('#' + inputid).css('display','none');
                } else if (inputvalue == "" || inputlength == 0) {
                    $('#' + textid).css('left','35px');
                    $('#' + textid).css('display','initial');
                    $('#' + inputid).css('display','none');
                }
            }; */
        } else if (targeticon === "quantityicon") {
            $('#' + targeticonid).css('display','none');

            if (inputvischk == "none") {
                $('#' + textid).css('display','none');
                $('#' + inputid).css('display','initial');
            } /*else {      REMOVED FEATURE
                if (inputlength > 8) {
                    alert("There is a maximum of 8 digits for the Quantity Amt.");
                    $('#' + inputid).css('display','none');
                    $('#' + inputid)[0].value = "";
                } else if (inputlength > 0 && inputlength <= 8) {
                    $('#' + textid).text(inputvalue);
                    $('#' + textid).css('display','initial');
                    $('#' + inputid).css('display','none');
                } else if (inputvalue == "" || inputlength == 0) {
                    $('#' + textid).css('left','35px');
                    $('#' + textid).css('display','initial');
                    $('#' + inputid).css('display','none');
                }
            }; */
        } else if (targeticon === "notesicon") {
            $('#' + targeticonid).css('display','none');

            if (inputvischk == "none") {
                $('#' + textid).css('display','none');
                $('#' + inputid).css('display','initial');
            } /*else {
                $('#' + inputid).css('display','none');

                if (inputvalue == "") {
                    $('#' + textid).text('-');
                    $('#' + textid).css('left','15px');
                    $('#' + textid).css('display','initial');
                } else {
                    $('#' + textid).text(inputnotes);
                    $('#' + textid).css('display','initial');
                }
            }; */
        }
    })
    

    /* AUTO-EDITS TABLE DATA & SENDS TO DATABASE IF USERS FOCUS OUT ON INPUT BOXES */
    $('.righttab').on('focusout keypress','input', (event) => {
        let keypressed = event.which;
        let eventtype = event.type;
        
        if (keypressed == 13 || keypressed == 27 || eventtype == 'keypress') {    /* ADDED TO AVOID DOUBLE QUERY VIA ENTER-KEY */
            $(this).unbind('focusout');
        } else if (eventtype == 'focusout' && keypressed != 13 && keypressed != 27 && eventtype != 'keypress') {
            let eventclassname = event.target.className;
            let inputidname = event.target.id;
            let textidname = event.target.previousSibling.id;
            let textvalue = $('#' + textidname).text();
            let editiconid = event.target.parentElement.children[0].id;
            let numinput = $(event.target)[0].value;
            let inputlength = numinput.length;
            let rightrowindex = event.target.parentElement.parentElement.rowIndex;
            let stockname = $('.lefttab tbody')[0].children[rightrowindex].children[0].textContent;
            var currentprice = Number($('#createdprice' + stockname)[0].textContent);

            if (eventclassname === "dateinput") {
                var didShowAlert = false;
                if (didShowAlert) {
                    didShowAlert = false;
                } else {
                    didShowAlert = true;
                    let initialdate = $('#' + textidname)[0].textContent;
                    let dateinputsplit = numinput.split('-');
                    let dateinputreformat = dateinputsplit[1] + '/' + dateinputsplit[2] + '/' + dateinputsplit[0]
                    if (dateinputreformat == "undefined/undefined/" || dateinputreformat == initialdate) {
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                    } else {
                        $('#' + textidname).text(dateinputreformat);
                        $('#' + textidname).css('left','35px');
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');

                        let verifiedvalue = dateinputreformat
                        let updatestockinfo = {'Stock' : stockname,'EditType' : 'Date' ,'Value' : verifiedvalue};
                        $.ajax({
                            url: '/updatestockinfo',
                            data: JSON.stringify(updatestockinfo),
                            contentType: 'application/json',
                            type: 'POST',
                            success: function(response) {
                            },
                        });
                    }
                }
            } else if (eventclassname === "purchaseinput") {
                var currentquantity = Number($('#quantitytext' + stockname)[0].textContent);
                var totalpurchase = Number((Number(numinput) * currentquantity).toFixed(2));
                var totalgains = Number(((currentprice * currentquantity) - totalpurchase).toFixed(2));
                var gainsperc = Number(((currentprice - numinput) / currentprice * 100).toFixed(2));

                var didShowAlert = false;
                if (didShowAlert) {
                    didShowAlert = false;
                } else {
                    didShowAlert = true;
                    if (inputlength > 8) {
                        alert("There is a maximum of 8 digits for the Purchase Cost.");
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                        $(event.target)[0].value = "";
                        event.preventDefault();
                    } else if (inputlength > 0 && inputlength <= 8 && numinput != textvalue) {

                                /* APPLIES CHANGES IMMEDIATELY TO USER'S VIEW */
                        $('#' + textidname).text(numinput);
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');

                        $('#createdtotal' + stockname).text(totalpurchase);
                        $('#createdgains' + stockname).text('$ ' + totalgains);
                        $('#createdgains2' + stockname).text(gainsperc + ' %');
                        if (totalgains > 0) {
                            $('#createdgains' + stockname).css('color','green');
                        } else if (totalgains < 0) {
                            $('#createdgains' + stockname).css('color','red');
                        } else {
                            $('#createdgains' + stockname).css('color','black');
                        };
                        if (gainsperc > 0) {
                            $('#createdgains2' + stockname).css('color','green');
                        } else if (gainsperc < 0) {
                            $('#createdgains2' + stockname).css('color','red');
                        } else {
                            $('#createdgains2' + stockname).css('color','black');
                        };

                                    /* SENDS EDITED STOCK INFO TO BE SAVED IN DATABASE */
                        let verifiedvalue = numinput;
                        let updatestockinfo = {'Stock' : stockname,'EditType' : 'PurchaseCost' ,'Value' : verifiedvalue};
                        $.ajax({
                            url: '/updatestockinfo',
                            data: JSON.stringify(updatestockinfo),
                            contentType: 'application/json',
                            type: 'POST',
                            success: function(response) {
                                
                            },
                        });
                    } else if (numinput == "" || inputlength == 0 || numinput == textvalue) {
                        $('#' + textidname).css('left','35px');
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                    }
                }
            } else if (eventclassname === "quantityinput") {
                var currentpurchase = Number($('#purchasetext' + stockname)[0].textContent);
                var totalpurchase = Number((Number(currentpurchase) * numinput).toFixed(2));
                var totalgains = Number(((currentprice * numinput) - totalpurchase).toFixed(2));
                var gainsperc = Number(((currentprice - currentpurchase) / currentprice * 100).toFixed(2));

                var didShowAlert = false;
                if (didShowAlert) {
                    didShowAlert = false;
                } else {
                    didShowAlert = true;
                    if (inputlength > 8) {
                        alert("There is a maximum of 8 digits for the Quantity Amt.");
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                        $(event.target)[0].value = "";
                        event.preventDefault();
                    } else if (inputlength > 0 && inputlength <= 8 && numinput != textvalue) {

                                /* APPLIES CHANGES IMMEDIATELY TO USER'S VIEW */

                        $('#' + textidname).text(numinput);
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');

                        $('#createdtotal' + stockname).text(totalpurchase);
                        $('#createdgains' + stockname).text('$ ' + totalgains);
                        $('#createdgains2' + stockname).text(gainsperc + ' %');
                        if (totalgains > 0) {
                            $('#createdgains' + stockname).css('color','green');
                        } else if (totalgains < 0) {
                            $('#createdgains' + stockname).css('color','red');
                        } else {
                            $('#createdgains' + stockname).css('color','black');
                        };
                        if (gainsperc > 0) {
                            $('#createdgains2' + stockname).css('color','green');
                        } else if (gainsperc < 0) {
                            $('#createdgains2' + stockname).css('color','red');
                        } else {
                            $('#createdgains2' + stockname).css('color','black');
                        };

                        
                            /* SENDS EDITED STOCK INFO TO BE SAVED IN DATABASE */

                        let verifiedvalue = numinput;
                        let updatestockinfo = {'Stock' : stockname,'EditType' : 'Quantity' ,'Value' : verifiedvalue};
                        $.ajax({
                            url: '/updatestockinfo',
                            data: JSON.stringify(updatestockinfo),
                            contentType: 'application/json',
                            type: 'POST',
                            success: function(response) {
                            },
                        });
                    } else if (numinput == "" || inputlength == 0 || numinput == textvalue) {
                        $('#' + textidname).css('left','35px');
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                    }
                }
            } else if (eventclassname === "notesinput") {
                var didShowAlert = false;
                if (didShowAlert) {
                    didShowAlert = false;
                } else {
                    didShowAlert = true;
                    if (inputlength > 20) {
                        alert("There is a maximum of 20 Characters for Notes.");
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                        $(event.target)[0].value = ""
                        event.preventDefault();
                    } else if (inputlength > 0 && inputlength <= 20 && numinput != textvalue) {
                        $('#' + textidname).text(numinput);
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');

                        let verifiedvalue = numinput
                        let updatestockinfo = {'Stock' : stockname,'EditType' : 'Notes' ,'Value' : verifiedvalue};
                        $.ajax({
                            url: '/updatestockinfo',
                            data: JSON.stringify(updatestockinfo),
                            contentType: 'application/json',
                            type: 'POST',
                            success: function(response) {
                            },
                        });
                    } else if (numinput == "" || inputlength == 0 || numinput == textvalue) {
                        $('#' + textidname).css('left','15px');
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                    }
                }
            }
        };
    });

    $('.righttab').on('keydown','input', (event) => {
        let keypressed = event.which;

        if (keypressed == 13) {
            let eventclassname = event.target.className;
            let inputidname = event.target.id;
            let textidname = event.target.previousSibling.id;
            let textvalue = $('#' + textidname).text();
            let editiconid = event.target.parentElement.children[0].id;
            let numinput = $(event.target)[0].value;
            let inputlength = numinput.length;
            let rightrowindex = event.target.parentElement.parentElement.rowIndex;
            let stockname = $('.lefttab tbody')[0].children[rightrowindex].children[0].textContent;
            var currentprice = Number($('#createdprice' + stockname)[0].textContent);

            if (eventclassname === "dateinput") {
                var didShowAlert = false;
                if (didShowAlert) {
                    didShowAlert = false;
                } else {
                    didShowAlert = true;
                    let initialdate = $('#' + textidname)[0].textContent;
                    let dateinputsplit = numinput.split('-');
                    let dateinputreformat = dateinputsplit[1] + '/' + dateinputsplit[2] + '/' + dateinputsplit[0]
                    if (dateinputreformat == "undefined/undefined/" || dateinputreformat == initialdate) {
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                    } else {
                        $('#' + textidname).text(dateinputreformat);
                        $('#' + textidname).css('left','35px');
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');

                        let verifiedvalue = dateinputreformat;
                        let updatestockinfo = {'Stock' : stockname,'EditType' : 'Date' ,'Value' : verifiedvalue};
                        $.ajax({
                            url: '/updatestockinfo',
                            data: JSON.stringify(updatestockinfo),
                            contentType: 'application/json',
                            type: 'POST',
                            success: function(response) {
                            },
                        });
                    }
                }
            } else if (eventclassname === "purchaseinput") {
                var currentquantity = Number($('#quantitytext' + stockname)[0].textContent);
                var totalpurchase = Number((Number(numinput) * currentquantity).toFixed(2));
                var totalgains = Number(((currentprice * currentquantity) - totalpurchase).toFixed(2));
                var gainsperc = Number(((currentprice - numinput) / currentprice * 100).toFixed(2));

                var didShowAlert = false;
                if (didShowAlert) {
                    didShowAlert = false;
                } else {
                    didShowAlert = true;
                    if (inputlength > 8) {
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                        $('#' + inputidname)[0].value = "";
                        alert("There is a max of 8 digits for the Purchase Cost.");
                        event.preventDefault();
                    } else if (inputlength > 0 && inputlength <= 8 && numinput != textvalue) {

                                /* APPLIES CHANGES IMMEDIATELY TO USER'S VIEW */

                        $('#' + textidname).text(numinput);
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');

                        $('#createdtotal' + stockname).text(totalpurchase);
                        $('#createdgains' + stockname).text('$ ' + totalgains);
                        $('#createdgains2' + stockname).text(gainsperc + ' %');
                        if (totalgains > 0) {
                            $('#createdgains' + stockname).css('color','green');
                        } else if (totalgains < 0) {
                            $('#createdgains' + stockname).css('color','red');
                        } else {
                            $('#createdgains' + stockname).css('color','black');
                        };
                        if (gainsperc > 0) {
                            $('#createdgains2' + stockname).css('color','green');
                        } else if (gainsperc < 0) {
                            $('#createdgains2' + stockname).css('color','red');
                        } else {
                            $('#createdgains2' + stockname).css('color','black');
                        };

                                    /* SENDS EDITED STOCK INFO TO BE SAVED IN DATABASE */

                        let verifiedvalue = numinput;
                        let updatestockinfo = {'Stock' : stockname,'EditType' : 'PurchaseCost' ,'Value' : verifiedvalue};
                        $.ajax({
                            url: '/updatestockinfo',
                            data: JSON.stringify(updatestockinfo),
                            contentType: 'application/json',
                            type: 'POST',
                            success: function(response) {
                            },
                        });
                    } else if (numinput == "" || inputlength == 0 || numinput == textvalue) {
                        $('#' + textidname).css('left','35px');
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                    }
                }
            } else if (eventclassname === "quantityinput") {
                var currentpurchase = Number($('#purchasetext' + stockname)[0].textContent);
                var totalpurchase = Number((Number(currentpurchase) * numinput).toFixed(2));
                var totalgains = Number(((currentprice * numinput) - totalpurchase).toFixed(2));
                var gainsperc = Number(((currentprice - currentpurchase) / currentprice * 100).toFixed(2));

                var didShowAlert = false;
                if (didShowAlert) {
                    didShowAlert = false;
                } else {
                    didShowAlert = true;
                    if (inputlength > 8) {
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                        $('#' + inputidname)[0].value = "";
                        alert("There is a max of 8 digits for the Quantity Amt.");
                        event.preventDefault();
                    } else if (inputlength > 0 && inputlength <= 8 && numinput != textvalue) {
                        
                                /* APPLIES CHANGES IMMEDIATELY TO USER'S VIEW */

                        $('#' + textidname).text(numinput);
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');

                        $('#createdtotal' + stockname).text(totalpurchase);
                        $('#createdgains' + stockname).text('$ ' + totalgains);
                        $('#createdgains2' + stockname).text(gainsperc + ' %');
                        if (totalgains > 0) {
                            $('#createdgains' + stockname).css('color','green');
                        } else if (totalgains < 0) {
                            $('#createdgains' + stockname).css('color','red');
                        } else {
                            $('#createdgains' + stockname).css('color','black');
                        };
                        if (gainsperc > 0) {
                            $('#createdgains2' + stockname).css('color','green');
                        } else if (gainsperc < 0) {
                            $('#createdgains2' + stockname).css('color','red');
                        } else {
                            $('#createdgains2' + stockname).css('color','black');
                        };

                        
                            /* SENDS EDITED STOCK INFO TO BE SAVED IN DATABASE */

                        let verifiedvalue = numinput;
                        let updatestockinfo = {'Stock' : stockname,'EditType' : 'Quantity' ,'Value' : verifiedvalue};
                        $.ajax({
                            url: '/updatestockinfo',
                            data: JSON.stringify(updatestockinfo),
                            contentType: 'application/json',
                            type: 'POST',
                            success: function(response) {
                            },
                        });
                    } else if (numinput == "" || inputlength == 0 || numinput == textvalue) {
                        $('#' + textidname).css('left','35px');
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                    }
                }
            } else if (eventclassname === "notesinput") {
                var didShowAlert = false;
                if (didShowAlert) {
                    didShowAlert = false;
                } else {
                    didShowAlert = true;
                    if (inputlength > 20) {
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                        $('#' + inputidname)[0].value = "";
                        alert("There are a max of 20 characters for notes.");
                        event.preventDefault();
                    } else if (inputlength > 0 && inputlength <= 20 && numinput != textvalue) {
                        $('#' + textidname).text(numinput);
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');

                        let verifiedvalue = numinput;
                        let updatestockinfo = {'Stock' : stockname,'EditType' : 'Notes' ,'Value' : verifiedvalue};
                        $.ajax({
                            url: '/updatestockinfo',
                            data: JSON.stringify(updatestockinfo),
                            contentType: 'application/json',
                            type: 'POST',
                            success: function(response) {
                            },
                        });
                    } else if (numinput == "" || inputlength == 0 || numinput == textvalue) {
                        $('#' + textidname).css('left','15px');
                        $('#' + textidname).css('display','initial');
                        $('#' + inputidname).css('display','none');
                        $('#' + editiconid).css('display','initial');
                    }
                }
            }
        } else if (keypressed == 27) {
            let inputclass = event.target.className;
            let inputidname = event.target.id;
            let textidname = event.target.previousSibling.id;
            let editiconid = event.target.parentElement.children[0].id;
            if (inputclass == "dateinput") {
                $('#' + textidname).css('display','initial');
                $('#' + inputidname).css('display','none');
                $('#' + editiconid).css('display','initial');
            } else {
                let textvalue = $('#' + textidname).text();
                $('#' + textidname).css('display','initial');
                $('#' + inputidname).css('display','none');
                $('#' + editiconid).css('display','initial');
                $('#' + inputidname)[0].value = textvalue;
            }
        }
    });


    /* EXPAND ARROW ICON TO REVEAL RIGHT-TABLE */
    $('#expandarrow').on('click', () => {
        let expandarrow = $('#expandarrow');
        let righttable = $('.rightusertable');

        if (expandarrow.css('margin-left') == '-35px') {    /* TO EXPAND AND SHOW HIDDEN RIGHT TABLE */
            righttable.css('margin-left','-10px');
            expandarrow.css('margin-left', '-45px');
            expandarrow.css('transform', 'rotate(180deg)');
            expandarrow.css('pointer-events','none');       /* ADDED POINTER EVENTS TO AVOID USERS SPAMMING ARROW TO GLITCH FUNCTIONALITY */

            setTimeout(() => {
                righttable.css('transform', 'scale(1)').css('z-index', '200');
                expandarrow.css('pointer-events','auto');
            }, 1000);
        } else if (expandarrow.css('margin-left') == '-45px') {        /* HIDES RIGHT TABLE */
            righttable.css('z-index', '1').css('transform', 'scale(0.75)');
            expandarrow.css('margin-left', '-35px');
            expandarrow.css('transform', 'rotate(360deg)');
            expandarrow.css('pointer-events','none');

            setTimeout(() => {
                righttable.css('margin-left', '-970px');
                expandarrow.css('pointer-events','auto');
            }, 1000);
        };
    });

});