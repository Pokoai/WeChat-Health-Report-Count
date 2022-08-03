#! python
# daily_health_report_notice.py - 每日健康打卡提醒以及统计未打卡名单

from wxauto import *
import schedule
import time
import os

import requests


# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"

# Init
wx = WeChat()  # 获取当前微信客户端
wx.GetSessionList()  # 获取会话列表

wechat_group = '微信机器人测试群'  # 微信群名称

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
我还提供如下几个功能，直接回复括号内关键词获取：
1. 天气预报(tq)；
2. 笑话(xh)；
3. 电影票房排行榜(dy);
-------------------------------'''

msg_functions = '''目前实现的功能（直接回复括号内关键词获取）：\n
1. 天气预报(tq)；\n
2. 笑话(xh)；\n
3. 电影票房排行榜(dy);\n
4. 自动化定时发放通知；
5. 自动化提醒未打卡人员；
'''

msg_start = "！！！今日健康打卡开始 ！！！"

msg_end = "~~~~~~~~~~END~~~~~~~~~"


# 开始打卡通知
def start_clock_notice():
    global flg_unclock
    flg_unclock = 1  # 有未打卡人员标志位置1

    who = wechat_group
    wx.ChatWith(who)
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
        who = wechat_group
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

    who = wechat_group
    wx.ChatWith(who)
    wx.LoadMoreMessage()
    msgs = wx.GetAllMessage
    msgs = msgs[::-1]
    # print(msgs)
    for msg in msgs:
        # 管理员发送的开始信号作为循环结束条件
        if msg[0] == "BotManager" and ("开始" in msg[1] or msg[1] == msg_start):
            break
        elif msg[0] == "SYS" or msg[0] == "BotManager" or ("打卡" not in msg[1]):  # 忽视系统和管理员的发言
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


# 青云客智能聊天机器人
def ai_qingyunke(msg):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % msg
    res = requests.get(url)
    res.raise_for_status()
    answer = res.json()['content'].replace('{br}', '\n')
    return answer

# 思知对话机器人
def ai_sizhi(msg):
    url = 'https://api.ownthink.com/bot?spoken=%s' % msg
    res = requests.get(url)
    res.raise_for_status()
    answer = res.json()['data']['info']['text']
    print(type(answer))
    return answer

# 发送未来几天天气预报
def weather_report():
    msg = ai_qingyunke("杭州天气")
    wx.ChatWith(wechat_group)
    WxUtils.SetClipboard(msg)
    wx.SendClipboard()

# 获取今日天气数据（字符串）
def today_weather():
    msg = ai_qingyunke("杭州天气")
    lt = msg.split('\n')[1].split('：')
    # lt[0] = lt[0].replace('[', '(').replace(']', ')')
    lt[1] = lt[1].replace("低", "最低").replace("高", "最高")
    msg_today = f"                  {lt[0]}\n今日天气：{lt[1]}"
    return msg_today

# 发送笑话
def xiaohua_report():
    msg = ai_qingyunke("笑话").split("提示")[0]
    wx.ChatWith(wechat_group)
    WxUtils.SetClipboard(msg)
    wx.SendClipboard()

# 一言：获取每日一句数据（字符串）
def yiyan():
    url = 'https://v1.hitokoto.cn/?c=f&encode=json'
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    msg = data['hitokoto']
    author = data['from']
    answer = f"每日一句：『{msg}』——{author}"
    return answer



def today_report():
    # 今日天气
    msg_weather = today_weather()
    # 每日一句
    msg_word = yiyan()
    # 历史上的今天

    wx.ChatWith(wechat_group)
    msg = msg_weather + '\n\n' + msg_word
    WxUtils.SetClipboard(msg)
    wx.SendClipboard()


# 监视聊天中有没有出现命令指令，如果出现了，就立刻执行相关指令
def listen_order():
    msgs = wx.GetAllMessage
    # print(msgs)
    for msg in msgs[::-1]:
        info = msg[1]  # ('TTup', '介绍', '4252629441034')
        if "END" in info or info == msg_end:
            break
        elif info == "INTRO":  # 机器人自我介绍
            # wx.SendMsg(self_intro)
            WxUtils.SetClipboard(self_intro)
            wx.SendClipboard()
            wx.SendMsg(msg_end)
        elif info == "FUNC":  # 功能介绍
            # wx.SendMsg(msg_functions)
            WxUtils.SetClipboard(msg_functions)
            wx.SendClipboard()
            wx.SendMsg(msg_end)
        elif info == "NAME":  # 所有人员名单
            true_name_list = wxname2true_name(name_list)
            wx.SendMsg(" ".join(true_name_list))
            wx.SendMsg(msg_end)
        elif info == "RESTART" and msg[0] == 'BotManager':  # 重启机器人
            wx.SendMsg("机器人已重启，请所有人重新上报一次！")
            start_clock_notice()
            wx.SendMsg(msg_end)
        elif info == "NOTICE":  # 手动提醒打卡
            count_unclock()
            wx.SendMsg(msg_end)
        # 以下为附加功能
        elif info == 'tq':  # 天气预报
            weather_report()
            wx.SendMsg(msg_end)
        elif info == 'xh':  # 笑话
            xiaohua_report()
            wx.SendMsg(msg_end)
        elif info == 'dy':  # 电影票房排行榜
            # movie_report()
            wx.SendMsg("https://piaofang.maoyan.com/dashboard")
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
    today_report()

    # 今日天气预报
    # schedule.every().day.at("09:00").do(today_report)
    schedule.every().day.at("04:27").do(today_report)

    # 启动今日打卡提醒
    schedule.every().day.at("10:00").do(start_clock_notice)

    # 打卡提醒
    schedule.every().day.at("11:00").do(clock_notice_count)
    schedule.every().day.at("14:00").do(clock_notice_count)
    schedule.every().day.at("17:45").do(clock_notice_count)
    schedule.every().day.at("23:00").do(clock_notice_count)

    # 每隔一分钟遍历微信群聊天记录，监控是否实现命令关键词
    # schedule.every(1).minutes.do(listen_order)
    # schedule.every(10).seconds.do(listen_order)

    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)



if __name__ == '__main__':
    webot_health_notice()
