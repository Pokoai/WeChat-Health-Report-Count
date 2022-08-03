#! python
# send_msg_to_friends.py - 给微信群和好友发送消息，已集成到wechat2pdf中，公众号有新文章发布时，通知到微信群

import pywintypes # 务必加这一句，否则会报错"ImportError: DLL load failed while importing win32gui: 找不到指定的程序。"

from wxauto import WeChat
import time, random


# 需要群发的好友 ["备注名", "称呼(自定义)"]
whos = [["微信机器人测试群", "虚拟用户"], ["文件传输助手", "助手"]]

# 需要发送的消息
msg = "，测试中，请查收。"
# file1 = "D:/Media/Desktop/wechat2pdf/日记/1.E篇日记——关于做人的底线。22年6月27日。-2022-06-27(img).pdf"
# file2 = "E:/FileSave/data.zip"

wx = WeChat()  # 获取当前微信客户端
wx.GetSessionList()  # 获取会话列表

for who in whos:
    username = who[0]
    message = who[1] + msg  # 称呼和发送消息合并
    # print(message)
    time.sleep(random.randint(5, 8))  # 随机等待10-20s

    wx.ChatWith(username)  # 打开聊天窗口
    # wx.Search(username) # 查找微信好友，不会在当前聊天栏滚动查找
    wx.SendMsg(message)
    # wx.SendFiles(file1)  # 可发送多个文件

    print("发送成功：", who[0])

print("全部发送完成")
wx.ChatWith(whos[1][0])
wx.SendMsg("全部发送完成！")