import os
import configparser
from flask import Flask
from models import init_db

from blueprint import signin, terminal, reservation, receipt, cash, check, user, chatting

config = configparser.ConfigParser()
config.read('/usr/src/app/config.ini')
dbuser = config['MariaDB']['user']
password = config['MariaDB']['password']
port = int(config['MariaDB']['port'])

db = {
    'user':dbuser,
    'password':password,
    'host':'mariadb',
    'port':port,
    'database':'alwida_db'
}

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8mb4&collation=utf8mb4_general_ci"

db = init_db(app)

app.register_blueprint(signin.blue_signin)
app.register_blueprint(terminal.blue_terminal)
app.register_blueprint(terminal.blue_container)
app.register_blueprint(reservation.blue_reservation)
app.register_blueprint(receipt.blue_receipt)
app.register_blueprint(cash.blue_cash)
app.register_blueprint(check.blue_check)
app.register_blueprint(user.blue_user)
app.register_blueprint(chatting.blue_chatting)

@app.after_request
def after_request(response):
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' https://code.jquery.com/jquery-3.5.1.js https://cdn.datatables.net/1.13.1/js/jquery.dataTables.min.js https://cdn.datatables.net/1.13.1/css/jquery.dataTables.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js; img-src http://localhost:8888/ http://ec2-13-209-21-247.ap-northeast-2.compute.amazonaws.com:8888/ data:;"
    response.headers["X-Frame-Options"] = "deny"
    return response

app.run(host="0.0.0.0", port=8888)
