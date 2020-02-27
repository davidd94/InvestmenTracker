from flask import session, current_app, redirect, jsonify, request, render_template
from app import mongo
from app.view import bp
from app.model.users import User
from app.model.stocks import Stocks


@bp.route('/storestockinfo',methods=['POST'])
def storestocks():
    stockname = request.json['Stock']
    stockdate = request.json['Date']
    username = session['username']
    new_stock_data = {
        'StockTicker': stockname,
        'StockData': {
            'date': stockdate,
            'cost': 0,
            'qty': 0,
            'notes': ''
        }
    }

    user_data = Stocks.get_userstocks_by_username(username)
    stock_data = user_data.stocks

    for stock in stock_data:    #LOOPS EACH USER'S STOCK IN LIBRARY TO FIND ANY DUPLICATES
        if (stock['StockTicker'] == stockname):
            return jsonify("You already have that stock in your portfolio!")
    
    if (len(stock_data) < 10):
        user_data.update(push__stocks=new_stock_data)
        return jsonify("You have successfully added a stock!")
    elif (stockliblength >= 10):
        return jsonify("You have reached your maximum of 10 stocks in your portfolio! The stock info will only be displayed temporarily. The limit will increase in future updates.")
    else:
        return jsonify("ERROR: FAILED TO ADD STOCK!")


@bp.route('/deletestockinfo', methods=['POST'])
def deletestocks():
    stockname = request.json
    username = session['username']

    user_data = Stocks.get_userstocks_by_username(username)
    stockliblength = len(user_data['stocks'])
    foundexistingstock = False
    
    for count in range(stockliblength):    #LOOPS EACH USER'S STOCK IN LIBRARY TO LOCATE THE SPECIFIC GIVEN STOCK NAME
        findexistingstock = user_data['stocks'][count]['StockTicker']
        if (findexistingstock == stockname):
            foundexistingstock = True
            stockid = count
    
    if (foundexistingstock == True):
        userstockdb.update_one({'username' : username}, {'$pull' : {'stocks' : {'StockTicker' : stockname}}})
        return jsonify("You have successfully deleted a stock!")
    elif (user_data == None):
        return jsonify("No user info has been found!")
    
    return jsonify("Deleted temporary stock info!")


@bp.route('/retrievestockinfo', methods=['GET'])
def getstocks():
    if 'username' in session:
        username = session['username']
        userstockdb = mongo.db.Stocks
        finduser = userstockdb.find_one({'username' : username})
        stocklib = finduser['stocks']
        return jsonify(stocklib)


@bp.route('/updatestockinfo', methods=['POST'])
def updatestocks():
    username = session['username']
    stockname = request.json['Stock']
    edittype = request.json['EditType']
    updatevalue = request.json['Value']
    
    userstockdb = mongo.db.Stocks
    finduser = userstockdb.find_one({'username' : username})
    stockliblength = len(finduser['stocks'])

    for count in range(stockliblength):    #LOOPS EACH USER'S STOCK IN LIBRARY TO FIND THE DESIRED STOCK
        findexistingstock = finduser['stocks'][count]['StockTicker']
        if (findexistingstock == stockname):
            stocknum = count
            
        if (finduser):
            if (edittype == "Date"):
                userstockdb.update_one({'username' : username}, {'$set' : {('stocks.' + str(stocknum) + '.StockData.date') :  updatevalue}})
                return "Date updated!!"
            elif (edittype == "PurchaseCost"):
                userstockdb.update_one({'username' : username}, {'$set' : {('stocks.' + str(stocknum) + '.StockData.cost') :  float(updatevalue)}})
                return "Purchase Cost updated!!"
            elif (edittype == "Quantity"):
                userstockdb.update_one({'username' : username}, {'$set' : {('stocks.' + str(stocknum) + '.StockData.qty') :  float(updatevalue)}})
                return "Quantity updated!!"
            elif (edittype == "Notes"):
                userstockdb.update_one({'username' : username}, {'$set' : {('stocks.' + str(stocknum) + '.StockData.notes') :  updatevalue}})
                return "Notes updated!!"
    else:
        return jsonify("NO STOCK INFO WAS UPDATED!")
    
    return jsonify("ERROR UPDATING STOCK INFO!")
