#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@author: 韦炜,J-crow
#@GitHub:J-crow

import urllib.request
import http.cookiejar
import urllib.parse
import re
import ssl
import datetime
import time
import json
import user
from mark import station_names

#关闭证书验证
ssl._create_default_https_context = ssl._create_unverified_context

city={}
for i in station_names.split('@'):
    if i:
        city[i.split('|')[1]]=i.split('|')[2] #构造字典12306所有车站:车次代号

#train_date=input('出发时间，列如 2018-04-04: ')
#fs=input('出发城市,例如 广州: ')
#ts=input('到达城市,例如 重庆: ')
train_date='2018-03-29'
fs='重庆'
ts='长沙'
from_station=city[fs]
to_station=city[ts]
type=3 ##input('座位类型,软卧输入1，硬卧输入2，硬座输入3，无座输入4: ')
#type=input('座位类型,软卧输入1，硬卧输入2，硬座输入3，无座输入4: ')
#车次：[3]
#出发时间：[8]
#到达时间：[9]
#软卧：[23]
#硬卧：[26]
#硬座：[28]
#无座：[29]
dp_reg=urllib.request.Request("https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT"%(train_date,from_station ,to_station))

dp_reg.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
station={}
station2={}
def geturl():
    #读取HTML，并转码
    dphtml=urllib.request.urlopen(dp_reg).read().decode("utf-8")
    #把json字符串转换为dict
    dpdict=json.loads(dphtml)
    #dict字典里面的data里面的result是所需要的车次信息
    result=dpdict['data']['result']
    for r in result:
        a=r.split('|')
        if type==1:
            if a[23]=='无' or not a[23]:  #a[23]软卧的值等于False时继续查找
                continue
            #储存车次信息,通过键入车次名输出12306的车次随机数
            station[a[3]]=a[0]
            station2[a[3]] = a[2]
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


##########登录###########

##cookie相当于网站给用户的密钥
cjar=http.cookiejar.CookieJar()     #保存cookie值
#加入保存后的cookie
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
#将opener这个已经绑定cookie的函数加入request中
urllib.request.install_opener(opener)

yzmurl="https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand"           #验证码网址
j="D:\GAMES\py3.6.3\web_12306\\yzm.jpg"   #保存验证码的地址

#生成req
yzmreq=urllib.request.Request(yzmurl)
#加入头信息
yzmreq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
#yzmhtml=urllib.request.urlopen(yzmreq).read()
#保存验证码到j这个地址
urllib.request.urlretrieve(yzmurl,j)


#验证码的网络接口
yzmposturl='https://kyfw.12306.cn/passport/captcha/captcha-check'
#x坐标(35,105,175,245)，y坐标(35,110)
#验证码坐标函数
def getxy(inputxy):
    s=inputxy.split(',')  # 分割用户输入的验证码位置
    # 验证正确验证码的坐标列表(大概值)
    yzmxy=['35,35', '105,35', '175,35', '245,35', '35,110', '105,110', '175,110', '245,110']
    yzmlist=[]
    for i in s:
        # 迭代生成正确验证码的坐标
        yzmlist.append(yzmxy[int(i)])
    # 正确验证码的坐标拼接成字符串，作为网络请求时的参数
    xy= ','.join(yzmlist)  #以,为分隔符  生成字符串
    return xy
codexy=getxy(input('输入正确的验证码编号,由左往右依次是0到7,如果有多个请用,隔开: '))


#将字典类型转化为字符串类型
yzmdata=urllib.parse.urlencode({
"answer":codexy,
"login_site":"E",
"rand":"sjrand"
}).encode('utf-8')
#加入yzmdata 并且post
yzmpostreq=urllib.request.Request(yzmposturl,yzmdata)
yzmreq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
yzmhtml=urllib.request.urlopen(yzmpostreq).read().decode("utf-8")
print(yzmhtml)
result1=json.loads(yzmhtml)
if result1["result_code"]=='4':
    print('验证成功')
else:
    print('验证失败')


