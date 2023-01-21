from datetime import datetime
from flask import Blueprint, request, session, render_template
from models import cash_table, db

blue_cash = Blueprint("cash", __name__, url_prefix="/cash")

def is_login():
    return session.get("info")

def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");location.href = document.referrer;</script>' 

@blue_cash.route("/", methods=["GET","POST"])
def cash():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        cash = cash_table.query.filter_by().all()
        
        return render_template('cash.html', cashs=cash, usr=usr, check=is_login())
    elif(request.method=="POST"):
        id = request.form.get("id","")
        container_num = request.form.get("container_num","")
        
        cash = cash_table.query.filter((cash_table.id==id)&(cash_table.container_num==container_num)).first()
        cash.publish_pay = True
        cash.pay_datetime = datetime.now()
        db.session.commit()
        
        return alert('발급완료!')