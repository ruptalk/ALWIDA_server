import os
from flask import Flask, request, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, inspect
from datetime import datetime
from operator import itemgetter

db = {
    'user':'root',
    'password':'root',
    'host':'mariadb',
    'port':3306,
    'database':'alwida_db'
}

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8mb4&collation=utf8mb4_general_ci"

db = SQLAlchemy(app)

class admin_table(db.Model):
    uid = db.Column(db.String(36), primary_key=True, nullable=False)
    id = db.Column(db.String(20), nullable=False, unique=True)
    pw = db.Column(db.String(20), nullable=False)
    tn = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    enroll = db.Column(db.Boolean, nullable=True)
    
    def to_json(self):
        return {
            "id" : self.id,
            "pw":self.pw,
            "tn":self.tn
        }

class terminal_table(db.Model):
    tn = db.Column(db.String(30), primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    car_amount = db.Column(db.Integer, nullable=False)
    easy = db.Column(db.Integer, default=0)
    normal = db.Column(db.Integer, default=0)
    difficalt = db.Column(db.Integer, default=0)

class container_table(db.Model):
    container_num = db.Column(db.String(30), primary_key=True, nullable=False)
    id = db.Column(db.String(20), nullable=False)
    tn = db.Column(db.String(30), nullable=False)
    scale = db.Column(db.String(30), nullable=False)
    fm = db.Column(db.String(30), nullable=False)
    position = db.Column(db.String(30), nullable=True)
    contain_last_time = db.Column(db.DateTime, nullable=False)
    in_out = db.Column(db.Boolean, nullable=False)

class reservation_table(db.Model):
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    container_num = db.Column(db.String(30), nullable=False)
    tn = db.Column(db.String(30), nullable=False)
    request_time = db.Column(db.DateTime, nullable=False)
    accept_time = db.Column(db.DateTime, nullable=True)
    suggestion = db.Column(db.String(20), nullable=True)

class receipt_table(db.Model):
    container_num = db.Column(db.String(30), primary_key=True, nullable=False)
    id = db.Column(db.String(20), nullable=False)
    publish = db.Column(db.Boolean, nullable=False)
    publish_datetime = db.Column(db.DateTime, nullable=True)

def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");history.back(1);</script>'
    
def is_login():
    return session.get("info")

@app.route("/")
@app.route("/index")
def index():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    usr = session.get("info")
    admin_tn = admin_table.query.filter_by(id=usr["id"]).first().tn
    terminal = terminal_table.query.filter_by(tn=admin_tn).first()
    container = container_table.query.filter_by(tn=admin_tn).all()
    return render_template('index.html', terminal=terminal, containers=container)

@app.route("/signin", methods=['GET','POST'],  endpoint='signin')
def login():
    if(request.method == 'GET'):
        return render_template('signin.html')
    elif(request.method == 'POST'):
        id = request.form.get("id","")
        pw = request.form.get("pw","")
        
        usr = admin_table.query.filter_by(id=id, pw=pw).first()
        if(not hasattr(usr, 'id')):
            return alert("Check userid or userpw")
        session["info"] = usr.to_json()
        return alert("로그인 성공!","/")

@app.route("/signout")
def signout():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    del session["info"]
    return alert("로그아웃!","/")
    
@app.route("/congestion_update", methods=["POST"])
def congestion_update():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="POST"):
        easy = request.form.get("easy","")
        normal = request.form.get("normal","")
        difficalt = request.form.get("difficalt","")
        
        usr = session.get("info")
        admin_tn = admin_table.query.filter_by(id=usr["id"]).first().tn
        terminal = terminal_table.query.filter_by(tn=admin_tn).first()
        
        terminal.easy = easy
        terminal.normal = normal
        terminal.difficalt = difficalt
        
        db.session.commit()
        return alert("완료!")
    
@app.route("/container_popup", methods=["POST"])
def container_popup():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    container_num = request.form.get("container_num","")
    return render_template('container_popup.html', container_num=container_num)
    
