#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# __author__: 0h1in9e[https://www.ohlinge.cn]
# @Date:   2019-01-03
# Based-on Python 2.7

"""
部署linux服务器，使用nohup后台运行即可实现漏洞审核通过提醒：

$~: nohup python rank_asrc_model.py &

README:
	请求频率默认为5分钟一次，可修改：schedule.every(5).minutes.do(job)
	修改url secretUid为自己的uid
	修改发件/收件Email
	修改初始积分
"""

import time
import json
import requests
import schedule
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# URL为个人公开主页
url = "https://security.alibaba.com//api/asrc/pub/people.json?&secretUid=xxx"
headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Accept':'*/*',
	'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding':'gzip, deflate, br',
	'X-Requested-With':'XMLHttpRequest',
	'cookie':''
}

####
### 邮件发送模块
###
my_sender='xxx@163.com'    # 发件人邮箱账号
my_pass = 'xxx'   # 发件人邮箱密码
my_user='root@ohlinge.cn'      # 收件人邮箱账号，我这边发送给自己
def mail(obj):
    ret=True
    try:
        msg=MIMEText('漏洞审核啦！','plain','utf-8')
        msg['From']=formataddr(["积分助手",my_sender])  
        msg['To']=formataddr(["root",my_user])      
        msg['Subject']="这个漏洞积分为：{}".format(obj)

        server=smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25，465为ssl
        server.login(my_sender, my_pass)  # 发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception,e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print e
        ret=False
    return ret

#############
##### 初始积分 con_为当前安全币 count_为当前有效漏洞数
con_ = 3710
count_ = 73

def job():
	global con_
	global count_
	r = requests.get(url,headers=headers)
	js = json.loads(r.content)
	count = js['data']['finishedLeakNum']
	con = js['data']['profile']['historyCoin']
	con = con - con_
	print "count_ = " + str(count_)
	print "con_ = " + str(con_) 

	if int(count) > count_:
		#print '数量'+str(count)
		ret=mail(str(con))
		if ret:
		    print("邮件发送成功")
		    con_ = con_ + con
		    count_ = count
		else:
		    print("邮件发送失败")


schedule.every(5).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
