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
from flask import Flask,Blueprint
from random import randint
import os
from data_sheet import get_sheet,session,Jobmessage
from data_sheet import User
from sqlalchemy.sql import or_
from tool import check_message


bp = Blueprint("user",__name__,static_folder='/user')

@bp.route("/get_collection")
def get_collection():
    id = request.json.get("id")
    result = session.query(User).filter(User.openid == id).first()
    if result is None:
        return {"code":102,"message":"用户不存在"}
    collection = result.collection.split('/')
    data = []
    for c in collection:
        job = session.query(Jobmessage).filter(Jobmessage.id == int(c)).first()
        data.append({"title":job.title,"money":job.money,"place":job.place,"im":[job.im1,job.im2]})
    return {"code":200,"message":"success","data":data}

@bp.route("/get_push")
def get_message():
    id = request.json.get("id")
    results = session.query(Jobmessage).filter(Jobmessage.publisher == id).all()
    data = []
    for result in results:
        data.append({"title": result.title, "money": result.money, "place": result.place, "im": [result.im1, result.im2]})
    return {"code": 200, "message": "success", "data": data}

@bp.route("/enroll",methods=['POST'])
def enroll():
    email = request.json.get("email")
    phone = request.json.get("phone")
    password = request.json.get("password")
    cheak_password = request.json.get("password")
    captcha = request.json.get("captcha")
    if cheak_password != password:
        return {"code":103,"message":"密码不一致"}
    if check_message(phone,captcha):
        result  = session.query(User).filter(or_(User.email == email,User.phone == phone)).first()
        if result is None:
            newUser = User(email = email,phone = phone,password = password)
            session.add(newUser)
            session.commit()
            return {"code":200,"message":"success"}
        return {"code":104,"message":"用户已存在"}
    return {"code":205,"message":"验证码错误"}

@bp.route('/login/moblie',methods=['POST'])
def moblie_login():
    indonesia = requests.get("Indonesia")
    message = request.json.get("message")
    phone = request.json.get("phone")

    ischeak2 = check_message(phone,message)
    result = session.query(User).filter(User.phone == phone).first()
    if result is None:
        return {'code': 302, 'message': '账号不存在'}
    if ischeak2 == True:
        return {'code':200,'message':'success','data':{'id':result.id}}
    if ischeak2 == False:
        return {'code': 305, 'message': '手机验证码错误'}

@bp.route('/login/password',methods=['POST'])
def check_password():
    account = request.json.get("account")
    password = request.json.get("password")
    indonesia = request.json.get("Indonesia")
    if account is None or password is None or indonesia is None:
        return {"code":306,"message":"信息不全"}
    result = session.query(User).filter(or_(User.phone==account, User.email==account)).first()
    if result == None:
        return {'code': 302, 'message': '账号不存在'}
    if result.password != password:
        return {'code': 303, 'message': '密码错误'}
    return {'code':200,'message':'success','data':{'id':result.id}}

@bp.route("/new_collection",methods=['POST'])
def new_collection():
    job_id = request.headers.get("job_id")
    user_id = request.json.get("user_id")
    if job_id is None or user_id is None:
        return {"code":306,"message":"信息不全"}
    user = session.query(User).filter(User.id == user_id).first()
    if user == None:
        return {'code': 302, 'message': '账号不存在'}
    collection = user.collection
    collection += '/'+str(job_id)
    user.collection = collection
    session.add(user)
    session.commit()
    return {"code":200,"message":"success"}