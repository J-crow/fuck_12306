#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import ssl
import json
from mark import station_names
ssl._create_default_https_context = ssl._create_unverified_context  #关闭证书验证

city={}
for i in station_names.split('@'):
    if i:
        city[i.split('|')[1]]=i.split('|')[2] #构造字典12306所有车站:代号

train_date='2018-03-29'##input('出发时间，列如 2018-04-04: ')
##fs=input('出发城市,例如 成都: ')
##ts=input('到达城市,例如 成都: ')
fs="成都"
ts="长沙"
from_station=city[fs]
to_station=city[ts]
type=4 ##input('座位类型,软卧输入1，硬卧输入2，硬座输入3，无座输入4: ')
#车次：[3]
#出发时间：[8]
#到达时间：[9]
#软卧：[23]
#硬卧：[26]
#硬座：[28]
#无座：[29]
dp_reg="https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT"%(train_date,from_station ,to_station)
station={}
station2={}
def geturl():
    dphtml=urllib.request.urlopen(dp_reg).read().decode("utf-8")     #读取HTML，并转码
    dpdict=json.loads(dphtml)                 #把json字符串转换为dict
    result=dpdict['data']['result']         #dict字典里面的data里面的result是所需要的车次信息
    for r in result:
        a=r.split('|')
        if type==1:
            if a[23]=='无' or not a[23]:  #a[23]软卧的值等于False时继续查找
                continue
            #储存车次信息,通过键入车次名输出12306的车次随机数
            station[a[3]]=a[0]
            station2[a[3]]=a[2]
            print('软卧有票,车次:%s'%a[3],a[0])
        if type==2:
            if a[26]=='无' or not a[26]:  #a[26]硬卧的值等于False时继续查找
                continue
            station[a[3]] = a[0]
            station2[a[3]] = a[2]
            print('硬卧有票,车次:%s'%a[3],a[0])
        if type==3:
            if a[28]=='无' or not a[28]:  #a[28]硬座的值等于False时继续查找
                continue
            station[a[3]] = a[0]
            station2[a[3]] = a[2]
            print('硬座有票,车次:%s'%a[3],a[0])
        if type==4:
            if a[29]=='无' or not a[29]:  #a[29]无座的值等于False时继续查找
                continue
            station[a[3]] = a[0]
            station2[a[3]] = a[2]
            print('无座有票,车次:%s'%a[3],a[0])
            print(station2)

geturl()
