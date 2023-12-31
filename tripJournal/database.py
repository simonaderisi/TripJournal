import pymysql
from config import DB_PORT, DB_PWD, DB_USER, DB_NAME, DB_HOST_WRITE, DB_HOST_READ

conn = pymysql.connect(
    host=DB_HOST_WRITE,  # endpoint link
    port=DB_PORT,  # 3306
    user=DB_USER,  # admin
    password=DB_PWD,  # adminadmin
    db=DB_NAME,  # test

)


# Table Creation
cursor = conn.cursor()
create_posts = """
create table posts (id int, title varchar(200),author varchar(200),description varchar(20000),images varchar(2000), date datetime)

 """
cursor.execute(create_posts)

import mysql.connector
import config

def list_photos(cognito_username):
    "Select all the photos from the database"
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT object_key, description, labels, created_datetime
        FROM photo WHERE cognito_username = %s
        ORDER BY created_datetime desc""", (cognito_username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def add_photo(object_key, labels, description, cognito_username):
    "Add a photo to the database"
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""INSERT INTO photo (object_key, labels, description, cognito_username) VALUES
    (%s, %s, %s, %s);""", (object_key, labels, description, cognito_username))
    conn.commit()
    cursor.close()
    conn.close()

def delete_photo(object_key, cognito_username):
    "Delete a photo.  Users can only delete their photos!"
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM photo WHERE object_key = %s AND cognito_username = %s;""",
                   (object_key, cognito_username))
    conn.commit()
    cursor.close()
    conn.close()

def get_database_connection():
    "Build a database connection"
    conn = mysql.connector.connect(user=config.DATABASE_USER, password=config.DATABASE_PASSWORD,
                                   host=config.DATABASE_HOST,
                                   database=config.DATABASE_DB_NAME,
                                   use_pure=True) # see https://bugs.mysql.com/90585
    return conn
def insert_details(name, email, comment, gender):
    cur = conn.cursor()
    cur.execute("INSERT INTO Details (name,email,comment,gender) VALUES (%s,%s,%s,%s)", (name, email, comment, gender))
    conn.commit()


def get_details():
    cur = conn.cursor()
    cur.execute("SELECT *  FROM Details")
    details = cur.fetchall()
    return details