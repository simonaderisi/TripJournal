from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from tripJournal.config import DB_PORT, DB_PWD, DB_USER, DB_HOST_READ, DB_HOST_WRITE, DB_NAME
import pymysql
from flask_cognito_lib import CognitoAuth
from flask_awscognito import AWSCognitoAuthentication

app = Flask(__name__)

db = pymysql.connect(
    host=DB_HOST_WRITE,  # endpoint link
    port=DB_PORT,  # 3306
    user=DB_USER,  # admin
    password=DB_PWD,  # adminadmin
    db=DB_NAME,  # test

)
'''
cursor = db.cursor()
create_posts = """
create table posts2 (id int, title varchar(200),author varchar(200),description text,images varchar(2000), date varchar(200))

 """
cursor.execute(create_posts)

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


app.config["AWS_DEFAULT_REGION"] = "us-east-1"
app.config["AWS_COGNITO_USER_POOL_ID"] = 'us-east-1_sLBBUGGVu'#'us-east-1_9ZNCQcUAe'
app.config["AWS_COGNITO_DOMAIN"] = 'travelers3.auth.us-east-1.amazoncognito.com'#'https://travelers2.auth.us-east-1.amazoncognito.com'
app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"] = '7fghsm2unr6ts1uh36l2hknmoe'#'3ca3ibapboc9mtmi51o990n4dj'
app.config["AWS_COGNITO_USER_POOL_CLIENT_SECRET"] = '2p90karq14bbe6836mvhb12jh4bmbkiaflc9rbbpjguudmve28k'#'1f03m549inpv2incbq16dv8u73evcg12uf3c21mrskhvohn7h38j'
app.config["AWS_COGNITO_REDIRECT_URL"] = "http://localhost:5000/callback"
app.config["AWS_COGNITO_LOGOUT_URL"] = "http://localhost:5000/"

aws_auth = AWSCognitoAuthentication(app)
'''

login_manager = LoginManager()
login_manager.init_app(app)
#db = SQLAlchemy(app)
#db.create_all()
'''
from tripJournal import routes