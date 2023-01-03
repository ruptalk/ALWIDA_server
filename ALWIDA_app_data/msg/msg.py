import datetime
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import admin_table, user_table, terminal_table, container_table, reservation_table, receipt_table, cash_table, check_table, chatting_table, message_table, db

blue_msg = Blueprint("msg", __name__, url_prefix="/msg")

@blue_msg.route("/info", methods=["POST"])
def info():
    if(request.method == "POST"):
        id = request.form.get("id")
        if(id != ""):
            try:
                container_num = reservation_table.query.filter(reservation_table.id==id).first().container_num
                container = container_table.query.filter(container_table.container_num == container_num).first()
                
                data = {
                    "terminalName":container.name,
                    "terminalAbb":container.tn,
                    "scale":container.scale,
                    "deviceLocation":container.position,
                    "containerNum":container.container_num
                }
                
                return data
            except:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})

@blue_msg.route("/send", methods=["POST"])
def send():
    if(request.method == "POST"):
        id = request.form.get("id","")
        congestion = request.form.get("congestion", type=bool)
        numOfCar = request.form.get("numOfCar", type=bool)

        if(id != ""):
            try:
                now = datetime.datetime.now()
                if(congestion):
                    new_msg = message_table(id=id, message="목적지 혼잡도를 알려주세요.", time=now, sender=True)
                    db.session.add(new_msg)
                    db.session.commit()
                    
                    tn = reservation_table.query.filter(reservation_table.id==id).first().tn
                    terminal = terminal_table.query.filter(terminal_table.tn==tn).first()
                        
                    if(terminal.car_amount < terminal.easy):
                        state = "원활"
                    elif(terminal.car_amount < terminal.normal):
                        state = "보통"
                    else:
                        state = "혼잡"
                        
                    time = now.strftime('%Y-%m-%d %H:%M')
                    
                    msg = f"목적지 혼잡도\n{tn} 터미널\n혼잡도: {state}\n{time} 기준"
                elif(numOfCar):
                    new_msg = message_table(id=id, message="부두 내 차량 현황을알려주세요.", time=now, sender=True)
                    db.session.add(new_msg)
                    db.session.commit()
                        
                    tn = reservation_table.query.filter(reservation_table.id==id).first().tn
                    terminal = terminal_table.query.filter(terminal_table.tn==tn).first()
                    
                    time = now.strftime('%Y-%m-%d %H:%M')
                    msg = f"부두 내 차량 현황\n{terminal.car_amount}\n{time}"
                        
                new_msg = message_table(id=id, message=msg, time=now, sender=False)
                    
                db.session.add(new_msg)
                db.session.commit()
                
                data = {
                    "description":msg,
                    "hour":now.hour,
                    "min":now.minute
                }
                
                return data
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'}) 