from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return db

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
    car_num = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    check_num = db.Column(db.String(5), nullable=True)
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
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    container_num = db.Column(db.String(30), nullable=False)
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
    
    def obj_to_dict(self):
        return {
            "idx":self.idx,
            "id":self.id,
            "message":self.message,
            "time":self.time,
            "sender":self.sender
        }
    