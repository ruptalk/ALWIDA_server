import os
import configparser
from flask import Flask
from models import init_db

from msg import msg
from signup import signup
from signin import signin
from destination import destination
from main import main
from receipt import receipt
from check import check

config = configparser.ConfigParser()
config.read('/usr/src/app/config.ini')
user = config['MariaDB']['user']
password = config['MariaDB']['password']
port = int(config['MariaDB']['port'])

db = {
    'user':user,
    'password':password,
    'host':'mariadb',
    'port':port,
    'database':'alwida_db'
}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.urandom(32)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8mb4&collation=utf8mb4_general_ci"

db = init_db(app)

app.register_blueprint(main.blue_main)
app.register_blueprint(signin.blue_signin)
app.register_blueprint(signup.blue_signup)
app.register_blueprint(msg.blue_msg)
app.register_blueprint(destination.blue_dest)
app.register_blueprint(receipt.blue_receipt)
app.register_blueprint(check.blue_check)


app.run(host="0.0.0.0", port=5000)
