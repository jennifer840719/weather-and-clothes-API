import zipfile36 as zipfile
import requests
import io
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import pandas as pd

dict = {} 
list_city = []
list_startTime = []
list_endTime = []
list_description = []

#下載氣象局資料夾 並解壓縮
uri = 'http://opendata.cwb.gov.tw/opendataapi?dataid=F-D0047-093&authorizationkey=CWB-3F41A7B9-BAF0-4CCE-8A93-AFEBC64EF888'
#uri = 'http://opendata.cwb.gov.tw/opendataapi?dataid=F-D0047-093&authorizationkey=CWB-3FB0188A-5506-41BE-B42A-3785B42C3823'
res = requests.get(uri)
z = zipfile.ZipFile(io.BytesIO(res.content))
z.extractall(r'C:\Users\JENNIFER\Downloads\weatherData') #下載zip資料夾中所有檔案(已解壓縮)到指定資料夾

#開啟指定檔案 整理格式
weatherXML_path = r'C:\Users\JENNIFER\Downloads\weatherData\TAIWAN_72hr_CH.xml'
infile = open(weatherXML_path,'r',encoding = 'utf8')
weatherXML = infile.read()
soup = BeautifulSoup(weatherXML,'xml')
blocks = soup.select('location')

def changeTypeDatetime(textTime):
    temp_Time = textTime.split('T')[0]
    temp_Time2 = textTime.split('T')[1]
    temp_Time2 = temp_Time2.split('+')[0]
    datetime_Time = temp_Time +' '+ temp_Time2
#         print(datetime_startTime)
    sql_Time = datetime.datetime.strptime(datetime_Time,'%Y-%m-%d %H:%M:%S')
    return sql_Time
    
for block in blocks:
    
    location_block = block.select('locationName')[0].text #縣市名
    
    weather_block = block.select('weatherElement')[10] #weather_block(type:bs4.element.Tag)
    weather_description = weather_block.select('time')[0:8] #取前八個三小時區間 (type:list)
    
    for time_block in weather_description:
#         print(time_block) (type:bs4.element.Tag)
        sql_location = location_block
        list_city.append(sql_location)
        
        startTime = time_block.select('startTime')[0].text
        endTime = time_block.select('endTime')[0].text
        sql_startTime = changeTypeDatetime(startTime)
        sql_endTime = changeTypeDatetime(endTime)
        
        list_startTime.append(sql_startTime)
        list_endTime.append(sql_endTime)
        
        sql_description = time_block.select('value')[0].text
        list_description.append(sql_description)
            
infile.close()
dict = {'city':list_city,
        'startTime':list_startTime,
        'endTime':list_endTime,
        'description':list_description}
df = pd.DataFrame(dict, columns=['city','startTime','endTime','description'])

#把 Dataframe 資料寫進資料庫
listdata = df.values.tolist()

db = MySQLdb.connect(host="127.0.0.1",
    user="root", passwd="",
    db="webservice", charset="utf8")
cursor = db.cursor()

cleanSQL = "TRUNCATE TABLE weather"
cursor.execute(cleanSQL)

for dict in listdata:
#     print(dict)
    insertSQL = "INSERT INTO weather (city,startTime,endTime,description) VALUES ('%s', '%s', '%s', '%s')" % (dict[0],dict[1],dict[2],dict[3])
    cursor.execute(insertSQL)

db.commit()
db.close()
print('done')