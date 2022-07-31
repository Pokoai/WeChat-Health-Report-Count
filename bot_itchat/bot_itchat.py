#!/usr/bin/env python
# -*- coding:utf-8 -*-

import itchat
import schedule
import time
import datetime

# 登陆网页端微信，有的微信号可能登陆不上
itchat.auto_login(hotReload=True)

# 查找微信群，替换"XXX"为你要发送消息的群名称即可，一定要先将群保存到通讯录才可以！
chatroom = itchat.search_chatrooms(name=u"XXX")
userName = chatroom[0][u'UserName']

# 循环打卡三次，每次间隔1秒
def job():
    for i in range(3):
        itchat.send("打卡", toUserName=userName)
        time.sleep(1)

# 每天固定时间运行job，可自定义引号中的时间
schedule.every().day.at("08:20").do(job)
schedule.every().day.at("17:35").do(job)

while True:
    schedule.run_pending()
    # 在运行时打印当前时间
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')[11:]
    print('\r{}'.format(now), end='')
