from flask import render_template, url_for, flash, redirect
from tripJournal import app
import requests
import datetime
import hashlib
import hmac
import base64
#from config import initialize_boto3
'''
import boto3
import botocore
import json

policy = '{ "Version": "2012-10-17", "Statement": [{"Effect": "Allow","Action": "*","Resource": "*"}}'


def initialize_boto3():
    # Inizializza STS utilizzando le tue credenziali federate
    sts_client = boto3.client('sts')
    response = sts_client.get_federation_token(
        Name='admin',
        Policy=json.dumps(policy),
        DurationSeconds=1000,
    )
    response = sts_client.get_session_token(DurationSeconds=3600, Policy='arn:aws:iam::597682427518:policy/allfortrip')
    response = sts_client.assume_role(
        RoleArn='arn:aws:iam::597682427518:role/LabRole',
        RoleSessionName='admin'#,
        #Policy='{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": ["*"], "Resource": "*"}]}',
        #DurationSeconds=3600
    )
    #
    # Ottieni le credenziali temporanee
    credentials = response['Credentials']
    access_key = credentials['AccessKeyId']
    secret_key = credentials['SecretAccessKey']
    session_token = credentials['SessionToken']
    region_name = 'us-east-1'
    account_id = 597682427518

    # Inizializza Boto3 con le credenziali temporanee
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region_name=region_name,
        account_id=account_id
    )

    return access_key, secret_key, session_token


@app.route("/")
@app.route("/home")
def home():
    #session = initialize_boto3()
    session = boto3.Session(aws_access_key_id=123123123, aws_secret_access_key=123123123, region_name='us-east-1')
    print(session)

    s3 = session.client('s3')
    #s3 = boto3.client('s3')

    my_bucket = s3.Bucket('prova123')
    print(my_bucket)
    #response = s3.list_buckets()
    #print(response)
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket='mybucket')
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response['Error']['Code']
        if error_code == '404':
            exists = False
    buckets = response['Buckets']
    for b in buckets:
        print(b['Name'])
  
    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object.key)
    return render_template('layout-standard.html', title="boto3")
'''

import os
import secrets
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

import requests


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
    # Utilizzo della funzione per ottenere il contenuto di un file
    bucket_name = "prova123"
    object_name = "pass0_fin.png"
    file_content = get_file_content_from_s3(bucket_name, object_name)
    # Stampa il contenuto del file
    if file_content:
        print("FINALMENTE")
    return render_template('homepage.html', title='Homepage', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')
