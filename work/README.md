# 工作相关脚本


***
### CVE-Monitor.py
该脚本是根据https://cassandra.cerias.purdue.edu/CVE_changes/today.html 监控最新CVE信息。然后入库并发送结果到邮件。
主要包括以下几个方面。
1. 获取最新的CVE列表和详情
主要采用了python的requests模块和BeautifulSoup模块。
2. 将最新的CVE信息存入数据库
数据库使用了Mongodb，采用了pymongo模块。
3. 通过邮件发送最新的CVE信息
发送邮件采用了smtplib模块。
4. 定时执行任务
使用了linux的crontab来实现。



使用方法：

1. 下载脚本，按装所需的依赖库

requirements.txt
```
pymongo==3.6.0
requests==2.18.4
beautifulsoup4==4.6.0
```
2. 数据库操作
	这里采用的是Mongodb，也可以换成其他数据库。或者不用数据库（不用的话将相关的代码屏蔽即可）。
    
    1.数据库安装
	Ubuntu下可以使用`apt-get install mongodb`。CentOS下的安装可以参考[CentOS 安装MongoDB](http://blog.csdn.net/yima1006/article/details/9840239)
    
    2.创建数据库存储文件位置
```bash
mkdir /var/data/ #创建数据存储位置
mongod --port 65521 --dbpath /var/data/ --bind_ip 127.0.0.1 #启动mongodb，指定端口和路径，且仅本机可连
mongo 127.0.0.1:65521/mydb 
db.createUser({user:'tass',pwd:'liehu',roles:[{role:'dbOwner',db:'mydb'}]}) #添加认证
```
    3.修改代码中数据库配置
```python
def addData(data):
    DBNAME = 'mydb'
    DBUSERNAME = 'tass'
    DBPASSWORD = 'liehu'
    DB = '127.0.0.1'
    PORT = 65521
```
3. 修改邮箱信息为自己的

```python
def sendEmail(mail_msg):  # 发送邮件
    sender = 'from@163.com' # 发件人
    password = 'password' # 发件人密码
    receiver = 'receiver@163.com' # 收件人
```
具体可以参考博客：https://fuping.site/2017/12/11/NEW-CVE-Monitor/
