from tripJournal import app, db
from flask import render_template, url_for, flash, redirect, request, abort
from sqlalchemy import desc
from tripJournal.model import Post
import os
import base64
'''
from PIL import Image
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
'''

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


import boto3

def upload_file_to_s3(file, bucket, filename):
    session = boto3.Session()
    s3 = session.client("s3")
    s3.upload_fileobj(file, bucket, filename)


def get_file_content_from_s3(bucket_name, object_name):
    # Crea un oggetto sessione Boto3
    session = boto3.Session()

    # Ottieni l'oggetto cliente per Amazon S3
    s3_client = session.client("s3")

    # Recupera il contenuto del file da S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        file_content = response["Body"].read().decode("utf-8")
        return file_content
    except Exception as e:
        print(f"Si è verificato un errore durante il recupero del file da S3: {e}")
        return None

'''
@app.route("/")
@app.route("/homepage")
def home():
    posts = Post.query.with_bind('lettura').order_by(desc(Post.date)).all()
    return render_template('homepage.html', title='Homepage', posts=posts)


@app.route("/callback.html")
def callback():
    return render_template("callback.html")


@app.route("/about")
def about():
    return render_template('about.html', title='About')
'''

from tripJournal.config import S3_BUCKET


@app.route('/create_post', methods=['GET', 'POST'])
#@login_required
def create_post():
    if request.method == 'POST':
        post = Post(
            title=request.form.get('title'),
            author=request.form.get('author'),
            description=request.form.get('description'),
            images=[],
            date=datetime.now()
        )
        p_id = post.id
        for i, image in enumerate(request.files.getlist('images')):
            filename = str(p_id) + str(i) + image.filename.split('.')[1]
            upload_file_to_s3(image, S3_BUCKET, filename)
            file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
            post.images.append(file_url)
        db.session.add(post)
        db.session.commit()
        flash("Posted!")
        return redirect(url_for('homepage'))
    # Se il metodo HTTP non è POST, restituisci la pagina di creazione del post
    return render_template('create_post.html')


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete_post(id):
    to_delete = Post.query.get(id)
    db.session.delete(to_delete)
    db.session.commit()
    flash("Book is deleted")
    return redirect(url_for('homepage'))


import random

from tripJournal import app, login_manager
from flask import render_template, url_for, flash, redirect, request, abort

'''
from PIL import Image
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
'''

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

import boto3


def get_file_content_from_s3(bucket_name, object_name):
    # Crea un oggetto sessione Boto3
    session = boto3.Session()

    # Ottieni l'oggetto cliente per Amazon S3
    s3_client = session.client("s3")

    # Recupera il contenuto del file da S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        file_content = response["Body"].read().decode("utf-8")
        return file_content
    except Exception as e:
        print(f"Si è verificato un errore durante il recupero del file da S3: {e}")
        return None

''' 
@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template('homepage.html', title='Homepage', posts=posts)


@app.route("/callback.html")
def callback():
    return render_template("callback.html")

'''
@app.route("/about")
def about():
    return render_template('about.html', title='About')


COGNITO_POOL_ID = 'us-east-1_9ZNCQcUAe'
COGNITO_CLIENT_ID = '3ca3ibapboc9mtmi51o990n4dj'
COGNITO_CLIENT_SECRET = '1f03m549inpv2incbq16dv8u73evcg12uf3c21mrskhvohn7h38j'
COGNITO_DOMAIN = 'travelers2.auth.us-east-1.amazoncognito.com'
BASE_URL = 'http://localhost:5000'
AWS_REGION = 'us-east-1'
import sys
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import boto3
from flask import Flask, render_template_string, session, redirect, request, url_for
import flask_login
#from jose import jwt


### load and cache cognito JSON Web Key (JWK)
# https://docs.aws.amazon.com/cognito/latest/developerguide/amazoncognito-user-pools-using-tokens-with-identity-providers.html
JWKS_URL = ("https://cognito-idp.us-east-1.amazonaws.com/us-east-1_9ZNCQcUAe/.well-known/jwks.json")
JWKS = requests.get(JWKS_URL).json()["keys"]
print(JWKS)


class User(flask_login.UserMixin):
    """Standard flask_login UserMixin"""
    pass


@login_manager.user_loader
def user_loader(session_token):
    """Populate user object, check expiry"""
    if "expires" not in session:
        return None
    expires = datetime.utcfromtimestamp(session['expires'])
    print('expires', expires)
    expires_seconds = (expires - datetime.utcnow()).total_seconds()
    if expires_seconds < 0:
        return None
    user = User()
    user.id = session_token
    user.nickname = session['nickname']
    print(user)
    return user


@app.route("/")
def home():
    """Homepage route"""
    return render_template_string("""
 {% extends "layout.html" %}
 {% block content %}
 {% if current_user.is_authenticated %}
 <h1> DENTRO </h1>
 {% else %}
 Click <em>login in / sign up<em> to access this site.
 {% endif %}
 {% endblock %}""")


@app.route("/login")
def login():
    """Login route"""
    # http://docs.aws.amazon.com/cognito/latest/developerguide/loginendpoint.html
    session['csrf_state'] = os.urandom(8).hex()
    print('session:', session)
    cognito_login = ("https://%s/"
                     "login?response_type=code&client_id=%s"
                     "&state=%s"
                     "&redirect_uri=%s/callback" %
                     (COGNITO_DOMAIN, COGNITO_CLIENT_ID,
                      session['csrf_state'], BASE_URL))
    print(cognito_login)
    return redirect(cognito_login)


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
    """Exchange the 'code' for Cognito tokens"""
    print('ciao')
    #http://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
    csrf_state = request.args.get('state')
    code = request.args.get('code')
    request_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Authorization':  'Basic ' + base64.b64encode(COGNITO_CLIENT_ID + ':' + COGNITO_CLIENT_SECRET)}
    request_parameters = {'grant_type': 'authorization_code',
                          'client_id': COGNITO_CLIENT_ID,
                          'code': code,
                          "redirect_uri" : BASE_URL + "/callback"}
    response = requests.post("https://%s/oauth2/token" % COGNITO_DOMAIN,
                             params=request_headers,
                             data=request_parameters,
                             auth=HTTPBasicAuth(COGNITO_CLIENT_ID,
                                                COGNITO_CLIENT_SECRET))

    # the response:
    # http://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html
    if response.status_code == requests.codes.ok and csrf_state == session['csrf_state']:
        verify(response.json()["access_token"])
        id_token = verify(response.json()["id_token"], response.json()["access_token"])

        user = User()
        user.id = id_token["cognito:username"]
        session['nickname'] = id_token["nickname"]
        session['expires'] = id_token["exp"]
        session['refresh_token'] = response.json()["refresh_token"]
        flask_login.login_user(user, remember=True)
        return redirect(url_for("home"))

    return render_template_string("""
        {% extends "main.html" %}
        {% block content %}
            <p>Something went wrong</p>
        {% endblock %}""")


def verify(token, access_token=None):
    """Verify a cognito JWT"""
    # get the key id from the header, locate it in the cognito keys
    # and verify the key
    print("problema?")
    header = jwt.get_unverified_header(token)
    key = [k for k in JWKS if k["kid"] == header['kid']][0]
    id_token = jwt.decode(token, key, audience=COGNITO_CLIENT_ID,
                          access_token=access_token)
    return id_token
