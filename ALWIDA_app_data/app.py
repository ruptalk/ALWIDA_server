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

app.run(host="0.0.0.0", port=5000)
