# 通过python的urllib来实现12306的查票，登录和购票

fuck_12306
=========

本人小白水平有限，文笔略水，文中有讲得不好的地方和错误的地方，恳请大神指出，并一同探讨。
***
python版本`python 3.6`

# 目录
* [查票环节](#查票环节)
* [登录12306](#登录12306)
* [购票环节](#购票环节)

推荐视频：[天善智能](http://blog.csdn.net/guodongxiaren) 天善智能里面找12306
        

****
# 查票环节<br>
首先打开12306的查票界面，`查票的url`：https://kyfw.12306.cn/otn/leftTicket/init<br>
输入相应的信息（即车站和时间），并F12，Network<br>
![](https://github.com/J-crow/fuck_12306/raw/master/image/check.png)


可以看到有两个get请求<br>
第二个get请求明显是张图片，所以只关注第一个get请求<br>


打开第一个get，发现里面的是我所选的车站信息 ![](https://github.com/J-crow/fuck_12306/raw/master/image/check1.png)<br>

[0..99]那个列表可以猜到应该就是我查询的车次信息，与查询界面的车次信息进行对比，发现G1408是车次，IZQ,CWQ不知道是什么鬼，猜测是每个车站独有的代号<br>
既然猜测是每个车站独有的代号，那么应该在进入这个查票界面的时候会有相关的get请求；<br>
so我刷新再次进入这个界面  然后用了个比较笨的方法逐个请求寻找IZQ，果然在一个get请求里面找到了相应的信息 ![](https://github.com/J-crow/fuck_12306/raw/master/image/check2.png)<br>

我试着去查询其他地方的车票，可以确定IZQ就是广州南的车站代号<br>
然后把那些车站代号的信息存为一个py文件<br>
通过`split`这个函数把车站代号构造成dict
```python
city={}
for i in station_names.split('@'):
    if i:
        city[i.split('|')[1]]=i.split('|')[2] #构造字典12306所有车站:代号
```

然而爬虫查票url是Headers里面的Request URL:https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2018-04-04&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=CSQ&purpose_codes=ADULT<br>
通过格式化代替url中的train_date,from_station,to_station,同样使用`split函数`让爬取的信息可视化
```python
ssl._create_default_https_context = ssl._create_unverified_context  #关闭证书验证
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
```
***
# 登录12306<br>
    **首先说明这个登录12306的方法没有使用机器学习相关方面的库，是通过返回值坐标值来通过验证码的**<br>
12306的`登录url`：https://kyfw.12306.cn/otn/login/init<br>
按照爬虫的基本登录套路，输入错误的登录信息和验证码。<br>
然后获得了一个get请求一个post请求 ![](https://github.com/J-crow/fuck_12306/raw/master/image/login1.png)<br>
点开来看可以知道get请求是验证码的图片，post的请求是验证码校验，没有登录用户相关的请求，所以可以猜测12306是先检验验证码然后再检验用户信息
![](https://github.com/J-crow/fuck_12306/raw/master/image/login3.png)  ![](https://github.com/J-crow/fuck_12306/raw/master/image/login2.png)<br>

既然是post请求就习惯性的去看Headers的Form data![](https://github.com/J-crow/fuck_12306/raw/master/image/login4.png)<br>

里面的数据也不知道是什么鬼，只能再试一次错误的登录看一下能不能找到破绽；<br>
这次登录我把所有的验证图片都选了，这次的post请求的data数据如下图：![](https://github.com/J-crow/fuck_12306/raw/master/image/login7.png)<br>

由上图可看出<br>
`login_site:E`是固定的<br>
`rand:sjrand`也是固定的<br>
而`answer:`是变化的，看着像是xy坐标<br>
我查找了相关的资料，也多次尝试选择错误的验证图片，尽可能点中图片的中间，最终确定`answer:`里面的参数是所点图片的坐标（就是说每个图都有个坐标范围，只要返回的`answer:`值在这个范围内就可以12306确定是那一张图片）<br>
然后我试一次正确的登录，一下子弹出5个post请求，一堆get请求。（我们需要关注主要是post请求，get请求不需要过多的关注，除非里面有post所需要的随机字符串）
![](https://github.com/J-crow/fuck_12306/raw/master/image/login8.png)<br>

随后我就通过Python来模拟登录，主要是模仿浏览器post请求<br>
      **注:要加入cookies值才能爬取相关信息并保持登录**<br>
 ****
```python
cjar=http.cookiejar.CookieJar()     #保存cookie值
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))   #加入保存后的cookie
urllib.request.install_opener(opener)   #将opener这个已经绑定cookie的函数加入request中
```
其中登录相关验证的post请求里面有个tk值是随机字符串![](https://github.com/J-crow/fuck_12306/raw/master/image/login9.png)<br>

我就往回找这个tk值，在这个post请求https://kyfw.12306.cn/passport/web/auth/uamtk 找到相应的tk值![](https://github.com/J-crow/fuck_12306/raw/master/image/login10.png)<br>
然后通过`urllib.parse.urlencode`返回form_data，记得要加消息头，最终实现登录。


# 购票环节<br>
购票环节比较繁琐，建议用抓包工具fiddler去寻找相关的随机数。

其中`预定信息提交的url`：https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest 里面的secretStr是每辆车次的随机字符串（在查票那个环节里面生成）<br>
![](https://github.com/J-crow/fuck_12306/raw/master/image/buy1.png)<br>
    而这段字符串有点坑爹<br>
    不知道是12306挖的坑还是正则表达式的转换问题  车次的随机数据%被替换成了%25 <br>
```python
data1=dpdata3.replace("%25","%")
data2=data1.encode('utf-8')
```
然后接下来寻找生成的随机数要给点耐心。<br>
就好比我要寻找TOKEN这个随机字符串，![](https://github.com/J-crow/fuck_12306/raw/master/image/buy2.png)<br>
要在前面请求的相应里面寻找![](https://github.com/J-crow/fuck_12306/raw/master/image/buy3.png)<br>

`url1`：https://kyfw.12306.cn/otn/confirmPassenger/initDc<br>
里面可以找到`leftTicketStr`,`Token`,`key_check_isChange`,`train_location`；<br>

`url2`:https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs<br>
里面可以找到`passenger_name`,`mobile_no`等相关的用户信息；<br>

`url3`:`"https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)`<br>
里面可以找到`orderSequence_no`<br>

其中还要注意这些随机字符串中的某一字段有没有被替换成其他字段。<br>

如下图的`passengerTicketStr`的`1,0,1`对应我所选的座位类型（这需要一个个的试出来，例如：`硬座`是`1,0,1`，`无座`是`3,0,1`）
![](https://github.com/J-crow/fuck_12306/raw/master/image/buy4.png)<br>

然而最令人头痛的是`格林时间`-`GMT`![](https://github.com/J-crow/fuck_12306/raw/master/image/buy5.png)<br>
如上图`train_date`就是格林时间`GMT`  `seatType`是所选座位类型。<br>
12306的`GMT`形式是`星期`+`月`+`日`+`年`+`00:00:00`+`GMT`+`0800`;<br>
```python
#将日期转为格林时间  gmt
datestr=train_date       #需要的买票时间
#先将字符串形式的时间转为常规时间格式        strptime格式化输出
date1=datetime.datetime.strptime(datestr,"%Y-%m-%d").date()
#再转为对应的格林时间
gmt='%a+%b+%d+%Y'    #a是星期的英文单词的缩写  b是月份的英文单词的缩写
gmtdate=date1.strftime(gmt)
```

返回这么多个post请求，终于买到票了<br>
然而却是另一番景象--->30分钟的排队等票<br>
我万脸懵逼，百度了一下办法，也无果，碰巧有一天在知乎上有人说加延时可跳过排队；<br>
```python
time.sleep(1)
```
这个方法确实可以跳过排队，但是我觉得程序抢票的宗旨是要快，加了延时感觉违背了宗旨，不知道有没有大神可以解答一下这个问题。

这段代码也不知道能撑多久，听说12306又更新了<br>
本文仅供学习参考，不做商业用途.<br>


