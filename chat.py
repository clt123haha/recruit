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

from flask_socketio import emit

from crose import allow_cross_domain
from data_sheet import get_sheet,session,Jobmessage
from data_sheet import User
from sqlalchemy.sql import or_
from tool import check_message,append


bp = Blueprint("chat",__name__,static_folder='/chat')

@bp.route('/sendmessage')
def sendmessage():
    id1 = request.json.get("userid")
    id2 = request.json.get("talkto")
    message = request.json.get("message")
    sid = session.query(User).filter(User.id == id2).first().sid
    emit("sendmeaasge",message,room = sid)
    append(id2,id1,message)
    append(id1, id1, message)
