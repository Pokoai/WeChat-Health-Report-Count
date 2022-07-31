#! python
# demo.py - 给微信好友发送消息模板

import pywintypes  # 务必加这一句，否则会报错"ImportError: DLL load failed while importing win32gui: 找不到指定的程序。"

from wxauto import WeChat
import time, random

# 需要群发的好友 ["好友备注名", "称呼(自定义)"]
whos = [["微信备注名A", "称呼A"], ["微信备注名B", "称呼B"]]

# 需要发送的消息
msg = "，测试中，请查收。"
file1 = "E:/FileSave/QRcode.jpg"
file2 = "E:/FileSave/data.zip"

wx = WeChat()  # 获取当前微信客户端
wx.GetSessionList()  # 获取会话列表

for who in whos:
    who = who[0]
    message = who[1] + msg  # 称呼和发送消息合并
    time.sleep(random.randint(10, 20))  # 随机等待10-20s

    wx.ChatWith(who)  # 打开聊天窗口
    # wx.Search(who) # 查找微信好友，不会在当前聊天栏滚动查找
    wx.SendMsg(message)
    wx.SendFiles(file1, file2)  # 可发送多个文件

    print("发送成功：", who[0])
print("All end send")