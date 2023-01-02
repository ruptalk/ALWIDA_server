from flask import Blueprint, request, jsonify
from models import user_table, db

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