from flask import Flask
from flask import redirect, render_template, request, session
from random import randint
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


 
# mihin tämä tulee? postgresql+psycopg2://


 #hash_value = generate_password_hash(password)
    #sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
    #db.session.execute(sql, {"username":username,"password":hash_value})  
    #db.session.commit()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
     return redirect("/")
     # TODO: invalid username, nyt vaan mennöön alkuun
     # else:
     #  hash_value = user[0]
     #  if check_password_hash(hash_value,password):
        # TODO: correct username and password
    else:
        # TODO: invalid password
        # TODO: user check
     session["username"] = username
     return redirect("/island")
   
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register",methods=["POST"])
# tämä ei oikeasti laita vielä kantaan mitään vaan laittaa nimen session-käyttäjäksi jollei nimi ollut kannassa.
def register():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
     session["username"] = username
     return redirect("/island")
    else:  
     return redirect("/") 


@app.route("/island")
def island():
    return render_template("island.html")
