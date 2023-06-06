import base64
import random
import time
import urllib.parse
import urllib.request
from io import BytesIO

from flask_socketio import SocketIO, emit
from flask import send_from_directory, make_response
from flask import Flask, request, jsonify,Blueprint,send_file
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import Flask,Blueprint
from random import randint
import os
from tool import append

from flask_cors import CORS
from data_sheet import  User

from data_sheet import get_sheet,session,Jobmessage
from job import bp as job_bp
from user import bp as user_bp
from tool import bp as tool_bp
from chat import  bp as chat_bp


app = Flask(__name__)
app.register_blueprint(job_bp,url_prefix='/job')
app.register_blueprint(user_bp,url_prefix='/user')
app.register_blueprint(tool_bp,url_prefix='/tool')
app.register_blueprint(chat_bp,url_prefix='/chat')
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

@socketio.on('connect')
def test_connect(data):
    sid = data["socketid"]
    id = data["userid"]
    user = session.query(User).filter(User.id == id).first()
    user.sid = sid
    session.add(user)
    session.commit()
    emit('connect response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('getmessage')
def getmessage(data):
    id1 = request.json.get("userid")
    id2 = request.json.get("talkto")
    message = data["message"]
    sid = session.query(User).filter(User.id == id1).first().sid
    emit("getmeaasge", message, room=sid)
    append(id2, id1, message)
    append(id1, id1, message)


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    get_sheet()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)