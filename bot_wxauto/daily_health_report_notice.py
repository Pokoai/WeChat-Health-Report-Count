#! python
# daily_health_report_notice.py - 每日健康打卡提醒以及统计未打卡名单

from wxauto import *
import schedule
import time
import os

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# Init
wx = WeChat()  # 获取当前微信客户端
wx.GetSessionList()  # 获取会话列表

# 群内所有人员微信名
name_list = [
    "XXX1", "XXX2",
]

# 真实姓名映射
name_dic = {
    "XXX1": "XXX",
    "XXX2": "XXX",
}

# 遗漏的人员名单
name_out_set = set()

# 有未打卡人员标志位
flg_unclock = 1


self_intro = '''0w0蔻你吉瓦~\n
我是一个健康打卡提醒 Bot，\n
每天4次提醒健康打卡及出入杭情况确认。\n
随开发者的心情迭代，\n
并且可能会随着某一次的更新去世qaq'''

msg_auto = '''-------------------------------\n
大家好，我是本群的【健康打卡&报备提醒小助手】\n
您今天打卡了吗？(若已打卡，请回复“已打卡”)\n
您离杭报备了吗？\n
小助手提醒您：实验千万条，打卡第一条；出门不报备，禁闭两行泪。\n
-------------------------------'''

msg_functions = '''目前实现的功能：\n
1. 自动化定时发放通知；\n
2. 自动化提醒未打卡人员；\n
3. 功能查询；'''

msg_start = "！！！今日健康打卡开始 ！！！"

msg_end = "~~~~~~~~~~END~~~~~~~~~"


# 开始打卡通知
def start_clock_notice():
    global flg_unclock
    flg_unclock = 1  # 有未打卡人员标志位置1

    # 开始提醒
    WxUtils.SetClipboard(msg_start)
    wx.SendClipboard()

    # 打卡提醒
    WxUtils.SetClipboard(msg_auto)
    wx.SendClipboard()


# 打卡提醒并统计
def clock_notice_count():
    global flg_unclock

    # 若全员已打卡，则跳过该程序
    if 1 == flg_unclock:
        who = '微信机器人测试群'
        wx.ChatWith(who)

        # 打卡提醒
        WxUtils.SetClipboard(msg_auto)
        wx.SendClipboard()

        # 更新未打卡名单
        count_unclock()
    else:
        pass


# 微信名映射为真实姓名
def wxname2true_name(name_list):
    true_name_list = []
    for name in name_list:
        true_name_list.append(name_dic[name])

    return true_name_list

# 统计函数
def count_unclock():
    global flg_unclock
    flg_name_out = 0  # 遗漏名单标志位

    name_unclock = name_list.copy()  # 未打卡名单初始化
    msg_db = {}

    who = '微信机器人测试群'
    wx.ChatWith(who)
    wx.LoadMoreMessage()
    msgs = wx.GetAllMessage
    msgs = msgs[::-1]
    # print(msgs)
    for msg in msgs:
        # 管理员发送的开始信号作为循环结束条件
        if msg[0] == "TTup" and ("开始" in msg[1] or msg[1] == msg_start):
            break
        elif msg[0] == "SYS" or msg[0] == "TTup":  # 忽视系统和管理员的发言
            continue
        else:
            # 更新未打卡名单
            try:
                name_unclock.remove(msg[0])
            except:  # 如果发言者不在未打卡名单里
                if msg[0] not in name_list:   # 同时也不在所有名单里
                    name_out_set.add(msg[0])  # 添加到遗漏名单中
                    print("Name not find:" + msg[0])
                    flg_name_out = 1
            # else:
                # 爬取群聊内容，根据内容对发送者进行分类
                # try:
                #     msg_db[msg[1]] += "," + msg[0]
                #     # print(msg_db)
                # except:
                #     msg_db[msg[1]] = msg[0]
                #     # print(msg_db)

    # msg_sign_situation = ""
    # for type in msg_db:
    #     msg_sign_situation += str(type) + ": " + str(msg_db[type]) + ";;;"
    # print(msg_sign_situation)
    # print(name_list)
    # wx.SendMsg(msg_sign_situation)

    if name_unclock == []:
        wx.SendMsg("恭喜，全员打卡完成！" )
        flg_unclock = 0
    else:
        true_name_unclock = wxname2true_name(name_unclock)
        wx.SendMsg("未打卡人员：" + '，'.join(true_name_unclock))

    if 1 == flg_name_out:
        flg_name_out = 0
        wx.SendMsg("遗漏名单：" + '，'.join(list(name_out_set)))


# 监视聊天中有没有出现命令指令，如果出现了，就立刻执行相关指令
def listen_order():
    msgs = wx.GetAllMessage
    # print(msgs)
    for msg in msgs[::-1]:
        info = msg[1]  # ('TTup', '介绍', '4252629441034')
        if "END" in info or info == msg_end:
            break
        elif info == "INTRO":
            # wx.SendMsg(self_intro)
            WxUtils.SetClipboard(self_intro)
            wx.SendClipboard()
            wx.SendMsg(msg_end)
        elif info == "FUNC":
            # wx.SendMsg(msg_functions)
            WxUtils.SetClipboard(msg_functions)
            wx.SendClipboard()
            wx.SendMsg(msg_end)
        elif info == "NAME":
            true_name_list = wxname2true_name(name_list)
            wx.SendMsg(" ".join(true_name_list))
            wx.SendMsg(msg_end)
        elif info == "RESTART":
            wx.SendMsg("机器人已重启，请所有人重新上报一次！")
            start_clock_notice()
            wx.SendMsg(msg_end)
        elif info == "NOTICE":
            count_unclock()
            wx.SendMsg(msg_end)
        else:
            continue


def webot_health_notice():
    
    # 获取当前微信客户端
    wx = WeChat()
    # 获取会话列表
    wx.GetSessionList()

    # 一天内只要重新运行程序，必须从count()开始
    # count_unclock()

    schedule.every().day.at("09:00").do(start_clock_notice)
    
    schedule.every().day.at("12:15").do(clock_notice_count)
    schedule.every().day.at("18:00").do(clock_notice_count)
    schedule.every().day.at("23:00").do(clock_notice_count)


    # schedule.every(1).minutes.do(Listen_Order)
    schedule.every(10).seconds.do(listen_order)

    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)



if __name__ == '__main__':
    webot_health_notice()
