import requests
from flask import Blueprint, request, session, jsonify
from sqlalchemy import or_

from crose import allow_cross_domain
from data_sheet import User
import base64
import random
import time
import urllib.parse
import urllib.request
from io import BytesIO
from flask import send_from_directory, make_response
from flask import Flask, request, jsonify,Blueprint,send_file
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import Flask
from random import randint
import os
from data_sheet import get_sheet,session,User,ShortMessage
import requests
import json
import datetime

bp = Blueprint("tool", __name__, url_prefix="/tool")



def check_message(phone,indonesia):   # 退出程序的时候一定要记得删除验证码，否则内存占用会越来越大
    result = session.query(ShortMessage).filter(ShortMessage.phonenumber==phone).first()
    t = time.time()
    second = time.time() - float(result.time)
    m, s = divmod(second, 60)

    if m >= 10:
        return False
    if indonesia == result.meaasge:
        return  True
    return False

def short_message(mobile):
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
    str = generate_random_str()
    # 定义请求的数据
    values = {
        'account': 'C99499604',  # 用户名
        'password': 'f8306695d35f13813318e04e6a2c4349',
        'mobile': mobile,  # 要发送的号码
        'content': '您的验证码是{}，十分钟内有效，请不要泄露给他人。'.format(str),  # 发送的
        'format': 'json',  # 格式类型
    }

    # 将数据进行编码
    data = urllib.parse.urlencode(values).encode(encoding='UTF8')

    # 发起请求
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    return str

#用于获取验证码的接口

#手机验证码的字符串
def generate_random_str():
  random_str =''
  base_str ='0123456789'
  for i in range(6):
    random_str +=base_str[random.randint(0, len(base_str)-1)]
  return random_str



@bp.route('/mobile_text')
@allow_cross_domain
def test():
    phone = request.json.get("phone")
    if phone is None:
        return {'code':201,'message':'请输入手机号码'}
    try:
         indonesia = short_message(phone)
    except Exception as e:
        print(e)
        return {'code':202,'meaasge':'发送失败，请稍后再试'}
    try:
        result = session.query(ShortMessage).filter(ShortMessage.phonenumber == phone).first()
        if result is None:
            newMessage = ShortMessage(phonenumber=phone,meaasge=indonesia,time=str(time.time()))
            session.add(newMessage)
            session.commit()
        else:
            result.meaasge = indonesia
            result.time = str(time.time())
            session.add(result)
            session.commit()
    except Exception as e:
        session.rollback()
        return {'code':203,'message':'验证码无效'}
    return  {'code':200,'message':'success'}