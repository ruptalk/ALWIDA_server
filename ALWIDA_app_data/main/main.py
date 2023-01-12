from flask import Blueprint, request, jsonify
from models import user_table, cash_table, check_table, db

blue_main = Blueprint("main", __name__, url_prefix="/main")

@blue_main.route("/info", methods=["POST"])
def info():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            try:
                user = user_table.query.filter(user_table.id==id).first()
                data = {
                    "name":user.name,
                    "phoneNum":user.phone,
                    "address":user.address,
                    "carNum":user.car_num
                }
                return data
            except:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})
        
@blue_main.route("/carmod", methods=["POST"])
def carmod():
    if(request.method == "POST"):
        id = request.form.get("id","")
        phone = request.form.get("phoneNum","")
        address = request.form.get("address","")
        car_num = request.form.get("carNum","")
        if(id != "" and phone != "" and address != "" and car_num != ""):
            try:
                user = user_table.query.filter(user_table.id==id).first()
                user.phone = phone
                user.address = address
                user.car_num = car_num
                db.session.commit()
                return jsonify({'result':True})
            except:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})

@blue_main.route("/cash", methods=["POST"])
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
        
@blue_main.route("/check", methods=["POST"])
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