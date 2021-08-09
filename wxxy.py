from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests
import datetime

# 从缓存中获取登录信息，刚登陆过，无需一直登陆
bot = Bot(cache_path=True)

def get_list():
    api = "https://student.wozaixiaoyuan.com/health/getHealthUsers.json"
    headers = {
        "Host": "student.wozaixiaoyuan.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",  # 修改5：User-Agent
        "Referer": "https://servicewechat.com/wxce6d08f781975d91/177/page-frame.html",  # 修改6：Referer
        "Content-Length": "360",
        "JWSESSION": "d95278f0ddf14b8f9bf31f4742d1282f",  # 修改7：JWSESSION
    }
    datenow = datetime.date.today()
    dateformat = datenow.strftime('%Y%m%d')
    data = {
        "type":"0",
        "date":dateformat
    }
    res = requests.post(api, headers=headers, data=data).json() #提交
    my_list = res['data']
    my_dic = {}
    for i in range(len(my_list)):
        name = my_list[i]['name']
        phone = my_list[i]['phone']
        my_dic[name] = phone

    temp = str(my_dic)
    chars = "{}':"
    for c in chars:
        temp = temp.replace(c,'')

    my_str = temp.replace(',','\n')
    if not my_str:
        title = ""
        zone = "健康打卡全部完成"
    else:
        title = "   姓名    电话\n "
        zone = "尽快打卡"

    print(my_str,zone)
    timenow = datetime.datetime.now().strftime('%m-%d %H:%M')
    char = title + my_str + "\n" + timenow +zone
    return char

def send_news_group():
    char = get_list()
    try:
        my_group = bot.groups().search(u'Test')[0]
        my_group.send(char)
        print("发送成功")
    except:
        my_friend = bot.friends().search('Dominic.')[0]
        my_friend.send(u'Faild')
        print("发送失败")

if __name__ == "__main__":
    send_news_group()
