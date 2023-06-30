from flask import render_template, url_for, flash, redirect
from tripJournal import app

@app.route("/")
@app.route("/home")
def home():
    return render_template('layout.html', title="chjfekhfe")