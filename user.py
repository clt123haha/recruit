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

@bp.route("/newcollection",methods=['POST'])
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

@bp.route("/putresume",methods=["POST"])
def putResume():
    user_id = request.json.get("user_id")
    gender = request.json.get("gender")
    intention = request.json.get("intention")
    appraise = request.json.get("appraise")
    educational_background = request.json.get("educational_background")
    work_experience = request.json.get("work_experience")
    school_experience = request.json.get("school_experience")
    certificate = request.json.get("certificate")
    skill = request.json.get("skill")
    if gender is None or school_experience is None or intention is None or appraise is None or educational_background is None or work_experience is None or certificate is None or skill is None:
        {"code": 306, "message": "信息不全"}
    user = session.query(User).filter(User.id == user_id).first()
    if user == None:
        return {'code': 302, 'message': '账号不存在'}
    save_path = r'E:\recruit\resume'
    if not os.path.exists(save_path):   # 检测目录是否存在，不在则创建
        os.makedirs(save_path)
    try:
        f = open(save_path + '\\' + str(user.id) +".txt",'w')
        f.write("性别\n")
        f.write(gender+'\n')
        f.write("求职意向\n")
        f.write(intention+'\n')
        f.write("自我评价\n")
        for i in appraise:
            f.write(intention+'\n')
        f.write("教育背景\n")
        for i in educational_background:
            f.write('#' + i + '\n')
        f.write("工作经历\n")
        for i in work_experience:
             f.write('#' + i + '\n')
        f.write("在校经历\n")
        for i in school_experience:
            f.write('#' + i + '\n')
        f.write("资格证书\n")
        for i in certificate:
            f.write('#' + i + '\n')
        f.write("职业技能\n")
        for i in skill:
            f.write('#' + i + '\n')
    except Exception as e:
        print(e)
        return {"code": 307, "message": "信息储存失败，请稍后再试"}
    return {"code":200,"message":"success"}

@bp.route("/getresume")
def getResume():
    mark = -1
    data = []
    appraise= []
    educational_background = []
    work_experience = []
    school_experience = []
    certificate = []
    skill = []
    string_list = ["性别","求职意向","自我评价","教育背景","工作经历","在校经历","资格证书","职业技能"]
    user_id = request.json.get("user_id")
    user = session.query(User).filter(User.id == user_id).first()
    if user == None:
        return {'code': 302, 'message': '账号不存在'}
    file_path = r'E:\recruit\resume' + '\\' + str(user_id) +".txt"
    if not os.path.exists(file_path):   # 检测目录是否存在，不在则创建
        return {'code': 302, 'message': '简历不存在'}
    try:
        f = open(file_path, 'r')
        for line in f:
            if line[:line.__len__()-1] in string_list:
                mark = string_list.index(line[:line.__len__()-1])
                continue
            if mark == 0:
                gender = line[1:line.__len__() -1]
            if mark == 1:
                intention = line[1:line.__len__() -1]
            if mark == 2:
                if line[0] == '#':
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    appraise.append(temp)
                else:
                    temp = appraise.pop()
                    if line[line.__len__() -1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    appraise.append(temp)
            if mark == 3:
                if line[0] == '#':
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    educational_background.append(temp)
                else:
                    temp = educational_background.pop()
                    if line[line.__len__() - 1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    educational_background.append(temp)
            if mark == 4:
                if line[0] == '#':
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    work_experience.append(temp)
                else:
                    temp = work_experience.pop()
                    if line[line.__len__() - 1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    work_experience.append(temp)
            if mark == 5:
                if line[0] == '#':
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    school_experience.append(temp)
                else:
                    temp = school_experience.pop()
                    if line[line.__len__() - 1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    school_experience.append(temp)
            if mark == 6:
                if line[0] == '#':
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    certificate.append(temp)
                else:
                    temp = certificate.pop()
                    if line[line.__len__() - 1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    certificate.append(temp)
            if mark == 7:
                if line[0] == '#':
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    skill.append(temp)
                else:
                    temp = skill.pop()
                    if line[line.__len__() - 1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    skill.append(temp)
    except Exception as e:
        print(e)
        return {"code": 308, "message": "信息读取失败，请稍后再试"}
    data = {"性别":gender,"求职意向":intention,"自我评价":appraise,"教育背景":educational_background,"工作经历":work_experience,"在校经历":school_experience,"资格证书":certificate,"职业技能":skill}
    return {"code": 200, "message": "success","resume":data}

