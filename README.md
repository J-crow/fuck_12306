fuck_12306
=========

本人小白水平有限，文笔略水，文中有讲得不好的地方和错误的地方，恳请大神指出，并一同探讨。
***
python版本`python 3.6`

# 查票环节<br>
首先打开12306的查票界面，`查票的url`：https://kyfw.12306.cn/otn/leftTicket/init<br>
输入相应的信息（即车站和时间），并F12，Network<br>
![](https://github.com/J-crow/fuck_12306/raw/master/image/check.png)


可以看到有两个get请求<br>
第二个get请求明显是张图片，所以只关注第一个get请求<br>


打开第一个get，发现里面的是我所选的车站信息 ![](https://github.com/J-crow/fuck_12306/raw/master/image/check1.png)<br>

[0..99]那个列表可以猜到应该就是我查询的车次信息，与查询界面的车次信息进行对比，发现G1408是车次，IZQ,CWQ不知道是什么鬼，猜测是每个车站独有的代号<br>
既然猜测是每个车站独有的代号，那么应该在进入这个查票界面的时候会有相关的get请求；<br>
so我刷新再次进入这个界面  然后用了个比较笨的方法逐个请求寻找IZQ，果然在一个get请求里面找到了相应的信息 ![](https://github.com/J-crow/fuck_12306/raw/master/image/check1.png)<br>
