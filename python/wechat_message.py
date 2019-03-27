# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from wxpy import *
import requests
from threading import Timer
import datetime
import random
import time

# bot = Bot()
# linux执行登陆请调用下面的这句
bot = Bot(console_qr = 2, cache_path="botoo.pkl")
def get_news():

    """获取金山词霸每日一句，英文和翻译"""
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content, note

def send_news():
    try:
        contents = get_news()
        # 你朋友的微信名称，不是备注，也不是微信帐号。
        my_friend = bot.friends().search('Michael Zhang')[0]
        my_friend.send(contents[0])
        my_friend.send(contents[1])
        my_friend.send(u'心若向阳，微笑向暖！愿我们都可以勇敢且温柔，有爱可寻亦有梦可追。早安！')
        # 每86400秒（1天），发送1次
        t = Timer(10, send_news)
        # ran_int = random.randint(0,100)
        # t = Timer(86400+ran_int,send_news)

        t.start()
    except:
        # 你的微信名称，不是微信帐号。
        my_friend = bot.friends().search(u'张继')[0]
        my_friend.send(u"今天消息发送失败了")

def getDateByTimeStamp(time_stamp):
    timeArray = time.localtime(time_stamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def task():
    try:
        contents = get_news()
        my_friend = bot.friends().search('Grace')[0]
        my_friend.send(contents[0])
        my_friend.send(contents[1])
        my_friend.send(u'出门的时候记得反馈一下今天的天气怎么样(づ｡◕‿‿◕｡)づ')
    except:
        my_friend = bot.friends().search(u'张继')[0]
        my_friend.send(u"今天消息发送失败了")

def regular_task(sched_timer):
    while True:
        now = int(time.time())
        if now == sched_timer:
            task()
            print(u'当前:' + getDateByTimeStamp(now) + u' 计划:' + getDateByTimeStamp(sched_timer))
            sched_timer = sched_timer + 86400
            time.sleep(86300);
        elif now > sched_timer:
            print(u'当前:' + getDateByTimeStamp(now) + u' 计划:' + getDateByTimeStamp(sched_timer))
            sched_timer = sched_timer + 86400
            print(u'下次执行时间:' + getDateByTimeStamp(otherStyleTime))

if __name__ == "__main__":
    # dt = '2018-03-21 06:00:00'
    dt = '2019-03-21 06:00:00'
    sched_timer = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
    regular_task(sched_timer)
    # send_news()
