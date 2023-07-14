from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from tripJournal.config import *
import pymysql
from flask_awscognito import AWSCognitoAuthentication

app = Flask(__name__)

db = pymysql.connect(
    host=DB_HOST_WRITE,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PWD,
    db=DB_NAME,
)

'''
cursor = db.cursor()
create_posts = """
create table posts2 (id int, title varchar(200),author varchar(200),description text,images varchar(2000), map varchar(600), date varchar(200))

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


app.config["AWS_DEFAULT_REGION"] = AWS_REGION
app.config["AWS_COGNITO_USER_POOL_ID"] = COGNITO_POOL_ID
app.config["AWS_COGNITO_DOMAIN"] = COGNITO_DOMAIN
app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"] = COGNITO_CLIENT_ID
app.config["AWS_COGNITO_USER_POOL_CLIENT_SECRET"] = COGNITO_CLIENT_SECRET
app.config["AWS_COGNITO_REDIRECT_URL"] = BASE_URL + '/callback'
app.config["AWS_COGNITO_LOGOUT_URL"] = BASE_URL

aws_auth = AWSCognitoAuthentication(app)
'''

login_manager = LoginManager()
login_manager.init_app(app)
#db = SQLAlchemy(app)
#db.create_all()
'''
from tripJournal import routes