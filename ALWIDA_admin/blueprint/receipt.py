from flask import Blueprint, request, session, render_template
from models import receipt_table, cash_table, container_table, db

blue_receipt = Blueprint("receipt", __name__, url_prefix="/receipt")

def is_login():
    return session.get("info")

def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");location.href = document.referrer;</script>'        

@blue_receipt.route("/", methods=["GET", "POST"])
def receipt():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        receipt = receipt_table.query.join(container_table, container_table.container_num==receipt_table.container_num)\
                                                                .with_entities(receipt_table.container_num, receipt_table.id, receipt_table.publish, container_table.position, container_table.scale, container_table.fm)\
                                                                .filter(container_table.tn == usr["tn"]).all()
                                              
        return render_template('receipt.html', receipts=receipt, usr=usr, check=is_login())
    elif(request.method=="POST"):
        try:
            id = request.form.get("id","")
            container_num = request.form.get("container_num","")
            receipt = receipt_table.query.filter((receipt_table.id==id)&(receipt_table.container_num==container_num)).first()
            receipt.publish = True
            
            new_cash = cash_table(idx=None, id=id, container_num=container_num, publish_pay=False, pay_datetime=None)
            db.session.add(new_cash)
            db.session.commit()
        
            return alert('발급완료!')
        except:
            return alert('에러발생')