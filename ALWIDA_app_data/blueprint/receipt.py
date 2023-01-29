from flask import Blueprint, request, jsonify
from models import receipt_table, container_table

blue_receipt = Blueprint("receipt", __name__, url_prefix="/receipt")

@blue_receipt.route("/", methods=["POST"])
def receipt():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            try:
                receipt = receipt_table.query.filter(receipt_table.id == id).first()
                container = container_table.query.filter(container_table.container_num == receipt.container_num).first()
                data = {
                    "terminalName":container.tn,
                    "issue":receipt.publish,
                    "date":receipt.publish_datetime,
                    "divison":"반입" if(container.in_out) else "반출",
                    "containerNum":container.container_num,
                    "deviceLocation":container.position,
                    "standard":container.scale,
                    "fm":container.fm,
                    "publish":receipt.publish
                }
                return data
            except:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})