from __future__ import unicode_literals

import datetime

import requests
from wxpy import *

# 从缓存中获取登录信息，刚登陆过，无需一直登陆
bot = Bot(cache_path=True)

def get_list():
    api = "https://student.wozaixiaoyuan.com/health/getHealthUsers.json"    # 健康打卡
    headers = {
        "Host": "student.wozaixiaoyuan.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": "xxxxx",  # 修改1：User-Agent
        "Referer": "xxxxx",  # 修改2：Referer
        "Content-Length": "360",
        "JWSESSION": "xxxxx",  # 修改3：JWSESSION   最下面还有两次需要修改哦
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
        my_group = bot.groups().search(u'xxxxx')[0]  # 修改4：想要发送的群名称，建议先用自己的工具群做测试
        my_group.send(char)
        print("发送成功")
    except:
        my_friend = bot.friends().search('xxxxx')[0]    # 修改5：自己的微信昵称，用于提示报错
        my_friend.send(u'Faild')
        print("发送失败")

if __name__ == "__main__":
    send_news_group()