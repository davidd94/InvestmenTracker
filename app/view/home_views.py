from flask import session, current_app, render_template, request, jsonify
from bs4 import BeautifulSoup
from app.model.email import send_email
from app.model.feedback import FeedbackModel
from app.model.recaptcha import google_recaptchaV2
from app.view import bp
import json, requests, os, urllib


@bp.route("/")
def homepage():
    if ('username' in session) and ('firstname' in session):
        return render_template('InvestmenTracker-homepage.html', title=session['username'], name=session['firstname'])
    else:
        return render_template('InvestmenTracker-homepage.html')

@bp.route("/userportfolio")
def userportfolio():
    if 'username' in session:
        return render_template('InvestmenTracker-userportfolio.html', title=session['username'])
    else:
        return redirect('/')

@bp.route("/financialnews")
def financials():
    if 'username' in session:
        return render_template('InvestmenTracker-news.html', title=session['username'], username=session['firstname'])
    else:
        return render_template('InvestmenTracker-news.html')

@bp.route("/educationaltools")
def edutools():
    if 'username' in session:
        return render_template('InvestmenTracker-educationaltools.html', title=session['username'], username=session['firstname'])
    else:
        return render_template('InvestmenTracker-educationaltools.html')

@bp.route("/aboutme")
def aboutme():
    if 'username' in session:
        return render_template('InvestmenTracker-aboutme.html', title=session['username'])
    else:
        return render_template('InvestmenTracker-aboutme.html')

@bp.route("/contactme")
def contact():
    if 'username' in session:
        return render_template('InvestmenTracker-contact.html', title=session['username'], username=session['firstname'], useremail=session['email'])
    else:
        return render_template('InvestmenTracker-contact.html')

@bp.route("/sendfeedback", methods=['POST'])
def feedback():
    feedbackname = request.json['FirstName']
    feedbackemail = request.json['Email']
    feedbackcomment = request.json['Feedback']
    recaptchadata = request.json['Recaptcha']
    google_response = google_recaptchaV2(recaptchadata)

    if (google_response['success'] == True):
        subject = f'InvestmenTracker Feedback from {feedbackname}'
        sender = current_app.config['MAIL_USERNAME']
        recipient = current_app.config['MAIL_USERNAME']
        
        # SAVE TO DB
        feedback_data = FeedbackModel(email=feedbackemail,
                                        firstname=feedbackname,
                                        feedback=feedbackcomment)
        
        validation_errors = feedback_data.validate_self()
        if validation_errors:
            return str(validation_errors)
        else:
            feedback_data.connect()
            feedback_data.save()
            send_email(subject, sender, recipient, 'feedback',
                        firstname=feedbackname,
                        email=feedbackemail,
                        feedback=feedbackcomment)
            
            return "Feedback Success"
    
    return "Feedback Failure"


