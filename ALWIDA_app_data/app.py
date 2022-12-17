import os
import random
from flask import Flask, request, render_template, session, url_for, jsonify
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

@app.route("/signin", methods=["POST"])
def login():
    if(request.method == "POST"):
        id = request.form.get("id","")
        pw = request.form.get("pw","")
        
        if(id != "" and pw != ""):
            user = user_table.query.filter((user_table.id==id) & (user_table.pw==pw)).first()
            if(hasattr(user, 'id')):
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
            print(user)
            if(user == None):
                return jsonify({'result':True})
            else:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})
                

# @app.route("/signup_num", methods=["POST"])
# def signup_num():
#     if(request.method == "POST"):
#         id = request.form.get("id","")
#         checkNum = request.form.get("checknum","")
        
#         user = user_table.query.filter((user_table.id==id) & (user_table.check_num==checkNum)).first()

#         if(hasattr(user, 'id')):
#             return jsonify({'result':True})
#         else:
#             return jsonify({'result':False})
        

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
                new_user = user_table(id=id, pw=pw, name=name, phone=phoneNum, car_num=carNum, address=address, check_num=None, info_agree=agreeCheck, info_gps=True)

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
            json_data["percentage"] = tm.car_amount
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
        time = request.form.get("time","")
        
        if(id != "" and containerNum!= "" and location != "" and terminal != "" and time != ""):        
            try:
                tn = terminal_table.query.with_entities(terminal_table.tn).filter((terminal_table.location==location)&(terminal_table.name==terminal)).first()[0]
            
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
            if(suggestion!=None):
                return suggestion
            else:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})

@app.route("/accept_time", methods=["POST"])
def accept_time():
    if(request.method == "POST"):
        id = request.form.get("id","")
        selectedTime = request.form.get("selectedTime","")
        
        if(id != "" and selectedTime != ""):
            try:
                reservation = reservation_table.query.filter(reservation.id==id).first()
                reservation.accept_time = selectedTime
                
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
            data = {
                'location':terminal.location,
                'terminal':terminal.name,
                'time':reservation.accept_time
            }
            return data
        else:
            return jsonify({'result':'error'})
app.run(host="0.0.0.0", port=5000)