loginurl="https://kyfw.12306.cn/otn/login/init#"
loginreq=urllib.request.Request(loginurl)
loginreq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
req0data=urllib.request.urlopen(loginreq).read().decode("utf-8")
#12306的登录接口
loginposturl="https://kyfw.12306.cn/passport/web/login"
#user的data
loginpostdata=urllib.parse.urlencode({
"username":user.username,    #用户名
"password":user.password,    #用户密码
"appid":"otn"
}).encode('utf-8')
#加入user的data 并post
loginpostreq=urllib.request.Request(loginposturl,loginpostdata)
loginhtml=urllib.request.urlopen(loginpostreq).read().decode("utf-8")
print(loginhtml)
result2=json.loads(loginhtml)
if result2["result_code"]==0:
    print('登陆成功')
else:
    print('登录失败')

#其他登录的相关验证
#1
loginposturl1='https://kyfw.12306.cn/otn/login/userLogin'
loginpostdata1=urllib.parse.urlencode({
"_json_att":""
}).encode('utf-8')
loginreq1=urllib.request.Request(loginposturl1,loginpostdata1)
loginreq1.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
loginhtml1=urllib.request.urlopen(loginreq1).read().decode("utf-8")

#2
loginposturl2="https://kyfw.12306.cn/passport/web/auth/uamtk"
loginpostdata2=urllib.parse.urlencode({
"appid":"otn"
}).encode('utf-8')
loginreq2=urllib.request.Request(loginposturl2,loginpostdata2)
loginreq2.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
loginhtml2=urllib.request.urlopen(loginreq2).read().decode("utf-8")
logindict2=json.loads(loginhtml2)
tk=logindict2['newapptk']
print(logindict2['result_message'],tk)

#3
loginposturl3="https://kyfw.12306.cn/otn/uamauthclient"
loginpostdata3=urllib.parse.urlencode({
"tk":tk
}).encode('utf-8')
loginreq3=urllib.request.Request(loginposturl3,loginpostdata3)
loginreq3.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
loginhtml3=urllib.request.urlopen(loginreq3).read().decode("utf-8")
logindict3=json.loads(loginhtml3)
print(logindict3['result_message'],tk)


#爬个人中心页面
centerurl="https://kyfw.12306.cn/otn/index/initMy12306"
centerreq=urllib.request.Request(centerurl)
centerreq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
centerhtml=urllib.request.urlopen(centerreq).read().decode("utf-8")

#订票
#订票界面
dpurl="https://kyfw.12306.cn/otn/leftTicket/init"
dpreq=urllib.request.Request(dpurl)
dpreq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
dphtml=urllib.request.urlopen(dpreq).read().decode("utf-8")
#再爬对应订票信息
dpurl1="https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT"%(train_date,from_station ,to_station)
dpreq1=urllib.request.Request(dpurl1)
dpreq1.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
dphtml1=urllib.request.urlopen(dpreq1).read().decode("utf-8")

#订票 第1次post   check用户
dpurl2="https://kyfw.12306.cn/otn/login/checkUser"
dpdata2=urllib.parse.urlencode({
"_json_att":""
}).encode('utf-8')
dpreq2=urllib.request.Request(dpurl2,dpdata2)
dpreq2.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
dphtml2=urllib.request.urlopen(dpreq2).read().decode("utf-8")
dpdict2=json.loads(dphtml2)
print(dpdict2["httpstatus"])

cc=input("请输入要预定的车次：")

#读取当前日期，用于backdate
backdate=datetime.datetime.now()
backdate=backdate.strftime("%Y-%m-%d")
#订票  第2次post  进行预订信息的提交
dpurl3="https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
dpdata3=urllib.parse.urlencode({
   "back_train_date":backdate,
   "purpose_codes":"ADULT",
   "query_from_station_name":fs,
   "query_to_station_name":ts,
   "secretStr":station[cc],
   "tour_flag":"dc",
   "train_date":train_date,
   "undefined":""
})#.encode('utf-8')
#({
#"secretStr":station[cc],
#"train_date":train_date,
#"back_train_date":backdate,
#"tour_flag":"dc",
#"purpose_codes":"ADULT",
#"query_from_station_name":fs,
#"query_to_station_name":ts
#})#.encode('utf-8')
#print(dpdata3.encode('utf-8'))
#不知道是12306挖的坑还是正则表达式的转换问题   车次的随机数据%被替换成了%25
data1=dpdata3.replace("%25","%")
data2=data1.encode('utf-8')
#print(data2)
#print(station[cc].encode('utf-8'))
#print(station[cc].replace("%25","%").encode('utf-8'))
dpreq3=urllib.request.Request(dpurl3,data2)
dpreq3.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
dphtml3=urllib.request.urlopen(dpreq3).read().decode("utf-8")
dpdict3=json.loads(dphtml3)
print(dpdict3["httpstatus"])

