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


bp = Blueprint("user",__name__,static_folder='/user')

@bp.route("/get_collection")
def get_collection():
    openid = request.json.get("openid")
    result = session.query(User).filter(User.openid == openid).first()
    if result is None:
        return {"code":102,"message":"用户不存在"}
    collection = result.collection.split('/')
    data = []
    for c in collection:
        job = session.query(Jobmessage).filter(Jobmessage.id == int(c)).first()
        data.append({"title":job.title,"money":job.money,"place":job.place,"im":[job.im1,job.im2]})
    return {"code":200,"message":"success","data":data}
