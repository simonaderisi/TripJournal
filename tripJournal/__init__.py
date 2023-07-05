from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from tripJournal.config import DB_PORT, DB_PWD, DB_USER, DB_HOST_READ, DB_HOST_WRITE, DB_NAME
import pymysql

app = Flask(__name__)

db = pymysql.connect(
    host=DB_HOST_WRITE,  # endpoint link
    port=DB_PORT,  # 3306
    user=DB_USER,  # admin
    password=DB_PWD,  # adminadmin
    db=DB_NAME,  # test

)

cursor = db.cursor()
create_posts = """
create table posts (id int, title varchar(200),author varchar(200),description varchar(20000),images varchar(2000), date datetime)

 """
cursor.execute(create_posts)
'''
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PWD}@{DB_HOST_WRITE}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_BINDS'] = {
    'scrittura': f'mysql://{DB_USER}:{DB_PWD}@{DB_HOST_WRITE}:{DB_PORT}/{DB_NAME}',
    'lettura': f'mysql://{DB_USER}:{DB_PWD}@{DB_HOST_READ}:{DB_PORT}/{DB_NAME}'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''
app.secret_key = "123123"
login_manager = LoginManager()
login_manager.init_app(app)

#db = SQLAlchemy(app)
#db.create_all()

from tripJournal import routes