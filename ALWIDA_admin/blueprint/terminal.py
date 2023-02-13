from datetime import datetime
from flask import Blueprint, request, jsonify, session, render_template
from models import terminal_table, container_table, db

blue_terminal = Blueprint("terminal", __name__, url_prefix="/terminal")

def is_login():
    return session.get("info")

def select_tn_func():
     return terminal_table.query.with_entities(terminal_table.tn).filter_by().all()
 
def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");location.href = document.referrer;</script>'

@blue_terminal.route("/")
def terminal():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        terminal = terminal_table.query.filter_by(tn=select_tn).first()
        container = container_table.query.filter(container_table.tn==select_tn).all()
        
        return render_template('terminal.html', terminal=terminal, containers=container, select_tn=select_tn, tns=select_tn_func(), usr=usr, check=is_login())

@blue_terminal.route("/update", methods=["POST"])
def terminal_update():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
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

blue_container = Blueprint("container", __name__, url_prefix="/container")    

@blue_container.route("/update", methods=["POST"])
def container_update():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    try:
        container_num = request.form.get("container_num","")
        position = request.form.get("position","")
        scale = request.form.get("scale","")
        fm = request.form.get("fm","")
        tn = request.form.get("tn","")
                
        contaniner = container_table.query.filter_by(container_num=container_num).first()
        contaniner.position = position
        contaniner.scale = scale
        contaniner.fm = fm
        contaniner.tn = tn
        
        db.session.commit()
        return alert("완료!")
    except:
        return alert("에러발생")
    
@blue_container.route("/add", methods=["POST"])
def add():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    try:
        container_num = request.form.get("container_num","")
        position = request.form.get("position","")
        scale = request.form.get("scale","")
        fm = request.form.get("fm","")
        tn = request.form.get("tn","")
        
        new_container = container_table(container_num=container_num, id=None, tn=tn, scale=scale, fm=fm, position=position, contain_last_time=datetime.now(), in_out=None)
        db.session.add(new_container)
        db.session.commit()
        
        return alert("완료!")
    except:
        return alert("에러발생")