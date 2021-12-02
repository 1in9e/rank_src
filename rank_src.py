#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# __author__: _lin9e[https://www.ohlinge.cn]
# @Date:   2019-01-03 update2021202

import time
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# ASRC URL:
url_asrc = "https://security.alibaba.com/api/asrc/pub/people.json?&secretUid=xxxxxxxx"
# ASRC Current Rank
con_a = 5000		# 总积分
count_a = 10		# 漏洞数量

# BSRC URL:
url_bsrc = "https://bsrc.baidu.com/v2/api/user/000xxx000"
con_b = 5000		# 总积分
count_b = 10		# 漏洞数量

# EMAIL CONFIG
my_sender='test@163.com'    # 发件邮箱
my_pass = 'yourpassword'   		   # 发件密码
my_user='root@ohlinge.cn'      # 收件邮箱

headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Accept':'*/*',
	'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding':'gzip, deflate, br',
	'X-Requested-With':'XMLHttpRequest',
	'cookie':''
}

def mail(src_name, count):
    ret=True
    try:
        msg=MIMEText('[+] Your vuln is passed!','plain','utf-8')
        msg['From']=formataddr([str(src_name)+" Rank Robot",my_sender])  # 
        msg['To']=formataddr(["root",my_user])              # 
        msg['Subject']="Rank of this vuln  is {}".format(count)                # 
 
        server=smtplib.SMTP_SSL("smtp.163.com", 465)  # 
        server.login(my_sender, my_pass)  # 
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 
        server.quit()  # 
    except Exception as e:  # 
        print(e)
        ret=False
    return ret

def job_asrc():
	global con_a
	global count_a
	try:
		r = requests.get(url_asrc,headers=headers)
		js = json.loads(r.content)
		count = js['data']['finishedLeakNum']
		con = js['data']['profile']['historyCoin']
		con = con - con_a
		print("count_ = " + str(count_a))
		print("con_ = " + str(con_a))

		if int(count) > count_a:
			print('[+] Counts is '+str(count))
			ret=mail("ASRC", str(con))
			if ret:
			    print("[+] Success sending Email!")
			    con_a = con_a + con
			    count_a = count
			else:
			    print("[-] Failed sending Email!")
	except Exception as e:
		print(e)

def job_bsrc():
	global con_b
	global count_b
	try:
		r = requests.get(url_bsrc,headers=headers)
		js = json.loads(r.content)
		count = js['retdata']['user']['validBug']
		con = js['retdata']['user']['maxScore']
		con = con - con_b
		print("count_b = " + str(count_b))
		print("con_b = " + str(con_b))

		if int(count) > count_b:
			print('[+] Counts is '+str(count))
			ret=mail("BSRC", str(con))
			if ret:
			    print("[+] Success sending Email!")
			    con_b = con_b + con
			    count_b = count
			else:
			    print("[-] Failed sending Email!")
	except Exception as e:
		print(e)

# 简单定时任务, 不需要跑那个SRC注释掉相应job即可
def loopJob():
	while True:
		job_asrc()
		job_bsrc()
		time.sleep(300)		# 默认5分钟循环一次

loopJob()

