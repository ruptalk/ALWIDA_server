import os
import random
import time
import datetime
import base64
import hmac
import hashlib
import requests
from flask import Flask, request, render_template, session, url_for, jsonify, make_response
from sqlalchemy import func, inspect
from models import admin_table, user_table, terminal_table, container_table, reservation_table, receipt_table, cash_table, check_table, chatting_table, message_table, init_db

db = {
    'user':'root',
    'password':'root',
    'host':'mariadb',
    'port':3306,
    'database':'alwida_db'
}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.urandom(32)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8mb4&collation=utf8mb4_general_ci"

db = init_db(app)

# def	make_signature():
# 	timestamp = int(time.time() * 1000)
# 	timestamp = str(timestamp)

# 	access_key = "{accessKey}"				# access key id (from portal or Sub Account)
# 	secret_key = "{secretKey}"				# secret key (from portal or Sub Account)
# 	secret_key = bytes(secret_key, 'UTF-8')

# 	method = "GET"
# 	uri = "/sms/v2/services/ncp:sms:kr:297891290516:alwida/messages"

# 	message = method + " " + uri + "\n" + timestamp + "\n"
# 	+ access_key
# 	message = bytes(message, 'UTF-8')
# 	signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
# 	return signingKey

# def make_msg(msg):
#     header = {
#         "Content-Type":"application/json; charset=utf-8",
#         "x-ncp-apigw-timestamp":int(time.time()*1000),
#         "x-ncp-iam-access-key":"",
#         "x-ncp-apigw-signature-v2":make_signature()
#     }
    
#     data = {
#         "type":"SMS",
#         "from":"string",
#         "subject":"string",
#         "content":"string",
#         "messages":[
#             {
#                 "to":"string",
#                 "subject":"string",
#                 "content":"string"
#             }
#         ],
#         "files":[
#             {
#                 "name":"string",
#                 "body":"string"
#             }
#         ],
#         "reserveTime": "yyyy-MM-dd HH:mm",
#         "reserveTimeZone": "string",
#         "scheduleCode": "string"
#     }
    
    

@app.route("/signin", methods=["POST"])
def login():
    if(request.method == "POST"):
        id = request.form.get("id","")
        pw = request.form.get("pw","")
        
        if(id != "" and pw != ""):
            user = user_table.query.filter((user_table.id==id) & (user_table.pw==pw)).first()
            if(user != None):
                return jsonify({'result':True})
            else:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})
        
@app.route("/signup_id", methods=["POST"])
def signup_id():
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
                

# @app.route("/signup_num", methods=["POST"])
# def signup_num():
#     if(request.method == "POST"):
#         phone = request.form.get("phoneNum","")
        
#         if(phone != ""):
            
        

@app.route("/signup", methods=["POST"])
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

@app.route("/destination", methods=["POST"])
def destination():
    if(request.method == "POST"):
        locations = terminal_table.query.with_entities(terminal_table.location).distinct(terminal_table.location).all()
        terminals = terminal_table.query.all()
        
        data = []
        loc_index = {}
        
        for i, loc in enumerate(locations):
            json_data = {}
            json_data["index"] = i
            json_data["local"] = loc[0]
            json_data["terminals"] = []
            data.append(json_data)
            
            loc_index[loc[0]] = i

        for i,tm in enumerate(terminals):
            json_data = {}
            json_data["index"] = len(data[loc_index[tm.location]]["terminals"])
            json_data["terminal"] = tm.name
            # json_data["percentage"] = tm.car_amount
            json_data["percentage"] = random.randrange(0,100)
            if(tm.car_amount < tm.easy):
                json_data["status"] = "원활"
                json_data["color"] = "#32B32D"
            elif(tm.car_amount < tm.normal):
                json_data["status"] = "보통"
                json_data["color"] = "#2585EA"
            else:
                json_data["status"] = "혼잡"
                json_data["color"] = "#FF4D4D"
            data[loc_index[tm.location]]["terminals"].append(json_data)
        return data

@app.route("/container_state", methods=["POST"])
def container_state():
    if(request.method == "POST"):
        containerNum = request.form.get("containerNum","")
        if(containerNum != ""):
            container = container_table.query.filter(container_table.container_num==containerNum).first()
            if(container != None):
                if(container.in_out == True):
                    data = "반입"
                else:
                    data = "반출"
                return jsonify({'result':data}) 
            else:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})
    
@app.route("/carnum", methods=["POST"])
def carnum():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            user = user_table.query.filter(user_table.id==id).first()
            if(user != None):
                return jsonify({'result':user.car_num}) 
            else:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})

