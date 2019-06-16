#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

#import launcher

key = 'GPNYeB7snGIfFy9SjaOSs4RJlIn%2B4uAYYlq9ISmcNodo3AQX4uD6DS3M1%2FpXXHQ5IhR%2FUOewInIr%2F0WN4%2BdBdA%3D%3D'
TOKEN = '886975265:AAGNwVYRGIShdu4tf95OwRp6HHbwaMskYy4'
MAX_MSG_LENGTH = 300
baseurl = 'apis.data.go.kr/1741000/EarthquakeIndoors/getEarthquakeIndoorsList?serviceKey='+key
bot = telepot.Bot(TOKEN)

def getData(command_param=None, subCommand_param=None):
    res_list=[]
    for i in range(10):
        url = 'http://' + baseurl+'&pageNo='+str(i)+'&numOfRows=1000&type=xml&flag=Y'
        res_body = urlopen(url).read()
        soup = BeautifulSoup(res_body, 'html.parser')
        items = soup.findAll('row')
        for item in items:
            if item.find('ctprvn_nm').text == command_param and item.find('sgg_nm').text == subCommand_param:
                res_list.append("주소 : "+item.find('dtl_adres').text+" /관리자 : "+item.find('mngps_nm').text+" /전화번호 : "+item.find('mngps_telno').text+"\n")
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run():
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, param)
        res_list = getData( param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run()
