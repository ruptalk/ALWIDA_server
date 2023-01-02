from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import admin_table, user_table, terminal_table, container_table, reservation_table, receipt_table, cash_table, check_table, chatting_table, message_table, init_db

blue_msg = Blueprint("msg", __name__, url_prefix="/msg")

@blue_msg.route("/info", methods=["POST"])
def info():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            try:
                container_num = reservation_table.query.filter(reservation_table.id==id).first().container_num
                container = container_table.query.filter(container_table.container_num == container_num).first()
                
                data = {
                    "terminalName":container.tn,
                    "terminalAbb":container.position,
                    "scale":container.scale,
                    "deviceLocation":"test",
                    "containerNum":container.container_num
                }
                
                return data
            except:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})