@bp.route('/scrapingstockdata', methods=['POST'])
def stockscrape():
    try:
        tickersearch = request.json
        finvizstocks = "https://finviz.com/quote.ashx?t=" + tickersearch
        page = urllib.request.urlopen(finvizstocks)
        soup = BeautifulSoup(page, "html.parser")


        scrapeddata = {}
        
        scrapedstockinfo = soup.find_all("td",class_="snapshot-td2-cp")
        refinedstockinfo = []
        scrapedstockvalue = soup.find_all("td",class_="snapshot-td2")
        refinedstockvalue = []
        scrapedstockname = soup.find_all("a",class_="tab-link")
        refinedstocknamelist = []
        stockname = ""
        
        for a in scrapedstockname:         #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
            for b in a:
                for text in b:
                    if (len(text) > 1):
                        refinedstocknamelist.append(text)
        
        if (len(refinedstocknamelist) == 3):        #SAFEGUARDING AGAINST CHANGES IN STOCK COMPANMY NAME
            stockname = refinedstocknamelist[2]
            

        if (len(scrapedstockinfo) != 72 or len(scrapedstockvalue) != 72 ):   #SAFEGUARDING AGAINST ANY CHANGES MADE BY THE DATA-SCRAPED WEB DEV THAT WILL BREAK/INACCURATELY DISPLAY THE DATA ON MY WEBSITE 
            return jsonify("A problem has occurred with our 'Data Analysis'! Please send a feed back through our Contact Us page.")

        for eachtd in scrapedstockinfo:
            for text in eachtd:             #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
                refinedstockinfo.append(text)

        for eachtd in scrapedstockvalue:
            for eachb in eachtd:            #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
                spanlist = eachb.find_all('span')       #A FEW 'SPAN' HTML ELEMENTS THAT NEEDED TO BE EXTRACTED SEPARATELY
                smalllist = eachb.find_all('small')     #A SINGLE 'SMALL' HTML ELEMENT THAT NEEDED TO BE EXTRACTED SEPARATELY
                if (smalllist):
                    for small in smalllist:
                            for innersmalltext in small:    #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
                                refinedstockvalue.append(innersmalltext)
                for text in eachb:
                    if (text == '-' and len(text) == 1):    #FOR ANY NON-VALUES, MUST REPLACE WITH '-'
                        refinedstockvalue.append('-')
                    elif (len(text) == 1):            #CHECKING TO SEE IF FEW VALUES ARE STILL IN THEIR HTML FORMAT WHICH REQUIRES ADDITIONAL EXTRACTION METHODS
                        for span in spanlist:
                            for innerspantext in span:      #EXTRACTING INNER (CHILD) VALUES OF PARENT METHOD
                                refinedstockvalue.append(innerspantext)
                    else:
                        refinedstockvalue.append(text)
        
        
        #COMBINING THE TWO NEWLY EXTRACTED LIST INTO ONE DICTIONARY TO BE USED
        for i in range(len(refinedstockvalue)):
            scrapeddata[refinedstockinfo[i]] = refinedstockvalue[i]
        
        scrapeddata['CompanyName'] = stockname

        return jsonify(scrapeddata)
    
    except Exception:
        return jsonify("Failed to find stock/company symbol!")
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")


@bp.route('/scrapinggurunews', methods=['GET'])
def gurunews():
    gurunews = "https://www.gurufocus.com/news.php?cat=guru&n=100"
    page = urllib.request.urlopen(gurunews)
    soup = BeautifulSoup(page, "html.parser")

    articletitle = soup.find_all("a",class_="articletitle")
    articledate = soup.find_all("div",class_="date")
    compilednewsdata = {}
    
    count = 0
    for eacha in articletitle:
        newstitle = eacha.get_text()
        newslink = 'https://www.gurufocus.com' + eacha.get('href')

        compilednewsdata[str(count)] = {'Title' : newstitle, 'Link' : newslink}
        count += 1
    
    count2 = 0
    for div in articledate:
        rawnewsdate = div.get_text()
        newsdate = rawnewsdate.split('-',2)
        refinednewsdate = newsdate[0]
        
        rawstocktick = newsdate[len(newsdate) - 1]
        rawstockticksplit = rawstocktick.split('-')
        rawstocktick2 = rawstockticksplit[0]
        rawstocksplit2 = rawstocktick2.split('\n')
        refinedstocktick = ' '.join(rawstocksplit2)

        stockcheck = refinedstocktick.split(' ')
        if (stockcheck[1] == "Stocks:"):
            compilednewsdata[str(count2)]['Stocks'] = refinedstocktick
        else:
            compilednewsdata[str(count2)]['Stocks'] = ""

        compilednewsdata[str(count2)]['Date'] = refinednewsdate
        count2 += 1
    
    if (count == count2):    #SAFEGUARD IF WEBSITE WAS MODIFIED THUS DATA WILL NOT BE ALIGNED
        return jsonify(compilednewsdata)
    else:
        return jsonify("There was an error retrieving GuruFocus news.")