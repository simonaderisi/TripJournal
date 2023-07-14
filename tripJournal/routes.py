from tripJournal import app, aws_auth, login_manager
import pymysql
from tripJournal.config import *
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import requests
from flask import Flask, render_template_string, session, redirect, request, url_for, flash, render_template
import flask_login
import boto3

def upload_file_to_s3(file, bucket, filename):
    session = boto3.Session()
    s3 = session.client("s3")
    try:
        s3.upload_fileobj(file, bucket, filename)
    except Exception as e:
        print(f"Si è verificato un errore durante l'upload dell'immagine su s3: {e}")


def get_file_content_from_s3(bucket_name, object_name):
    # Crea un oggetto sessione Boto3
    session = boto3.Session()

    # Ottieni l'oggetto cliente per Amazon S3
    s3_client = session.client("s3")

    # Recupera il contenuto del file da S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        file_content = response["Body"].read()
        return file_content
    except Exception as e:
        print(f"Si è verificato un errore durante il recupero del file da S3: {e}")
        return None


def get_database_connection():
    "Build a database connection"
    conn = pymysql.connect(user=DB_USER, password=DB_PWD,
                                   host=DB_HOST_WRITE,
                                   database=DB_NAME
                                   ) # see https://bugs.mysql.com/90585
    return conn


ID_POST = 0

@app.route('/create_post', methods=['GET', 'POST'])
#@aws_auth.login_required
def create_post():
    global ID_POST
    if request.method == 'POST':
        images = []
        print(current_user)
        for i, image in enumerate(request.files.getlist('images[]')):
            filename = str(ID_POST) + '_' + str(i) + '_' + image.filename
            print(filename)
            upload_file_to_s3(image, S3_BUCKET, filename)
            file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
            images.append(file_url)
        images = ','.join(images)
        conn = get_database_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        print(type(ID_POST))
        cursor.execute("""INSERT INTO posts (id, title, author, description, images, map, datte) 
        VALUES (%s, %s, %s, %s, %s, %s);""", (ID_POST, request.form.get("title"), request.form.get("author"),
                                              request.form.get("content"), images, request.form.get('map'), now))
        conn.commit()
        cursor.close()
        conn.close()
        ID_POST += 1
        flash("Posted!")
        return redirect(url_for('home'))
    # Se il metodo HTTP non è POST, restituisci la pagina di creazione del post
    return render_template('create_post.html')



def get_posts():
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT * from posts ORDER BY datte""")
    posts = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return posts


@app.route("/about")
def about():
    return render_template('about.html', title='About')



class User(flask_login.UserMixin):
    """Standard flask_login UserMixin"""
    pass


@login_manager.user_loader
def user_loader(session_token):
    """Populate user object, check expiry"""
    #if "expires" not in session:
    #    return None
    #expires = datetime.utcfromtimestamp(session['expires'])
    #print('expires', expires)
    #expires_seconds = (expires - datetime.utcnow()).total_seconds()
    #if expires_seconds < 0:
    #    return None
    user = User()
    user.id = session_token
    user.nickname = session['nickname']
    print(user)
    return user


@app.route("/")
def home():
    """Homepage route"""
    return render_template('homepage.html', title='HOME')


@app.route("/login")
def login():
    """Login route"""
    return redirect(aws_auth.get_sign_in_url())


@app.route("/logout")
def logout():
    flask_login.logout_user()
    cognito_logout = ("https://%s/"
                      "logout?response_type=code&client_id=%s"
                      "&logout_uri=%s/" %
                      (COGNITO_DOMAIN, COGNITO_CLIENT_ID, BASE_URL))
    return redirect(cognito_logout)


@app.route("/callback")
def callback():
    """get Cognito tokens"""
    access_token = aws_auth.get_access_token(request.args)
    request_headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(f"https://{COGNITO_DOMAIN}/oauth2/userInfo",
                             headers=request_headers)
    r = response.json()
    user = User()
    user.id = r["username"]
    session['nickname'] = r["nickname"]
    #session['expires'] = id_token["exp"]
    #session['refresh_token'] = response.json()["refresh_token"]
    flask_login.login_user(user, remember=True)
    return redirect(url_for('home'))
