import sys
import os
import hashlib
import hmac
import base64
import requests
import json
import time
import configparser
from flask import Blueprint, request, jsonify
from models import user_table, db

config = configparser.ConfigParser()
config.read('/usr/src/app/config.ini')
service_id = config['naver']['service_id']
access_key = config['naver']['access_key']
secret_key = config['naver']['secret_key']
secret_key = bytes(secret_key, 'UTF-8')

blue_signup = Blueprint("signup", __name__, url_prefix="/signup")

@blue_signup.route("/", methods=["POST"])
def signup():
    if(request.method == "POST"):
        name = request.form.get("name","")
        phoneNum = request.form.get("phoneNum","")
        address = request.form.get("address","")
        carNum = request.form.get("carNum","")
        id = request.form.get("id","")
        pw = request.form.get("pw","")
        agreeCheck = bool(request.form.get("agreeCheck",""))
        
        if(name != "" or phoneNum != "" or address != "" or carNum != "" or id != "" or pw != "" or agreeCheck != ""):
            try:
                new_user = user_table(id=id, pw=pw, name=name, phone=phoneNum, car_num=carNum, address=address, check_num=None, info_agree=agreeCheck, info_gps=False)

                db.session.add(new_user)
                db.session.commit()
                return jsonify({'result':True})
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})


@blue_signup.route("/id", methods=["POST"])
def id():
    if(request.method == "POST"):
        id = request.form.get("id","")
        
        if(id != ""):
            user = user_table.query.filter(user_table.id==id).first()
            if(user == None):
                return jsonify({'result':True})
            else:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})
        
        
def	make_signature(timestamp, uri):
    method = "POST"
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')

    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

@blue_signup.route("/num", methods=["POST"])
def num():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            timestamp = int(time.time() * 1000)
            timestamp = str(timestamp)

            url = "https://sens.apigw.ntruss.com"
            uri = f"/sms/v2/services/{service_id}/messages"
            
            messages = {
                "subject":"test",
                "content":"test",
                "to":"01092337395"
                }
            body = {
                "type":"SMS",
                "countryCode":"82",
                "contentType":"COMM",
                "from":"01098381417",
                "content":"Test",
                "message":[messages]
            }
            body = json.dumps(body)
            headers = {
                'Content-Type':'application/json; charset=utf-8',
                'x-ncp-apigw-timestamp':timestamp,
                'x-ncp-iam-access-key':access_key,
                'x-ncp-apigw-signature-v2':make_signature(timestamp, uri)
            }
            
            res = requests.post(url+uri, headers=headers, data=body)
            print(res.content)
            return "test"
    else:
        return jsonify({'result':'error'})