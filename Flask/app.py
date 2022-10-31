from calendar import c
import os
from flask import Flask, request, render_template, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy

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
    accept_time = db.Column(db.DateTIme, nullable=True)
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
    admin = admin_table.query.filter_by(id=usr["id"]).first()
    terminal = terminal_table.query.filter_by(tn=admin.tn).first()
    container = container_table.query.filter_by(tn=admin.tn).all()
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
        admin = admin_table.query.filter_by(id=usr["id"]).first()
        terminal = terminal_table.query.filter_by(tn=admin.tn).first()
        
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
    return '<script>alert("완료!");window.close(); </script>'

@app.route("/reservation", methods=["GET"])
def reservation():
    if not is_login():
        return alert("로그인부터 해주세요!","/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        admin = admin_table.query.filter_by(id=usr["id"]).first()
        reservation = reservation_table.query.filter_by(tn=admin.tn).all()
        
        return render_template('reservation.html', reservations=reservation)

app.run(host="0.0.0.0", port=8888)
