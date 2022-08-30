# -*- codeing = utf-8 -*-
import random
from time import time, localtime
from requests import get, post
from datetime import datetime, date
import sys
import os
import io
import bs4
import requests
import json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
 
def get_color():
    # 往list中填喜欢的颜色即可
    color_list = ['#6495ED','#3CB371']
 
    return random.choice(color_list)
 
 
def get_access_token():
    # appId 
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause") 
        sys.exit(1)
    # print(access_token)
    return access_token
 
def get_weathers():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' }
    key = config['weather_key']
    region=config['region']
    region_url = 'https://geoapi.qweather.com/v2/city/lookup?location={}&key={}'.format(region, key)
    response = get(region_url, headers=header).json()
    if response['code'] == '404':
        os.system('pause')
        sys.exit(1)
    elif response['code'] == '401':
        os.system('pause')
        sys.exit(1)
    else:
        location_id = response['location'][0]['id']
    weather_url = 'https://devapi.qweather.com/v7/weather/now?location={}&key={}'.format(location_id, key)
    response = get(weather_url, headers=header).json()
    weather = response['now']['text']
    temp = response['now']['temp'] + '\xc2\xb0' + 'C'
    wind_dir = response['now']['windDir']
    url = 'https://devapi.qweather.com/v7/weather/3d?location={}&key={}'.format(location_id, key)
    response = get(url, headers=header).json()
    max_temp = response['daily'][0]['tempMax'] + '\xc2\xb0' + 'C'
    min_temp = response['daily'][0]['tempMin'] + '\xc2\xb0' + 'C'
    sunrise = response['daily'][0]['sunrise']
    sunset = response['daily'][0]['sunset']
    url = 'https://devapi.qweather.com/v7/air/now?location={}&key={}'.format(location_id, key)
    response = get(url, headers=header).json()
    if response['code'] == '200':
        category = response['now']['category']
        pm2p5 = response['now']['pm2p5']
    else:
        category = ''
        pm2p5 = ''
    id = random.randint(1, 16)
    url = 'https://devapi.qweather.com/v7/indices/1d?location={}&key={}&type={}'.format(location_id, key, id)
    response = get(url, headers=header).json()
    proposal = ''
    if response['code'] == '200':
        proposal += response['daily'][0]['text']
    return weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal,region


def get_birthday(birthday, year, today):
    # 获取生日的月和日
    birthday_month = int(birthday.split("-")[1])
    birthday_day = int(birthday.split("-")[2])
    # 今年生日
    year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day
 
def get_daily_love(): 
    
    url = "http://api.tianapi.com/caihongpi/index?key=f841d49aefd15af36eb082296b5aab9f"
    r = requests.get(url)
    content = r.json()
    name = content['newslist'][0]
    daily_love ="{}".format(name['content'])
    return daily_love
    
def get_tianhang():
    url = 'http://api.tianapi.com/zaoan/index?key=f841d49aefd15af36eb082296b5aab9f'
 
# requests 方法
   
    res = requests.get(url)
    content = res.json()
    print(content)
    name = content['newslist'][0]
    print("{}".format(name['content'])) 
    tianhang_name="{}".format(name['content'])
    return tianhang_name 
    
def send_message(weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal,user,accessToken, region,daily_love):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(accessToken)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
             "weather": {
                "value": weather,
                "color": get_color()
            },
             "temp": {
                "value": temp,
                "color": get_color()
            },
             "max_temp": {
                "value": max_temp,
                "color": get_color()
            },
             "min_temp": {
                "value": min_temp,
                "color": get_color()
            },
             "wind_dir": {
                "value": wind_dir,
                "color": get_color()
            },
             "sunrise": {
                "value": sunrise,
                "color": get_color()
            },
             "sunset": {
                "value": sunset,
                "color": get_color()
            },
             "proposal": {
                "value": proposal,
                "color": get_color()
            },
             "pm2p5": {
                "value": pm2p5,
                "color": get_color()
            },
             "category": {
                "value": category,
                "color": get_color()
            },
            "region": {
                "value": region,
                "color": get_color()
            },
            "daily_love": {
                "value": daily_love,
                "color": get_color()
            },
            "birthday": { 
                "value": birthdays,
                "color": get_color()
            },
            
            "love_day": {
                "value": love_days,
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value, year, today)
        # 将生日数据插入data
        data["data"][key] = {"value": birth_day, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)
 
 
if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)
 
    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入省份和市获取天气信息
    tianhang_name=get_tianhang();
    weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal,region=get_weathers();
    
    # 获取每日情话
    daily_love = get_daily_love()
    #获取每日一句英语 
    
    # 公众号推送消息
    for user in users:
        send_message(weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal,user,accessToken, region,daily_love)
    os.system("pause")
