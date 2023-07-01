from tripJournal import app
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


@app.route("/")
@app.route("/homepage")
def home():
    return render_template('homepage.html', title='Homepage', posts=posts)


@app.route("/callback.html")
def callback():
    return render_template("callback.html")


@app.route("/about")
def about():
    return render_template('about.html', title='About')
