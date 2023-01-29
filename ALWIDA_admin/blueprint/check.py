import base64
from flask import Blueprint, request, session, render_template
from models import container_table, check_table, terminal_table, db

blue_check = Blueprint("check", __name__, url_prefix="/check")

def is_login():
    return session.get("info")

def alert(msg, loc=None):
    if loc:
        return f'<script>alert("{msg}");location.href="{loc}";</script>'
    else:
        return f'<script>alert("{msg}");location.href = document.referrer;</script>' 

def select_tn_func():
     return terminal_table.query.with_entities(terminal_table.tn).filter_by().all()

@blue_check.route("/", methods=["GET","POST"])
def check():
    if not is_login():
        return alert("로그인부터 해주세요!","/acc/signin")
    if(request.method=="GET"):
        usr = session.get("info")
        select_tn = request.args.get("select_tn",usr["tn"])
        check_wait = check_table.query.join(container_table, container_table.id==check_table.id)\
                                                            .with_entities(check_table.idx, check_table.id, check_table.request_time, check_table.img, check_table.result, container_table.container_num, container_table.tn)\
                                                            .filter((container_table.tn==select_tn) & ((check_table.result==0) | (check_table.result==1) | (check_table.result==2))).all()
                                                                       
        check_result = check_table.query.join(container_table, container_table.id==check_table.id)\
                                                            .with_entities(check_table.idx, check_table.id, check_table.request_time, check_table.img, check_table.result, container_table.container_num, container_table.tn)\
                                                            .filter((container_table.tn==select_tn) & ((check_table.result==3) | (check_table.result==4))).all()
        
        check_wait = [list(x) for x in check_wait]
        
        for data in check_wait:
            data[3] = base64.b64encode(data[3])
            data[3] = data[3].decode()
        
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