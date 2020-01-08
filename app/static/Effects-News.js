$(document).ready(() => {
    $('.finviznewslink').on('click', () => {
        $('.finvizbox').css('display','initial');
        $('.yahoonews').css('display','none');
        $('.gurunews').css('display','none');
    });

    $('.yahoonewslink').on('click', () => {
        $('.finvizbox').css('display','none');
        $('.yahoonews').css('display','initial');
        $('.gurunews').css('display','none');
    });

    $('.gurunewslink').on('click', () => {
        $('.finvizbox').css('display','none');
        $('.yahoonews').css('display','none');
        $('.gurunews').css('display','initial');

        
        $.ajax({
            url: '/scrapinggurunews',
            contentType: 'application/json',
            type: 'GET',
            success: function(response) {
                if (response == "There was an error retrieving GuruFocus news.") {
                    alert(response);
                } else {
                    newslength = Object.keys(response).length;
                    
                    for (i = 0 ; i < newslength ; i++) {    /* LOOPS EACH OBJECT (NEWS) ITEM */
                        let unrefinedstocks = response[i]['Stocks'];
                        let refinedstocks = unrefinedstocks.replace(/Stocks:/g, "");
                        let newsdate = response[i]['Date'];
                        let newstitle = response[i]['Title'];
                        let newslink = response[i]['Link'];

                        /* ADDS NEW DYNAMIC TABLE ROWS WITH NEWS INFO */
                        $('.gurutbody').append($('<tr>')
                        .attr('id',('gurutr' + i))
                        .attr('class','gurutr')
                        .append($('<td>')
                            .attr('id','gurustock' + i)
                            .attr('class','gurustock')
                            .text(refinedstocks))
                        .append($('<td>')
                            .attr('id','gurudate' + i)
                            .attr('class','gurudate')
                            .text(newsdate))
                        .append($('<td>')
                            .attr('id','gurutitle' + i)
                            .attr('class','gurutitle')
                            .append($('<a>')
                                .attr('id','gurulink' + i)
                                .attr('class','gurulink')
                                .attr('href',newslink)
                                .attr('target','_blank')
                                .text(newstitle)
                                )
                            )
                        )
                    }
                }
            },
        })
    });
});