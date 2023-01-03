import random
import datetime
from flask import Blueprint, request, jsonify
from models import user_table, terminal_table, reservation_table, container_table, chatting_table, message_table, db

blue_dest = Blueprint("dest", __name__, url_prefix="/dest")

@blue_dest.route("/", methods=["POST"])
def dest():
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

@blue_dest.route("/container_state", methods=["POST"])
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

@blue_dest.route("/car", methods=["POST"])
def car():
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

@blue_dest.route("/reservation", methods=["POST"])
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
        
@blue_dest.route("/recommend", methods=["POST"])
def recommend():
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
        
@blue_dest.route("/accept", methods=["POST"])
def accept():
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
                
                new_chat = chatting_table(id=id, state=0)
                new_msg= message_table(id=id, message="운송작업이 생성되었습니다.\n사전반출입정보 승인",time=datetime.datetime.now(), sender=False)
                
                db.session.add(new_chat)
                db.session.add(new_msg)
                db.session.commit()
                return jsonify({'result':True})
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})
        
        
@blue_dest.route("/reservation_state", methods=["POST"])
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