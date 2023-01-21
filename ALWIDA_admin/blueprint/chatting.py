from datetime import datetime
from flask import Blueprint, request, session, render_template, jsonify
from models import user_table, reservation_table, chatting_table, message_table, terminal_table, db

blue_chatting = Blueprint("chatting", __name__, url_prefix="/chatting")

def is_login():
    return session.get("info")

def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");location.href = document.referrer;</script>' 
    
def select_tn_func():
     return terminal_table.query.with_entities(terminal_table.tn).filter_by().all()
    
@blue_chatting.route("/chatting", methods=["GET","POST"])
def chatting():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        chatting = chatting_table.query.join(reservation_table, reservation_table.id==chatting_table.id)\
                                                            .outerjoin(user_table, user_table.id == chatting_table.id)\
                                                            .with_entities(chatting_table.state, chatting_table.id, user_table.car_num, reservation_table.container_num)\
                                                            .filter(reservation_table.tn==select_tn).all()

        return  render_template('chatting.html', chattings=chatting, select_tn=select_tn, tns=select_tn_func(), usr=usr, check=is_login())
    elif(request.method=="POST"):
        data = request.get_json()
        message = message_table.query.filter(message_table.id == data["id"]).order_by(message_table.time).all()
        message = [msg.obj_to_dict() for msg in message]
        
        for i, msg in enumerate(message):
            message[i]["time"] = msg["time"].strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify(message = message, len=len(message))

@blue_chatting.route("/update", methods=["POST"])
def update():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    if(request.method=="POST"):
        data = request.get_json()
        new_msg = message_table(id=data["id"], message=data["text"], time=datetime.now(), sender=False)
        db.session.add(new_msg)
        db.session.commit()
        
        message = message_table.query.filter(message_table.id == data["id"]).order_by(message_table.time).all()
        message = [msg.obj_to_dict() for msg in message]
        
        for i, msg in enumerate(message):
            message[i]["time"] = msg["time"].strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify(message = message, len=len(message))