import datetime
from flask import Blueprint, request, jsonify
from models import check_table, db

blue_check = Blueprint("check", __name__, url_prefix="/check")

@blue_check.route("/", methods=["POST"], strict_slashes=False)
def check():
    if(request.method == "POST"):
        id = request.form.get("id","")
        img = request.files['file']
        
        if(id != "" and img):
            try:
                new_check = check_table(idx=None, id=id, request_time=datetime.datetime.now(), img=img.read(), result=0)
                db.session.add(new_check)
                db.session.commit()

                return jsonify({'result':True})
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'}) 