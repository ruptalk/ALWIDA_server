import os
import base64
from flask import Flask, request, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, inspect
from datetime import datetime
from operator import itemgetter
import uuid

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
            "name" : self.name,
            "tn":self.tn
        }

class user_table(db.Model):
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    pw = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    tn = db.Column(db.String(30), nullable=False)
    car_num = db.Column(db.String(20), nullable=False)
    check_num = db.Column(db.String(5), nullable=False)
    info_agree = db.Column(db.Boolean, nullable=False)
    info_gps = db.Column(db.Boolean, nullable=False)

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

class cash_table(db.Model):
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    container_num = db.Column(db.String(30), nullable=False)
    publish_pay = db.Column(db.Boolean, nullable=False)
    pay_datetime = db.Column(db.DateTime, nullable=True)

class check_table(db.Model):
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    request_time = db.Column(db.DateTime, nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
    result = db.Column(db.Integer, nullable=False)

class chatting_table(db.Model):
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    state = db.Column(db.Integer, nullable=False)
    
class message_table(db.Model):
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    sender = db.Column(db.Boolean, nullable=False)
    

def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");location.href = document.referrer;</script>'
    
def is_login():
    return session.get("info")

@app.route("/signin", methods=['GET','POST'])
def signin():
    if is_login():
        return alert("이미 로그인하셨습니다!","/")
    if(request.method == 'GET'):
        return render_template('signin.html',check=is_login())
    elif(request.method == 'POST'):
        id = request.form.get("id","")
        pw = request.form.get("pw","")
        
        usr = admin_table.query.filter_by(id=id, pw=pw).first()
        if(not hasattr(usr, 'id')):
            return alert("Check userid or userpw")
        session["info"] = usr.to_json()
        return alert("로그인 성공!","/")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if(request.method=="GET"):
        tns = terminal_table.query.with_entities(terminal_table.tn).filter_by().all()
        return render_template('signup.html',tns=tns, check=is_login())
    elif(request.method=="POST"):
        try:
            name = request.form.get("name","")
            id = request.form.get("id","")
            pw = request.form.get("pw","")
            phone = request.form.get("phone","")
            group = request.form.get("group","")
            
            admin = admin_table.query.filter_by(id=id, pw=pw).first()
            if(hasattr(admin, 'id')):
                return alert("이미 존재하는 아이디입니다!")
            
            new_admin = admin_table(uid=str(uuid.uuid4()),id=id,pw=pw,phone=phone,tn=group,name=name,enroll=False)
            db.session.add(new_admin)
            db.session.commit()
            
            return alert("완료!")
        except:
            return alert("에러!")

@app.route("/signout")
def signout():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    del session["info"]
    return alert("로그아웃!","/signin")

def select_tn_func():
     return terminal_table.query.with_entities(terminal_table.tn).filter_by().all()

@app.route("/")
@app.route("/index")
def index():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        terminal = terminal_table.query.filter_by(tn=select_tn).first()
        container = container_table.query.filter_by(tn=select_tn).all()
        
        return render_template('terminal.html', terminal=terminal, containers=container, select_tn=select_tn, tns=select_tn_func(), usr=usr, check=is_login())

@app.route("/terminal_update", methods=["POST"])
def terminal_update():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    try:
        usr = session.get("info")
        select_tn = request.form.get("select_tn",usr["tn"])
        car_amount = request.form.get("car_amount")
        easy = request.form.get("easy","")
        normal = request.form.get("normal","")
        difficalt = request.form.get("difficalt","")
        
        terminal = terminal_table.query.filter_by(tn=select_tn).first()
        
        terminal.car_amount = car_amount    
        terminal.easy = easy
        terminal.normal = normal
        terminal.difficalt = difficalt
        
        db.session.commit()
        
        return alert("완료!")
    except:
        return alert("에러발생")
    
@app.route("/container_update", methods=["POST"])
def container_update():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    try:
        container_num = request.form.get("container_num","")
        position = request.form.get("position","")
        scale = request.form.get("scale","")
        fm = request.form.get("fm","")

        contaniner = container_table.query.filter_by(container_num=container_num).first()
        contaniner.position = position
        contaniner.scale = scale
        contaniner.fm = fm
        
        db.session.commit()
        return alert("완료!")
    except:
        return alert("에러발생")

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

@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        reservation = reservation_table.query.filter_by(tn=select_tn).all()
        
        accept = reservation_table.query.with_entities(
            reservation_table.accept_time,
            func.count(reservation_table.accept_time).label('count')
        ).filter(
            (reservation_table.tn == select_tn)&
            (reservation_table.accept_time != None)&
            (func.date_format(reservation_table.accept_time, '%Y-%m-%d') == func.date_format(func.now(), '%Y-%m-%d'))
            # &(reservation_table.accept_time >= func.now())
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
            # &(reservation_table.accept_time >= func.now())
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

@app.route("/receipt", methods=["GET", "POST"])
def receipt():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
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
            receipt = receipt_table.query.filter((id==id)&(container_num==container_num)).first()
            receipt.publish = True
            db.session.commit()
        
            return alert('발급완료!')
        except:
            return alert('에러발생')

@app.route("/cash", methods=["GET","POST"])
def cash():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        cash = cash_table.query.filter_by().all()
        
        return render_template('cash.html', cashs=cash, usr=usr, check=is_login())
    elif(request.method=="POST"):
        id = request.form.get("id","")
        container_num = request.form.get("container_num","")
        
        cash = cash_table.query.filter((id==id)&(container_num==container_num)).first()
        cash.publish_pay = True
        cash.pay_datetime = datetime.now()
        db.session.commit()
        
        return alert('발급완료!')
        
@app.route("/check", methods=["GET","POST"])
def check():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        check_wait = check_table.query.join(container_table, container_table.id==check_table.id)\
                                                            .with_entities(check_table.id, check_table.request_time, check_table.img, check_table.result, container_table.container_num, container_table.tn)\
                                                            .filter((container_table.tn==select_tn) & ((check_table.result==0) | (check_table.result==1) | (check_table.result==2))).all()
                                                                       
        check_result = check_table.query.join(container_table, container_table.id==check_table.id)\
                                                            .with_entities(check_table.id, check_table.request_time, check_table.img, check_table.result, container_table.container_num, container_table.tn)\
                                                            .filter((container_table.tn==select_tn) & ((check_table.result==3) | (check_table.result==4))).all()
        
        check_wait = [list(x) for x in check_wait]
        
        for data in check_wait:
            data[2] = base64.b64encode(data[2])
            data[2] = data[2].decode() 
        
        return render_template('check.html', check_waits=check_wait,check_results=check_result, select_tn=select_tn, tns=select_tn_func(), usr=usr, check=is_login())
    elif(request.method=="POST"):
        id = request.form.get("id")
        type = request.form.get("type")
        
        check = check_table.query.filter(check_table.id==id).first()
        if(type=="pass"):
            check.result=3
        elif(type=="fail"):
            check.result=4
        elif(type=="hold"):
            check.result=2
        else:
            return alert("에러!")
        
        db.session.commit()
        
        return alert("완료!")
        
@app.route("/user_info", methods=["GET"])
def user_info():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        date = request.args.get("date",datetime.now().date())
        
        user = user_table.query.filter_by(tn=select_tn).all()
        
        reservation = reservation_table.query.join(user_table, reservation_table.id==user_table.id)\
                                                            .with_entities(reservation_table.accept_time, user_table.id, user_table.car_num, reservation_table.container_num, user_table.phone)\
                                                            .filter((reservation_table.tn==select_tn) & (reservation_table.accept_time != None) & (reservation_table.accept_time > date)).all()
        
        return render_template('user_info.html', users=user, reservations=reservation, date=date, select_tn=select_tn, tns=select_tn_func(), usr=usr, check=is_login())
    
@app.route("/chatting", methods=["GET","POST"])
def chatting():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        chatting = chatting_table.query.join(reservation_table, reservation_table.id==chatting_table.id)\
                                                            .outerjoin(user_table, user_table.id == chatting_table.id)\
                                                            .with_entities(chatting_table.state, chatting_table.id, user_table.car_num, reservation_table.container_num)\
                                                            .filter(reservation_table.tn==select_tn).all()
        message = message_table.query.filter().order_by(message_table.time).all()
        
        chatting = [list(x) for x in chatting]
        
        for chat in chatting:
            id = chat[1]
            msgs = []
            for msg in message:
                if(msg.id == id):
                    msgs.append([msg.message,msg.time.strftime("%Y-%m-%d %H:%M:%S"),msg.sender])
            chat.append(msgs)

        return  render_template('chatting.html', chattings=chatting, select_tn=select_tn, tns=select_tn_func(), usr=usr, check=is_login())
    elif(request.method=="POST"):
        id = request.form.get("id")
        text = request.form.get("send_text")
        
        msg = message_table(id=id, message=text, time=datetime.now(), sender=False)
        db.session.add(msg)
        db.session.commit()
        
        return alert("완료!")
    

app.run(host="0.0.0.0", port=8888)