from flask import Blueprint, request, jsonify
from models import user_table

blue_signin = Blueprint("signin", __name__, url_prefix="/signin")

@blue_signin.route("/", methods=["POST"])
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