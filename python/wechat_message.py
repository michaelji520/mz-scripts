# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from wxpy import *
import requests
from threading import Timer
import datetime
import random
import time
import urllib, json

# bot = Bot()
# linux执行登陆请调用下面的这句

# 天气现象映射
SKYCON_DICT = {
    'CLEAR_DAY': u'晴(白天)',
    'CLEAR_NIGHT': u'晴(夜间)',
    'PARTLY_CLOUDY_DAY': u'多云(白天)',
    'PARTLY_CLOUDY_NIGHT': u'多云(夜间)',
    'CLOUDY': u'阴',
    'WIND': u'大风',
    'HAZE': u'雾霾',
    'RAIN': u'雨',
    'SNOW': u'雪'
}

bot = Bot(console_qr = 2)
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

def getWeather():
    api_url = 'https://api.caiyunapp.com/v2/TAkhjf8d1nlSlspN/116.297006,40.043227/daily.json'
    try:
        response = urllib.request.urlopen(api_url)
        weather = json.loads(response.read().decode('utf-8'))
        if weather['status'] and weather['status'] == 'ok':
            today = weather['result']['daily']
            weather_str = ''
            temperature = today['temperature']
            weather_str += (u'今日气温: %s-%s℃; ' %(temperature[0]['min'], temperature[0]['max']))
            comfort = today['comfort']
            weather_str += (u'舒适指数: %s; ' %(comfort[0]['desc']))
            cold_risk = today['coldRisk']
            weather_str += (u'感冒指数: %s; ' %(cold_risk[0]['desc']))
            wind_speed = today['wind'][0]
            weather_str += (u'风速: %s-%s(m/s); ' %(wind_speed['min']['speed'], wind_speed['max']['speed']))
            humidity = today['humidity'][0]
            weather_str += (u'相对湿度: %s%%-%s%%; ' %(humidity['min'], humidity['max']))
            ultraviolet = today['ultraviolet'][0]
            weather_str += (u'紫外线指数: %s; ' %(ultraviolet['desc']))
            pm25 = today['pm25'][0]
            weather_str += (u'PM2.5: %s-%s; ' %(pm25['min'], pm25['max']))
            skycon = today['skycon'][0]
            weather_str += (u'天气状况: %s; ' %(SKYCON_DICT[skycon['value']]))
            return weather_str
    except:
        return u'o(╯□╰)o今天收到宇宙射线影响, 木有拿到天气数据!'

def task():
    try:
        contents = get_news()
        my_friend = bot.friends().search('Grace')[0]
        my_friend.send(contents[0])
        my_friend.send(contents[1])
        weather_info = getWeather()
        my_friend.send(weather_info)
        my_friend.send(u'Good Morning! (づ｡◕‿‿◕｡)づ')
    except:
        # 你的微信名称，不是微信帐号。
        my_friend = bot.friends().search(u'张继')[0]
        my_friend.send(u"今天消息发送失败了")

def regular_task(sched_timer):
    while True:
        now = int(time.time())
        if now == sched_timer:
            task()
            sched_timer = sched_timer + 86400
            print(u'本次任务执行时间:' + getDateByTimeStamp(now))
            time.sleep(86300);
        elif now > sched_timer:
            while now > sched_timer:
                sched_timer = sched_timer + 86400
            print(u'\n下次执行时间:' + getDateByTimeStamp(sched_timer))

if __name__ == "__main__":
    # dt = '2018-03-21 06:00:00'
    dt = '2019-03-21 06:00:00'
    sched_timer = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
    regular_task(sched_timer)
    # send_news()
