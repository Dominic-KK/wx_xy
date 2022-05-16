from __future__ import unicode_literals

import datetime
import json

import requests
from wxpy import *

# 从缓存中获取登录信息，刚登陆过，无需一直登陆
bot = Bot(cache_path=True)

def get_list():
    username = "xxxxx"  # 修改1：手机号
    password = "xxxxx"  # 修改2：密码
    Referer = "xxxxx"  # 修改3：抓包获取
    User_Agent = "xxxxx"  # 修改4：抓包获取
    # 最下面还有两处需要修改哦

    header = {
        "Host": "student.wozaixiaoyuan.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-us,en",
        "Connection": "keep-alive",
        "User-Agent": str(User_Agent),
        "Referer": str(Referer),
        "Content-Length": "360",
    }
    loginUrl = "http://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
    data = "{}"
    session = requests.session()
    url = loginUrl + "?username=" + username + "&password=" + password
    respt = session.post(url, data=data, headers=header)
    res = json.loads(respt.text)
    if res["code"] == 0:
        print("登录成功.")
        jwsession = respt.headers['JWSESSION']

    else:
        print(res['message'])

    api = "https://student.wozaixiaoyuan.com/health/getHealthUsers.json"    # 健康打卡
    headers = {
        "Host": "student.wozaixiaoyuan.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": str(User_Agent),
        "Referer": str(Referer),
        "Content-Length": "360",
        "JWSESSION": str(jwsession),
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
        my_group = bot.groups().search(u'备忘录')[0]  # 修改5：想要发送的群名称，建议先用自己的工具群做测试
        my_group.send(char)
        print("发送成功")
    except:
        my_friend = bot.friends().search('xxxxx')[0]    # 修改6：自己的微信昵称，用于提示报错
        my_friend.send(u'Faild')
        print("发送失败")

if __name__ == "__main__":
    send_news_group()