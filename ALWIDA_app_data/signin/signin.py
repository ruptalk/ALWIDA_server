from flask import Blueprint, request, jsonify
from models import user_table

blue_signin = Blueprint("signin", __name__, url_prefix="/signin")

@blue_signin.route("/", methods=["POST"])
def login():
    if(request.method == "POST"):
        id = request.form.get("id","")
        pw = request.form.get("pw","")
        
        if(id != "" and pw != ""):
            try:
                user = user_table.query.filter((user_table.id==id) & (user_table.pw==pw)).first()
                return jsonify({'result':True})
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'})