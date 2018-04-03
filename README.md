fuck_12306
=========

本人小白水平有限，文笔略水，文中有讲得不好的地方和错误的地方，恳请大神指出，并一同探讨。
***
python版本`python 3.6`

# 查票环节<br>
首先打开12306的查票界面，`查票的url`：https://kyfw.12306.cn/otn/leftTicket/init<br>
输入相应的信息（即车站和时间），并F12，Network<br>
![](https://github.com/J-crow/fuck_12306/raw/master/image/check.png)<br>
可以看到有两个get请求<br>
第二个get请求明显是张图片，所以我们只关注第一个get请求<br>

打开第一个get，发现里面的是我们所选的车站信息 ![](https://github.com/J-crow/fuck_12306/raw/master/image/check.png)<br>
