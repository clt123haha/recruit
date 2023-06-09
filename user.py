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

from crose import allow_cross_domain
from data_sheet import get_sheet,session,Jobmessage
from data_sheet import User
from sqlalchemy.sql import or_
from tool import check_message


bp = Blueprint("user",__name__,static_folder='/user')

@bp.route("/get_collection")
def get_collection():
    id = request.args.get("id")
    result = session.query(User).filter(User.id == id).first()
    if result is None:
        return {"code":102,"message":"用户不存在"}
    collection = result.collection.split('/')
    data = []
    for c in collection:
        job = session.query(Jobmessage).filter(Jobmessage.id == int(c)).first()
        if job is None:
            continue
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
    if account is None or password is None:
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
    name = request.json.get("name")
    gender = request.json.get("gender")
    age = request.json.get("age")
    place = request.json.get("place")
    degree = request.json.get("degree")
    major = request.json.get("major")
    courses = request.json.get("courses")
    experience = request.json.get("experience")
    intention = request.json.get("intention")
    appraise = request.json.get("appraise")
    phone = request.json.get("phone")
    email = request.json.get("email")
    personal_projects = request.json.get("Personal_projects")
    enterprise_projects = request.json.get("enterprise_projects")
    certificate = request.json.get("certificate")
    skill = request.json.get("skill")
    work_experience = request.json.get("work_experience")
    user = session.query(User).filter(User.id == user_id).first()
    if user == None:
        return {'code': 302, 'message': '账号不存在'}
    save_path = r'E:\recruit\resume'
    if not os.path.exists(save_path):   # 检测目录是否存在，不在则创建
        os.makedirs(save_path)
    try:
        f = open(save_path + '\\' + str(user.id) +".txt",'w')
        f.write("姓名\n")
        f.write(name + '\n')
        f.write("性别\n")
        f.write(gender+'\n')
        f.write("年龄\n")
        f.write(age+ '\n')
        f.write("现居\n")
        f.write(place + '\n')
        f.write("学历\n")
        f.write(degree + '\n')
        f.write("学校专业\n")
        f.write(major + '\n')
        f.write("主修课程\n")
        f.write(courses + '\n')
        f.write("电话\n")
        f.write(phone + '\n')
        f.write("邮箱\n")
        f.write(email + '\n')
        f.write("期望职业\n")
        f.write(intention+'\n')
        f.write("工作经验\n")
        for i in work_experience:
            f.write('#' + i + '\n')
        f.write("技能\n")
        for i in skill:
            f.write('#' + i + '\n')
        f.write("企业项目\n")
        for i in enterprise_projects:
            f.write('#' + i + '\n')
        f.write("个人项目\n")
        for i in personal_projects:
            f.write('#' + i + '\n')
        f.write("荣誉\n")
        for i in certificate:
            f.write('#' + i + '\n')
        f.write("项目经验\n")
        for i in experience:
            f.write('#' + i + '\n')
        f.write("自我评价\n")
        for i in appraise:
            f.write(i+'\n')
    except Exception as e:
        print(e)
        return {"code": 307, "message": "信息储存失败，请稍后再试"}
    return {"code":200,"message":"success"}

@bp.route("/getresume")
def getResume():
    mark = -1
    geren = []
    work_experience = []
    rongyu = []
    xiangmu = []
    ziwo = []
    skill = []
    qiye = []
    string_list = ["姓名","性别","年龄","现居","学历","学校专业","主修课程","电话","邮箱","期望职业","工作经验","技能","企业项目","个人项目","荣誉","项目经验","自我评价"]
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
                name = line[:line.__len__() - 1]
            if mark == 1:
                gender = line[:line.__len__() -1]
            if mark == 2:
                age = line[:line.__len__() -1]
            if mark == 3:
                place = line[:line.__len__() - 1]
            if mark == 4:
                xueli = line[:line.__len__() -1]
            if mark == 5:
                zhaunye = line[:line.__len__() -1]
            if mark == 6:
                zhuxiu = line[:line.__len__() -1]
            if mark == 7:
                phone = line[:line.__len__() -1]
            if mark == 8:
                email = line[:line.__len__() -1]
            if mark == 9:
                intention = line[:line.__len__() -1]
            if mark == 10:
                if line[0] == '#' or work_experience.__len__() == 0:
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    work_experience.append(temp)
                else:
                    temp = work_experience.pop()
                    if line[line.__len__() -1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    work_experience.append(temp)
            if mark == 11:
                if line[0] == '#' or skill.__len__() == 0:
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    skill.append(temp)
                else:
                    temp = skill.pop()
                    if line[line.__len__() -1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    skill.append(temp)
            if mark == 12:
                if line[0] == '#' or qiye.__len__() == 0:
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    qiye.append(temp)
                else:
                    temp = qiye.pop()
                    if line[line.__len__() -1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    qiye.append(temp)
            if mark == 13:
                if line[0] == '#' or geren.__len__() == 0:
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    geren.append(temp)
                else:
                    temp = geren.pop()
                    if line[line.__len__() -1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    geren.append(temp)
            if mark == 14:
                if line[0] == '#' or rongyu.__len__() == 0:
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    rongyu.append(temp)
                else:
                    temp = rongyu.pop()
                    if line[line.__len__() -1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    rongyu.append(temp)
            if mark == 15:
                if line[0] == '#' or xiangmu.__len__() == 0:
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    xiangmu.append(temp)
                else:
                    temp = xiangmu.pop()
                    if line[line.__len__() -1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    xiangmu.append(temp)
            if mark == 16:
                if line[0] == '#' or ziwo.__len__() == 0:
                    temp = line[1:]
                    if temp[temp.__len__() -1] == '\n':
                        temp = temp[:temp.__len__() -1]
                    ziwo.append(temp)
                else:
                    temp = ziwo.pop()
                    if line[line.__len__() -1] == '\n':
                        line = line[:line.__len__() - 1]
                    temp += line
                    ziwo.append(temp)
    except Exception as e:
        print(e)
        return {"code": 308, "message": "信息读取失败，请稍后再试"}
    data = {"姓名":name,"性别":gender,"年龄":age,"现居":place,"学历":xueli,"学校专业":zhaunye,
            "主修课程":zhuxiu,"电话":phone,"邮箱":email,"期望职业":intention,"工作经验":work_experience,"技能":skill,
            "企业项目":qiye,"个人项目":geren,"荣誉":rongyu,"项目经验":xiangmu,"自我评价":ziwo}
    return {"code": 200, "message": "success","resume":data}


