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


bp = Blueprint("job",__name__,static_folder='/job')

@bp.route("/get_postings")
def get():
    title = request.json.get('text').get('title')
    money= request.json.get('text').get('money')
    im = request.json.get('text').get('im')
    place = request.json.get('text').get('place')
    if title is None or money is None or im[0] is None or im[1] is None or place is None:
        return jsonify(dict(code=101,message="招聘信息不全"))
    newJob = Jobmessage(title=title,money=money,im1=im[0],im2=im[1],place=place)
    session.add(newJob)
    session.commit()
    return jsonify(dict(code=200, message="success"))

@bp.route("/return_message")
def get_message():
    query_result = session.query(Jobmessage).all()
    message = []
    try:
        for result in query_result:
           re = {"title":result.title,"money":result.money,"place":result.place,"im":[result.im1,result.im2]}
           message.append(re)
    except Exception as e:
        print(e)
        return jsonify(dict(code=102, message="数据查询失败"))
    return jsonify(dict(code=200, message="success",data=message))