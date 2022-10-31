import os
from flask import Flask, request, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, inspect

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
    response_publish = db.Column(db.Boolean, nullable=False)
    suggestion = db.Column(db.DateTime, nullable=True)

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

@app.route("/reservation", methods=["GET"])
def reservation():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        admin_tn = admin_table.query.filter_by(id=usr["id"]).first().tn
        reservation = reservation_table.query.filter_by(tn=admin_tn).all()
        accept = reservation_table.query.with_entities(reservation_table.accept_time, func.count(reservation_table.accept_time).label('count')).filter((reservation_table.tn==usr["tn"] )&(reservation_table.accept_time != None)).group_by(func.hour(reservation_table.accept_time), func.floor(func.minute(reservation_table.accept_time)/30)*10).order_by(reservation_table.accept_time).all()
        terminal = terminal_table.query.filter_by(tn=admin_tn).first()
        
        accept_list =  [[x[0],x[1]] for x in accept]
        
        for acc in accept_list:
            if(acc[0].minute >= 0 and acc[0].minute < 30):
                acc[0] = acc[0].replace(minute=0)
            else:
                acc[0] = acc[0].replace(minute=30)
        
        for acc in accept_list:
            print(acc[1])
            if(acc[1] < terminal.normal):
                acc.append('원활')
            elif(acc[1] <= terminal.normal):
                acc.append('보통')
            else:
                acc.append('혼잡')
        return render_template('reservation.html', reservations=reservation, accepts=accept_list)

@app.route("/reservation_popup", methods=["POST"])
def reservation_popup():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    id = request.form.get("id","")
    usr = session.get("info")
    reservation = reservation_table.query.filter((reservation_table.tn==usr["tn"] )&(reservation_table.accept_time != None)).order_by(reservation_table.accept_time).all()
    # accept = reservation_table.query.with_entities(reservation_table.accept_time, func.count(reservation_table.accept_time).label('count')).filter((reservation_table.tn==usr["tn"] )&(reservation_table.accept_time != None)).group_by(func.hour(reservation_table.accept_time), func.floor(func.minute(reservation_table.accept_time)/30)*10).order_by('count', reservation_table.accept_time).all()
    
    return render_template('reservation_popup.html', id=id)

app.run(host="0.0.0.0", port=8888)
