# coding: utf-8
import json

import pymongo
import requests
from flask import Flask
from flask import request, Response

from modules.res_html.liepin import resume_liepin
from modules.res_html.linkin import resume_linkin
from modules.res_html.zhilian import resume_zhilian
from modules.res_html.qianchengwuyou import resume_51job

s = requests.session()

app = Flask(__name__)
db = pymongo.MongoClient('127.0.0.1:27017')['test']

@app.route('/resume', methods=['POST'])
def resume_api():
    accessToken = request.headers.get('Authorization')[7:]
    name = request.json.get('name')
    password = request.json.get('password')
    web_name = request.json.get('web_name')
    customerId = request.json.get('customerId')
    url = request.json.get('url')
    cookie = request.json.get('cookie')
    flag = request.json.get('flag')

    if web_name == "51job":
        response = resume_51job(db, name, password, customerId, accessToken, flag)
        return response
    elif web_name == "zhilian":
        response = resume_zhilian(db, name, password, customerId, accessToken, flag)
        return response
    elif web_name == "liepin":
        response = resume_liepin(db, name, password, customerId, accessToken, flag)
        return response
    elif web_name == "linkin":
        response = resume_linkin(db, name, password, customerId, accessToken, flag, url, cookie)
        return response
    else:
        return new_response_error()
def new_response_error():
    data = {}
    data = json.dumps({
        'code': 404,
        'message': "not found",
        'data': data
    })
    return Response(
            response=data,
            status=200,
            mimetype="application/json")        