@app.route("/reservation", methods=["POST"])
def reservation():
    if(request.method == "POST"):
        id = request.form.get("id","")
        containerNum = request.form.get("containerNum","")
        location = request.form.get("location","")
        terminal = request.form.get("terminal","")
        hour = request.form.get("hour","")
        minute = request.form.get("minute","")
        
        if(id != "" and containerNum!= "" and location != "" and terminal != "" and hour != "" and minute != ""):        
            try:
                tn = terminal_table.query.with_entities(terminal_table.tn).filter((terminal_table.location==location)&(terminal_table.name==terminal)).first()[0]
            
                now = datetime.date.today()
                time = datetime.datetime(now.year,now.month,now.day,int(hour),int(minute),0)
            
                new_reservation = reservation_table(id=id, container_num=containerNum, tn=tn, request_time=time,accept_time=None, suggestion=None)
            
                db.session.add(new_reservation)
                db.session.commit()
            
                return jsonify({'result':True})
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})

@app.route("/recommend_time", methods=["POST"])
def recommend_time():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            suggestion = reservation_table.query.filter(reservation_table.id==id).first().suggestion.split(',')
            if(suggestion != None):
                return suggestion
            else:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})

@app.route("/accept_time", methods=["POST"])
def accept_time():
    if(request.method == "POST"):
        id = request.form.get("id","")
        hour = request.form.get("hour","")
        minute = request.form.get("minute","")
        
        if(id != "" and hour != "" and minute != ""):
            try:
                reservation = reservation_table.query.filter(reservation_table.id==id).first()
                
                now = datetime.date.today()
                time = datetime.datetime(now.year,now.month,now.day,int(hour),int(minute),0)
                reservation.accept_time = time
                
                db.session.commit()
                return jsonify({'result':True})
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})

@app.route("/reservation_state", methods=["POST"])
def reservation_state():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            reservation = reservation_table.query.filter(reservation_table.id==id).first()
            terminal = terminal_table.query.filter(terminal_table.tn==reservation.tn).first()
            if(reservation != None and terminal != None):
                data = {
                    'location':terminal.location,
                    'terminal':terminal.name,
                    'time': reservation.accept_time.strftime("%Y-%m-%d %H:%M:%S")
                }

                return data
            else:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})
        
@app.route("/main_car_load", methods=["POST"])
def main_car_load():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            user = user_table.query.filter(user_table.id==id).first()
            if(user != None):
                data = {
                    "name":user.name,
                    "phoneNum":user.phone,
                    "address":user.address,
                    "carNum":user.car_num
                }
                return data
            else:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})
            
            
@app.route("/main_car_modify", methods=["POST"])
def main_car_modify():
    if(request.method == "POST"):
        id = request.form.get("id","")
        phone = request.form.get("phoneNum","")
        address = request.form.get("address","")
        car_num = request.form.get("carNum","")
        if(id != "" and phone != "" and address != "" and car_num != ""):
            user = user_table.query.filter(user_table.id==id).first()
            if(user != None):
                user.phone = phone
                user.address = address
                user.car_num = car_num
                db.session.commit()
                return jsonify({'result':True})
            else:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})
    
@app.route("/cash", methods=["POST"])
def cash():
    if(request.method == "POST"):
        id = request.form.get("id","")
        user = user_table.query.filter(user_table.id==id).first()
        if(id != "" and user != None):
            try:
                cashs = cash_table.query.filter(cash_table.id==id).order_by(cash_table.pay_datetime).all()
                data = []
                for cash in cashs:
                    data.append({
                        "date":cash.pay_datetime,
                        "receiver":cash.id,
                        "result":cash.publish_pay
                    })
                return data
            except:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})

@app.route("/check", methods=["POST"])
def check():
    if(request.method == "POST"):
        id = request.form.get("id","")
        user = user_table.query.filter(user_table.id==id).first()
        if(id != "" and user != None):
            try:
                checks = check_table.query.filter(check_table.id==id).order_by(check_table.request_time).all()
                data = []
                for check in checks:
                    data.append({
                        "date":check.request_time,
                        "receiver":check.id,
                        "result":check.result
                    })
                return data
            except:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})

@app.route("/receipt", methods=["POST"])
def receipt():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            receipt = receipt_table.query.filter(receipt_table.id == id).first()
            container = container_table.query.filter(container_table.container_num == receipt.container_num).first()
            if(container != None and receipt != None):
                data = {
                    "terminalName":container.tn,
                    "issue":receipt.publish,
                    "date":receipt.publish_datetime,
                    "divison":container.in_out,
                    "containerNum":container.container_num,
                    "deviceLocation":container.position,
                    "standard":container.scale,
                    "fm":container.fm
                }
                return data
            else:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})
            

app.run(host="0.0.0.0", port=5000)
