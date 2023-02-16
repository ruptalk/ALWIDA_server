from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, session, render_template
from models import terminal_table, reservation_table, db

blue_reservation = Blueprint("reservation", __name__, url_prefix="/reservation")

def is_login():
    return session.get("info")

def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");location.href = document.referrer;</script>'

def select_tn_func():
     return terminal_table.query.with_entities(terminal_table.tn).filter_by().all()

def congestion(count):
    usr = session.get("info")
    terminal = terminal_table.query.filter_by(tn=usr["tn"]).first()
    
    if(count < terminal.normal):
        return '원활'
    elif(count < terminal.difficalt):
        return '보통'
    else:
        return '혼잡'

def recommand(accept):
    now = datetime.now().strftime('%H%M')
    result = dict()
    accept =  [[x[0],x[1]] for x in accept]
    for acc in accept:
        if(int(acc[0][2:]) >= 0 and int(acc[0][2:]) < 30):
            acc[0] = list(acc[0])
            acc[0][2:] = '00'
            acc[0] = ''.join(acc[0])
        else:
            acc[0] = list(acc[0])
            acc[0][2:] = '30'
            acc[0] = ''.join(acc[0])
    
    accept = dict(accept)
    for i in range(24):
        zero = str(i).zfill(2)+'00' 
        thirty = str(i).zfill(2)+'30'
        
        if(int(zero) >= int(now)):
            if(zero in accept):
                result[zero]=[accept[zero], congestion(accept[zero])]
            else:
                result[zero]=[0, congestion(0)]
            result[zero[:2] + ':' + zero[2:]] = result.pop(zero)
            
        if(int(thirty) >= int(now)):
            if(thirty in accept):
                result[thirty]=[accept[thirty], congestion(accept[thirty])]
            else:
                result[thirty]=[0, congestion(0)]
            result[thirty[:2] + ':' + thirty[2:]] = result.pop(thirty)
    return result

@blue_reservation.route("/", methods=["GET", "POST"])
def reservation():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        reservation = reservation_table.query.filter(reservation_table.tn==select_tn).all()
        
        accept = reservation_table.query.with_entities(
            reservation_table.accept_time,
            func.count(reservation_table.accept_time).label('count')
        ).filter(
            (reservation_table.tn == select_tn)&
            (reservation_table.accept_time != None)&
            (func.date_format(reservation_table.accept_time, '%Y-%m-%d') == func.date_format(func.now(), '%Y-%m-%d'))
            &(reservation_table.accept_time >= func.now())
        ).group_by(
            func.hour(reservation_table.accept_time),
            func.floor(func.minute(reservation_table.accept_time)/30)*10
        ).order_by(reservation_table.accept_time).all()
        
        suggestion = reservation_table.query.with_entities(
            func.date_format(reservation_table.accept_time, '%H%i'),
            func.count(reservation_table.accept_time).label('count')
        ).filter(
            (reservation_table.tn == select_tn)&
            (reservation_table.accept_time != None)&
            (func.date_format(reservation_table.accept_time, '%Y-%m-%d') == func.date_format(func.now(), '%Y-%m-%d'))
            &(reservation_table.accept_time >= func.now())
        ).group_by(
            func.hour(reservation_table.accept_time),
            func.floor(func.minute(reservation_table.accept_time)/30)*10
        ).order_by(reservation_table.accept_time).all()
        
        accept_list =  [[x[0],x[1]] for x in accept]
        
        for acc in accept_list:
            if(acc[0].minute >= 0 and acc[0].minute < 30):
                acc[0] = acc[0].replace(minute=0)
            else:
                acc[0] = acc[0].replace(minute=30)
            
            acc.append(congestion(acc[1]))
        return render_template('reservation.html', reservations=reservation, suggestions=recommand(suggestion), accepts=accept_list, usr=usr, select_tn=select_tn, tns=select_tn_func(), check=is_login())
    elif(request.method=="POST"):
        try:
            timeList = ','.join(request.form.getlist("timeList"))
            id = request.form.get("id","")
            reservation = reservation_table.query.filter_by(id=id).first()
            reservation.suggestion = timeList
        
            db.session.commit()
            return alert("완료!")
        except:
            return alert("에러발생")