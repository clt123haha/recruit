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

from flask_cors import cross_origin

from data_sheet import get_sheet,session,Jobmessage
from crose import allow_cross_domain

bp = Blueprint("job",__name__,static_folder='/job')

@bp.route("/put_postings",methods=["POST"])

def get():
    title = request.json.get('text').get('title')
    money= request.json.get('text').get('money')
    im = request.json.get('text').get('im')
    place = request.json.get('text').get('place')
    name = request.json.get("name")
    work = request.json.get("work")
    time = request.json.get("time")
    number = request.json.get("number")
    company = request.json.get("company")
    detail = request.json.get("detail")
    need = request.json.get("need")
    well = request.json.get("well")
    if title is None or money is None or im[0] is None or im[1] is None or place is None:
        return jsonify(dict(code=101,message="招聘信息不全"))
    newJob = Jobmessage(title=title,money=money,im1=im[0],im2=im[1],place=place,name=name,work=work,time=time,number=number,company=company)
    session.add(newJob)
    session.commit()
    id = session.query(Jobmessage).count()
    save_path = r'E:\recruit\job'
    if not os.path.exists(save_path):  # 检测目录是否存在，不在则创建
        os.makedirs(save_path)
    try:
        f = open(save_path + '\\' + str(id) + ".txt", 'w')
        f.write("detail\n")
        f.write(detail + '\n')
        f.write("need\n")
        f.write(need + '\n')
        f.write("well\n")
        f.write(well + '\n')
    except Exception as e:
        return jsonify(dict(code=102, message="存储信息失败"))
    return jsonify(dict(code=200, message="success"))

@bp.route("/return_message")
@allow_cross_domain
def get_message():
    data = []
    string_list = ["detail","need","well"]
    jobList = session.query(Jobmessage).all()
    for job in jobList:
        id = job.id
        title = job.title
        money = job.money
        im = [job.im1,job.im2]
        place = job.place
        name = job.name
        work = job.work
        time = job.time
        number = job.number
        company = job.company
        detail = ""
        well = ""
        need = ""
        file_path = r'E:\recruit\job' + '\\' + str(id) + ".txt"
        if not os.path.exists(file_path):  # 检测目录是否存在，不在则创建
            return {'code': 302, 'message': '简历不存在'}
        try:
            f = open(file_path, 'r')
            for line in f:
                if line[:line.__len__() - 1] in string_list:
                    mark = string_list.index(line[:line.__len__() - 1])
                    continue
                if mark == 0:
                    detail += line
                if mark == 1:
                    need += line
                if mark == 2:
                    well += well
        except Exception as e:
            return {"code": 308, "message": "信息读取失败，请稍后再试"}
        data.append({"id":id,
                     "title":title,
                     "money":money,
                     "im":im,
                     "place":place,
                     "name":name,
                     "work":work,
                     "time":time,
                     "number":number,
                     "company":company,
                     "detail":detail[:detail.__len__()-1],
                     "need":need[:need.__len__()-1],
                     "well":well[:well.__len__()-1]
                     })
    return {"data":data,
            "code":200}
    try:
        for result in query_result:
           re = {"title":result.title,"money":result.money,"place":result.place,"im":[result.im1,result.im2]}
           message.append(re)
    except Exception as e:
        print(e)
        return jsonify(dict(code=102, message="数据查询失败"))
    return jsonify(dict(code=200, message="success",data=message))