#订票 第3次post  获取12306随机生成的formdata数
dpurl4="https://kyfw.12306.cn/otn/confirmPassenger/initDc"
dpdata4=urllib.parse.urlencode({
"_json_att":""
}).encode('utf-8')
dpreq4=urllib.request.Request(dpurl4,dpdata4)
dpreq4.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
dphtml4=urllib.request.urlopen(dpreq4).read().decode("utf-8")

#post完之后，获取leftTicketStr
#正则表达式寻找（.*?）
paleft="'leftTicketStr':'(.*?)'"
#列表形式返回匹配到的字符串  re.compile正则匹配paleft  findall以列表形式返回
leftstrall=re.compile(paleft).findall(dphtml4)
#判断leftstrall是否有参数
if(len(leftstrall)!=0):
    leftstr=leftstrall[0]
    print(leftstr)
else:
    print("leftTicketStr获取失败")
patoken="var globalRepeatSubmitToken.*?'(.*?)'"
pakey="'key_check_isChange':'(.*?)'"
tokenall=re.compile(patoken).findall(dphtml4)
if(len(tokenall)!=0):
    token=tokenall[0]
    print(token)
else:
    print("Token获取失败")
keyall=re.compile(pakey).findall(dphtml4)
if(len(keyall)!=0):
    key=keyall[0]
    print(key)
else:
    print("key_check_isChange获取失败")
#还需要获取train_location
patrain_location="'tour_flag':'dc','train_location':'(.*?)'"
train_locationall=re.compile(patrain_location).findall(dphtml4)
if(len(train_locationall)!=0):
    train_location=train_locationall[0]
    print(train_location)
else:
    print("train_location获取失败")
#订票  第4次post  应该是get用户信息
dpurl5="https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
dpdata5=urllib.parse.urlencode({
"REPEAT_SUBMIT_TOKEN":token,
"_json_att":""
}).encode('utf-8')
dpreq5=urllib.request.Request(dpurl5,dpdata5)
dpreq5.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
dphtml5=urllib.request.urlopen(dpreq5).read().decode("utf-8")
#通过正则表达式获取用户信息
#提取姓名
passenger_name='"passenger_name":"(.*?)"'
#提取身份证
passenger_id_no='"passenger_id_no":"(.*?)"'
#提取手机号
mobile_no='"mobile_no":"(.*?)"'
#提取对应乘客所在的国家
country_code='"country_code":"(.*?)"'
nameall=re.compile(passenger_name).findall(dphtml5)
idall=re.compile(passenger_id_no).findall(dphtml5)
mobileall=re.compile(mobile_no).findall(dphtml5)
#countryall=re.compile(country_code).findall(dphtml5)
print(nameall[0])
print(idall[0])
print(mobileall[0])


#确认订票
#第1次post
confirmurl="https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"

confirmdata=urllib.parse.urlencode({
"cancel_flag":"2",
"bed_level_order_num":"000000000000000000000000000000",
"passengerTicketStr":"1,0,1,%s,1,%s,%s,N"%(nameall[0],idall[0],mobileall[0]),
"oldPassengerStr":"%s,1,%s,1_"%(nameall[0],idall[0]),
"tour_flag":"dc",
"randCode":"",
"whatsSelect":"1",
"_json_att":"",
"REPEAT_SUBMIT_TOKEN":token
}).encode('utf-8')
confirmreq=urllib.request.Request(confirmurl,confirmdata)
confirmreq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
confirmhtml=urllib.request.urlopen(confirmreq).read().decode("utf-8")
confirmdict=json.loads(confirmhtml)
time.sleep(1)
print(confirmdict["httpstatus"])
print("第1次post")

