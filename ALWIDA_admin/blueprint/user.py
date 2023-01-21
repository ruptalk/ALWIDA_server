from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, session, render_template
from models import user_table, reservation_table, terminal_table

blue_user = Blueprint("user", __name__, url_prefix="/user")

def is_login():
    return session.get("info")

def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");location.href = document.referrer;</script>' 
    
def select_tn_func():
     return terminal_table.query.with_entities(terminal_table.tn).filter_by().all()

@blue_user.route("/", methods=["GET"])
def user():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        date = request.args.get("date",datetime.now().date())
        
        user = user_table.query.filter_by().all()
        
        reservation = reservation_table.query.join(user_table, reservation_table.id==user_table.id)\
                                                            .with_entities(reservation_table.accept_time, user_table.id, user_table.car_num, reservation_table.container_num, user_table.phone)\
                                                            .filter((reservation_table.tn==select_tn) & (reservation_table.accept_time != None) & (func.date_format(reservation_table.accept_time,'%Y-%m-%d') == date)).all()
        
        return render_template('user.html', users=user, reservations=reservation, date=date, select_tn=select_tn, tns=select_tn_func(), usr=usr, check=is_login())