@app.route("/container_update", methods=["POST"])
def container_update():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    container_num = request.form.get("container_num","")
    position = request.form.get("position","")
    scale = request.form.get("scale","")
    fm = request.form.get("fm","")

    contaniner = container_table.query.filter_by(container_num=container_num).first()
    contaniner.position = position
    contaniner.scale = scale
    contaniner.fm = fm
    
    db.session.commit()
    return '<script>alert("완료!");window.close();</script>'

def congestion(count):
    usr = session.get("info")
    admin_tn = admin_table.query.filter_by(id=usr["id"]).first().tn
    terminal = terminal_table.query.filter_by(tn=admin_tn).first()
    
    if(count < terminal.normal):
        return '원활'
    elif(count < terminal.difficalt):
        return '보통'
    else:
        return '혼잡'

def recommand(accept):
    # now = datetime.now().strftime('%H%M')
    now = '0600'
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

@app.route("/reservation", methods=["GET"])
def reservation():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        admin_tn = admin_table.query.filter_by(id=usr["id"]).first().tn
        reservation = reservation_table.query.filter_by(tn=admin_tn).all()
        
        accept = reservation_table.query.with_entities(
            reservation_table.accept_time,
            func.count(reservation_table.accept_time).label('count')
        ).filter(
            (reservation_table.tn == usr["tn"])&
            (reservation_table.accept_time != None)&
            (func.date_format(reservation_table.accept_time, '%Y-%m-%d') == func.date_format(func.now(), '%Y-%m-%d'))
            # &(reservation_table.accept_time >= func.now())
        ).group_by(
            func.hour(reservation_table.accept_time),
            func.floor(func.minute(reservation_table.accept_time)/30)*10
        ).order_by(reservation_table.accept_time).all()
        
        terminal = terminal_table.query.filter_by(tn=admin_tn).first()
        
        accept_list =  [[x[0],x[1]] for x in accept]
        
        for acc in accept_list:
            if(acc[0].minute >= 0 and acc[0].minute < 30):
                acc[0] = acc[0].replace(minute=0)
            else:
                acc[0] = acc[0].replace(minute=30)
            
            acc.append(congestion(acc[1]))
        return render_template('reservation.html', reservations=reservation, accepts=accept_list)
    
@app.route("/reservation_popup", methods=["POST"])
def reservation_popup():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    usr = session.get("info")
    id = request.form.get("id","")
    
    accept = reservation_table.query.with_entities(
        func.date_format(reservation_table.accept_time, '%H%i'),
        func.count(reservation_table.accept_time).label('count')
    ).filter(
        (reservation_table.tn == usr["tn"])&
        (reservation_table.accept_time != None)&
        (func.date_format(reservation_table.accept_time, '%Y-%m-%d') == func.date_format(func.now(), '%Y-%m-%d'))
        # &(reservation_table.accept_time >= func.now())
    ).group_by(
        func.hour(reservation_table.accept_time),
        func.floor(func.minute(reservation_table.accept_time)/30)*10
    ).order_by(reservation_table.accept_time).all()
    
    result = recommand(accept)
    return render_template('reservation_popup.html', result=result, id=id)

@app.route("/reservation_update", methods=["POST"])
def reservation_update(): 
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    timeList = request.form.get("timeList","")
    id = request.form.get("id","")
    reservation = reservation_table.query.filter_by(id=id).first()
    reservation.suggestion = timeList
    
    db.session.commit()
    return '<script>alert("완료!");window.close();</script>'

@app.route("/receipt", methods=["GET", "POST"])
def receipt():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        admin_tn = admin_table.query.filter_by(id=usr["id"]).first().tn
        receipt = receipt_table.query.join(container_table, container_table.container_num==receipt_table.container_num)\
                                                                .with_entities(receipt_table.container_num, receipt_table.id, receipt_table.publish, container_table.position, container_table.scale, container_table.fm)\
                                                                .filter(container_table.tn == admin_tn).all()
                                              
        return render_template('receipt.html', receipts=receipt)
    elif(request.method=="POST"):
        id = request.form.get("id","")
        container_num = request.form.get("container_num","")
        receipt = receipt_table.query.filter_by(id=id).first()
        receipt.publish = True
        db.session.commit()
    
        return f'<script>alert("{id}가 요청하신 컨테어너 번호 {container_num} 발급이 완료되었습니다.");window.close();</script>'

app.run(host="0.0.0.0", port=8888)
