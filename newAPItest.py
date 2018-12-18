# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 13:44:41 2018

@author: Jennifer Yang
"""

# -*- coding: utf-8 -*-

from flask import Flask, request,jsonify
import MySQLdb
import datetime
from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

def connectDB(searchTarget,param):
    
    db = MySQLdb.connect(host="127.0.0.1",
        user="root", passwd="",
        db="webservice", charset="utf8")
    cursor = db.cursor()
    
    if searchTarget == 'weather':
        user_city = param
        user_dateTime_callTime = datetime.datetime.now()
        searchSQL = "SELECT * FROM weather WHERE city = '%s' and startTime <= '%s' and '%s' < endTime"% (user_city,user_dateTime_callTime,user_dateTime_callTime)
        cursor.execute(searchSQL)
        
        results_weather = cursor.fetchall() #type:tuple
        
        tuple_dbResult = results_weather[0]
#        db_city = tuple_dbResult[0]
        db_startTime = tuple_dbResult[1]
        db_endTime = tuple_dbResult[2]
        temp_description = tuple_dbResult[3]
        
        #回傳的參數
        text = temp_description.split('。')[0]
        temp_rain = temp_description.split('。')[1]
        rain = temp_rain.split(' ')[1]
        temp_temp = temp_description.split('。')[2]
        temp = temp_temp.split('攝氏')[1]
        temp = temp.split('度')[0]
        
        temp_startTime = str(db_startTime)
        temp_endTime = str(db_endTime)
        timeInterval = temp_startTime +' ~ '+ temp_endTime

        dict_weather = {'text':text,
                        'rain':rain,
                        'tem
                        p':temp,
                        'timeInterval':timeInterval}
        result = dict_weather
    
    if searchTarget == 'clothes':
        urls = []
        user_gender = param[0]
        user_temp = param[1]
        
        searchSQL = "SELECT url FROM clothes WHERE gender = '%s' and low_temp <= '%s' and '%s' <= high_temp"% (user_gender,user_temp,user_temp)
        cursor.execute(searchSQL)
        
        results_clothes = cursor.fetchall() #type:tuple
        
        dict_photosURL = {'photo1': results_clothes[0][0],
                          'photo2': results_clothes[1][0],
                          'photo3': results_clothes[2][0]
                }        
        result = dict_photosURL

    db.commit()
    db.close()
    return result

@app.route('/weatherAndOutfits', methods = ['get'])
def index():
    dict_weather = {}
    dict_photosURL = {}
    results = {}
    
#    user_gender = request.values.get('gender')
#    user_city = request.values.get('city')
    
#    user_gender = request.form.get('gender')
#    user_city = request.form.get('city')
    
    user_gender = request.args.get('gender')
    user_city = request.args.get('city')
    
    data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]
#
    json = json.dumps(data)
    return "{\"a\":\"1\"}" 
    
#    searchWeather = 'weather'
#    resultFromWeather = connectDB(searchWeather,user_city)
#    
#    user_temp = resultFromWeather['temp']
#    params = [user_gender,user_temp]
#    searchClothes = 'clothes'
#    resultFromClothes = connectDB(searchClothes,params)
#    
#    results = {'text':resultFromWeather['text'],
#               'rain':resultFromWeather['rain'],
#               'temp':resultFromWeather['temp'],
#               'timeInterval':resultFromWeather['timeInterval'],
#               'url_1':resultFromClothes['photo1'],
#               'url_2':resultFromClothes['photo2'],
#               'url_3':resultFromClothes['photo3']
#            }
##    return 'hello'
##    return str(results)
##    return jsonify(results)
# 
#    response = jsonify(results)
#    response.headers['Access-Control-Allow-Credentials'] = 'true'
#    response.headers['Access-Control-Allow-Origin'] = request.environ['HTTP_ORIGIN']
#    response.headers['Access-Control-Allow-Methods'] = 'POST'
#    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#    return response

if __name__ == '__main__':
#    app.run(debug = True)
    app.run(host = '0.0.0.0')


