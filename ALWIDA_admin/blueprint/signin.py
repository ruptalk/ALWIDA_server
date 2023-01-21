import uuid
from flask import Blueprint, request, session, render_template
from models import admin_table, terminal_table, db

blue_signin = Blueprint("acc", __name__, url_prefix="/acc")

def is_login():
    return session.get("info")

def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");location.href = document.referrer;</script>'

@blue_signin.route("/signin", methods=['GET','POST'])
def signin():
    if is_login():
        return alert("이미 로그인하셨습니다!","/terminal")
    if(request.method == 'GET'):
        return render_template('signin.html',check=is_login())
    elif(request.method == 'POST'):
        id = request.form.get("id","")
        pw = request.form.get("pw","")
        
        usr = admin_table.query.filter_by(id=id, pw=pw).first()
        if(not hasattr(usr, 'id')):
            return alert("Check userid or userpw")
        session["info"] = usr.to_json()
        return alert("로그인 성공!","/terminal")

@blue_signin.route("/signup", methods=["GET","POST"])
def signup():
    if is_login():
        return alert("이미 로그인하셨습니다!","/terminal")
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
            
            return alert("완료!","/acc/signin")
        except:
            return alert("에러!")

@blue_signin.route("/signout")
def signout():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    del session["info"]
    return alert("로그아웃!","/acc/signin")