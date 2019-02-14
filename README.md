# rank_asrc

> 监控个人在asrc漏洞审核情况，并自动发邮件及时提醒

### Usage

> 部署linux服务器，使用nohup后台运行即可实现漏洞审核通过提醒：

```
➜  ~ nohup python rank_asrc_model.py &
```

### change code

 - 请求频率默认为5分钟一次，可修改：schedule.every(5).minutes.do(job)
 - 修改url secretUid为自己的uid
 - 修改发件/收件Email
 - 修改初始积分
