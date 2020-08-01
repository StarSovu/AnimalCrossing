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
     # TODO: invalid username, nyt vaan menään alkuun
     # else:
     #  hash_value = user[0]
     #  if check_password_hash(hash_value,password):
        # TODO: correct username and password
    else:
        # TODO: invalid password
        # TODO: user check
     session["username"] = username
     sql = "SELECT id FROM users WHERE username=:username"
     result = db.session.execute(sql, {"username":username})
     userid = result.fetchone()[0]
     session["userid"] = userid
     return redirect("/")
   
@app.route("/logout")
def logout():
    del session["username"]
    del session["userid"]
    return redirect("/")

@app.route("/register",methods=["POST"])
#talleettaa vielä salasanat suoraan kantaan, pitää muuttaa HASH-tallennus
def register():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
     sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, 'user')"
     db.session.execute(sql, {"username":username, "password":password})
     db.session.commit()   
     return redirect("/")
    else:
     return "Username taken"
     #TODO: ohjaus jonnekin

@app.route("/user/<string:user>")
def page(user):
    #Kirjoittamalla html-osoitteeksi käyttäjän jota ei ole ohjelma kaatuu (mutta ei kai väliä?)
    username = user
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    userid = result.fetchone()[0]
    sql = "SELECT islandname FROM islands WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    islands = result.fetchall()
    return render_template("user.html", user=user, islands=islands, userid=userid)


@app.route("/createisland")
def createisland():
   return render_template("createisland.html")
    # TODO

@app.route("/addisland",methods=["POST"])
def addisland():
    islandname = request.form["islandname"]
    userid = session["userid"]
    sql = "SELECT islandname FROM islands WHERE islandname=:islandname AND userid=:userid"
    result = db.session.execute(sql, {"islandname":islandname, "userid":userid})
    island = result.fetchone()
    if island == None:
     sql = "INSERT INTO islands (islandname, userid, visible) VALUES (:islandname, :userid, 1)"
     db.session.execute(sql, {"islandname":islandname, "userid":userid})
     db.session.commit()
     return redirect("/")
    else:
     return "You already have an island with this name."
     #TODO: ohjaus jonnekin


@app.route("/island")
def island():
    return render_template("island.html")