#第2次post
confirmurl2="https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
#将日期转为格林时间  gmt
datestr=train_date       #需要的买票时间
#先将字符串形式的时间转为常规时间格式        strptime格式化输出
date1=datetime.datetime.strptime(datestr,"%Y-%m-%d").date()
#再转为对应的格林时间
gmt='%a+%b+%d+%Y'    #a是星期的英文单词的缩写  b是月份的英文单词的缩写
gmtdate=date1.strftime(gmt)
#将leftstr2转成指定格式
leftstr2=leftstr.replace("%","%25")
confirmdata2="train_date="+str(gmtdate)+"+00%3A00%3A00+GMT%2B0800&train_no="+station2[cc]+"&stationTrainCode="+cc+"&seatType=3&fromStationTelecode="+from_station+"&toStationTelecode="+to_station+"&leftTicket="+leftstr2+"&purpose_codes=00&train_location=%s&_json_att=&REPEAT_SUBMIT_TOKEN=%s"%(train_location,token)
confirmdata_2=urllib.parse.urlencode({
"train_date":"%s 00:00:00 GMT+0800"%gmtdate,
"train_no":station2[cc],
"stationTrainCode":cc,
"seatType":"1",
"fromStationTelecode":from_station,
"toStationTelecode":to_station,
"leftTicket":leftstr2,
"purpose_codes":"00",
"train_location":train_location,
"_json_att":"",
"REPEAT_SUBMIT_TOKEN":token}).encode('utf-8')
getdata=confirmdata2.encode('utf-8')
#getdata_2=confirmdata_2.encode('utf-8')
confirmreq2=urllib.request.Request(confirmurl2,getdata)
print(getdata)
print(confirmdata_2)
confirmreq2.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
confirmhtml2=urllib.request.urlopen(confirmreq2).read().decode("utf-8")
time.sleep(2)
print("第2次post")


#第3次post
confirmurl3="https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
confirmdata3=urllib.parse.urlencode({
"passengerTicketStr":"1,0,1,%s,1,%s,%s,N"%(nameall[0],idall[0],mobileall[0]),
"oldPassengerStr":"%s,1,%s,1_"%(nameall[0],idall[0]),
"tour_flag":"dc",
"randCode":"",
"purpose_codes":"00",
"key_check_isChange":key,
"leftTicketStr":leftstr,
"train_location":train_location,
"choose_seats":"",
"seatDetailType":"000",
"whatsSelect":"1",
"roomType":"00",
"dwAll":"N",
"_json_att":"",
"REPEAT_SUBMIT_TOKEN":token,
}).encode('utf-8')
print(confirmdata3)
confirmreq3=urllib.request.Request(confirmurl3,confirmdata3)
confirmreq3.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
confirmhtml3=urllib.request.urlopen(confirmreq3).read().decode("utf-8")
time.sleep(1)
print("第3次post")

#获取orderid的随机值
getorderidurl="https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
getreq=urllib.request.Request(getorderidurl)
getreq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
orderhtml=urllib.request.urlopen(getreq).read().decode("utf-8")
getorderid='"orderId":"(.*?)"'
orderidall=re.compile(getorderid).findall(orderhtml)
if(len(orderidall)!=0):
    orderid=orderidall[0]
else:
    print("预订成功,3秒后程序退出")
    exit(3)
time.sleep(1)
print("获取orderid成功")

#第4次post
confirmurl4="https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
confirmdata4=urllib.parse.urlencode({
    "orderSequence_no":orderid,
    "_json_att":"",
    "REPEAT_SUBMIT_TOKEN":token}).encode('utf-8')
confirmreq4=urllib.request.Request(confirmurl4,confirmdata4)
confirmreq4.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
confirmhtml4=urllib.request.urlopen(confirmreq4).read().decode("utf-8")
time.sleep(1)
print("第4次post")


#第5次post
confirmurl5="https://kyfw.12306.cn/otn//payOrder/init"
confirmdata5=urllib.parse.urlencode({
    "_json_att":"",
    "REPEAT_SUBMIT_TOKEN":token}).encode('utf-8')
confirmreq5=urllib.request.Request(confirmurl5,confirmdata5)
confirmreq5.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
confirmhtml5=urllib.request.urlopen(confirmreq5).read().decode("utf-8")
print("购票成功")
