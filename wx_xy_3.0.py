from __future__ import unicode_literals

import datetime
import json
from time import strftime
import requests
import pyautogui
import pyperclip
import time


# 从缓存中获取登录信息，刚登陆过，无需一直登陆
name="xxx"#需要发给谁（可以填写名字）
def get_list():
    username = "xxx"  # 修改1：手机号
    password = "xxx"  # 修改2：密码
    
    Referer = "https://gw.wozaixiaoyuan.com/h5/mobile/basicinfo/index/login/index"  # 修改3：抓包获取
    User_Agent = "User-Agent: Mozilla/5.0 (Linux; Android 11; V2055A Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4277 MMWEBSDK/20220706 Mobile Safari/537.36 MMWEBID/815 MicroMessenger/8.0.25.2200(0x2800193B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxce6d08f781975d91"  # 修改4：抓包获取
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


    time=strftime("%Y%m%d")
    # api = "https://student.wozaixiaoyuan.com/health/getHealthUsers.json"    # 健康打卡
    api="http://gw.wozaixiaoyuan.com/health/mobile/manage/getUsers?date="+str(time)+"&batch=1300001&page=1&size=20&state=1&keyword=&type=0"
    headers = {
        "Host": "gw.wozaixiaoyuan.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '''"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"''',
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "JWSESSION": str(jwsession),
        "sec-ch-ua-mobile": "?1",
        "User-Agent": str(jwsession),
        "sec-ch-ua-platform": "Android",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://gw.wozaixiaoyuan.com/h5/mobile/health/0.3.7/manage/users?date=20230105&batch=1300001&state=-1&type=0",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": "JWSESSION="+str(jwsession)+"; JWSESSION="+str(jwsession),
    }
    res2=requests.get(url=api,headers=headers)
    res2=eval(res2.text)
    my_list = res2['data']
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
        zone = "\n尽快打卡"

    print(my_str,zone)
    timenow = datetime.datetime.now().strftime('%m-%d %H:%M')
    char = title + my_str + "\n" + timenow +zone
    return char
    

def send(msg):
    pyperclip.copy(msg)             # 复制需要发送的内容到粘贴板
    pyautogui.hotkey('ctrl', 'v')   # 模拟键盘 ctrl + v 粘贴内容
    pyautogui.press('enter')        # 发送消息

def send_msg(friend):
    pyautogui.hotkey('ctrl', 'alt', 'w')    # Ctrl + alt + w 打开微信
    pyautogui.hotkey('ctrl', 'f')           # 搜索好友
    pyperclip.copy(friend)                  # 复制好友昵称到粘贴板
    pyautogui.hotkey('ctrl', 'v')           # 模拟键盘 ctrl + v 粘贴
    time.sleep(1)
    pyautogui.press('enter')                # 回车进入好友消息界面
    send(get_list())
    
    
    
if __name__ == "__main__":
    friend_name = str(name)		
    send_msg(friend_name)