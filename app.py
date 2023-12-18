import pickle
from flask import *
import numpy as np
import pandas as pd
import os
import phase1
import sqlite3 as sq
import time


#-- Database section using Sqlite for data handling
#-- Create function creates a connection file if doesn't exists
def create():
    from os.path import exists
    file_exists = exists("site_db")
    if file_exists:
        return
    db = sq.connect("site_db")
    cursor = db.cursor()
    print("creating database connection file!")
    time.sleep(1)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password BLOB) """)
    db.commit()

#-- Insert function add new record to database
def insert(name, email, password):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""INSERT INTO users (name, email, password) VALUES(?,?,?)""",(name,email,password))
    db.commit()
    db.close()

#-- basic data check, using email address to check if user already registred or not
def check_data(email):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT email FROM users WHERE email=(?)""",(email,))
    data = cursor.fetchall()
    if len(data) == 0:
        return True
#-- Basic data check, using email and password to check if user entred correct login info
def check_login_data(email, password):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT email FROM users WHERE email=(?)""",(email,))
    data = cursor.fetchall()
    print(data)
    if len(data) > 0:
        cursor.execute("""SELECT password FROM users WHERE password=(?)""",(password,))
        data = cursor.fetchall()
        print(data)
        if len(data) > 0:
            return True


app = Flask(__name__)
app.secret_key = 'super secret key'

f=open('args.txt')
args=f.readlines()
f.close()

@app.route('/')
def index():
    create()
    return render_template('index.html', args=args)

@app.route('/about')
def about():
    return render_template('about.html', args=args)

@app.route('/train')
def train():
    os.system("jupyter notebook crop-analysis-and-prediction.ipynb")
    return render_template('train.html', args=args)

@app.route('/parameters', methods=['GET'])
def parameters():
    return render_template('parameters.html', args=args)

@app.route('/team')
def team():
    return render_template('team.html', args=args) 

@app.route('/predict', methods=['GET'])
def predict():        
    District=request.args.get("District")
    N=request.args.get("N")
    P=request.args.get("P")
    K=request.args.get("K")
    temperature=request.args.get("temperature")
    humidity=request.args.get("humidity")
    ph=request.args.get("ph")
    rainfall=request.args.get("rainfall")
    #label=request.args.get("label")
    inputs=[N,P,K,temperature,humidity,ph,rainfall]
    result=phase1.predict(inputs)
    return render_template('predict.html', args=args, result=result)

#-- mapping for register page
@app.route("/register")
def register():
    return render_template("register.html", args=args)

#-- mapping for register_success page
#-- the registery page uses post method to send data to server
@app.route("/register_success", methods = ["POST", "GET"])
def register_success():
    #-- checking for method and runing data check before sending data to
    #-- Sqlite
    if request.method == "POST":
        email = request.form["email"]
        if check_data(email):
            email = request.form["email"]
            name = request.form["name"]
            password = request.form["password"]
            print(name)
            print(email)
            print(password)
            insert(name, email, password)
            return render_template("register_success.html", args=args)
        else:
            return render_template("register_fail.html", args=args)

#-- Registery fail page
@app.route("/register_faile")
def register_faile():
    return render_template("register_faile.html", args=args)
#-- Login page
@app.route("/login")
def login():
    return render_template("login.html", args=args)
@app.route("/logout")
def logout():
    return render_template("login.html", args=args)
@app.route("/test")
def test():
    return render_template("test.html", args=args)

#-- same as register_success page here we use POST method to send data
#-- back to server, so we can run data check for login proccess
@app.route("/login_success", methods = ["POST", "GET"])
def login_success():
    #-- using email and password
    #-- first check if even email exists if yes checks for password
    #-- we can expand system by creating auto send reset link to user Email
    #-- in a case that they forgot their password
    if request.method == "POST":
        email = request.form["email"]
        print(email)
        password = request.form["password"]
        print(password)
        if check_login_data(email, password):
            return render_template("login_success.html", args=args)
        else:
            return render_template("login_fail.html", args=args)


if __name__ == "__main__":
    ## Uncomment for flask only (no docker container)
    #app.run(debug=True)
    ## Comment out for flask only (no docker container)
    app.run(host="0.0.0.0", port=8080, debug=True)