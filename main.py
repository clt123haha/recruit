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
from job import bp as job_bp
from user import bp as user_bp
from tool import bp as tool_bp


app = Flask(__name__)
app.register_blueprint(job_bp,url_prefix='/job')
app.register_blueprint(user_bp,url_prefix='/user')
app.register_blueprint(tool_bp,url_prefix='/tool')

if __name__ == '__main__':
    get_sheet()
    app.run(host='0.0.0.0', debug=True)
