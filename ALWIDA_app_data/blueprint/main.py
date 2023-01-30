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

def cash_convert(value):
    if(value):
        return "수납완료"
    else:
        return "미정산"

@blue_main.route("/cash", methods=["POST"])
def cash():
    if(request.method == "POST"):
        id = request.form.get("id","")
        user = user_table.query.filter(user_table.id==id).first()
        if(id != "" and user != None):
            try:
                cashs = cash_table.query.filter(cash_table.id==id).order_by(cash_table.pay_datetime).all()
                data = []
                for i, cash in enumerate(cashs):
                    data.append({
                        "id":i+1,
                        "date":cash.pay_datetime.strftime("%y.%m.%d %H.%M") if(cash.pay_datetime != None) else cash.pay_datetime,
                        "receiver":cash.id,
                        "result":cash_convert(cash.publish_pay)
                    })
                return data
            except Exception as e:
                print(e)
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})


def check_convert(value):
    if(value == 0):
        return "수신대기"
    elif(value == 1):
        return "수신완료"
    elif(value == 2):
        return "보류"
    elif(value == 3):
        return "검사합격"
    else:
        return "검사불합격"

@blue_main.route("/check", methods=["POST"])
def check():
    if(request.method == "POST"):
        id = request.form.get("id","")
        user = user_table.query.filter(user_table.id==id).first()
        if(id != "" and user != None):
            try:
                checks = check_table.query.filter(check_table.id==id).order_by(check_table.request_time).all()
                data = []
                for i, check in enumerate(checks):
                    data.append({
                        "id":i+1,
                        "date":check.request_time.strftime("%y.%m.%d %H.%M") if(check.request_time != None) else check.request_time,
                        "receiver":check.id,
                        "result":check_convert(check.result)
                    })
                return data
            except Exception as e:
                print(e)
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})