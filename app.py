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
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    usercheck = result.fetchone()
    if usercheck == None:
     session["infotext"] = "Username does not exist."
     return redirect("/")
     # TODO: hash
     #else:
     #  hash_value = user[0]
     #  if check_password_hash(hash_value,password):
    else:
     sql = "SELECT password FROM users WHERE username=:username"
     result = db.session.execute(sql, {"username":username})
     pwd = result.fetchone()[0]  
     if password == pwd:
      session["username"] = username
      sql = "SELECT id FROM users WHERE username=:username"
      result = db.session.execute(sql, {"username":username})
      userid = result.fetchone()[0]
      session["userid"] = userid
      session["infotext"] = "q"
      del session["infotext"]
      return redirect("/")
     else:
      session["infotext"] = "Password not correct."
      return redirect("/")

     
   
@app.route("/logout")
def logout():
    del session["username"]
    del session["userid"]
    session["infotext"] = "q"
    del session["infotext"]
    return redirect("/")

@app.route("/register",methods=["POST"])
#talleettaa vielä salasanat suoraan kantaan, pitää muuttaa HASH-tallennus
#ei mitään ehtoja username (paitsi pitää olla uniikki) ja password, esim. tyhjä käy. Pitää lisätä.
def register():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
     sql = "INSERT INTO users (username, password, role, visible) VALUES (:username, :password, 'user', 1)"
     db.session.execute(sql, {"username":username, "password":password})
     db.session.commit()
     session["infotext"] = "q"
     del session["infotext"]   
     return redirect("/")
    else:
     session["infotext"] = "Username taken"
     return redirect("/")

@app.route("/user/<int:id>")
def page(id):
    #Kirjoittamalla html-osoitteeksi käyttäjän jota ei ole ohjelma kaatuu (mutta ei kai väliä?)
    userid = id
    sql = "SELECT username FROM users WHERE id=:userid"
    result = db.session.execute(sql, {"userid":userid})
    user = result.fetchone()[0]
    sql = "SELECT islandname FROM islands WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    islands = result.fetchall()
    return render_template("user.html", user=user, islands=islands, userid=userid)


@app.route("/createisland")
def createisland():
    userid = session["userid"]
    sql = "SELECT islandname FROM islands WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    islands = result.fetchall()
    return render_template("createisland.html", islands=islands)
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
     return redirect("/createisland")
    else:
     return "You already have an island with this name."
     #TODO: ohjaus jonnekin

@app.route("/editcharacters")
def editcharacters():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
     sql = "SELECT personalityname FROM personalities WHERE visible=1"
     result = db.session.execute(sql)
     personalities = result.fetchall()
     sql = "SELECT speciesname FROM species WHERE visible=1"
     result = db.session.execute(sql)
     species = result.fetchall()
     sql = "SELECT outfitname FROM outfits WHERE visible=1"
     result = db.session.execute(sql)
     outfits = result.fetchall()
     return render_template("editcharacters.html", personalities=personalities, species=species, outfits=outfits)
    else:
     return "You don't have permission."

@app.route("/personalities")
def personalities():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
     sql = "SELECT personalityname FROM personalities WHERE visible=1"
     result = db.session.execute(sql)
     personalities = result.fetchall()
     return render_template("personalities.html", personalities=personalities)
    else:
     return "You don't have permission."

@app.route("/addpersonality",methods=["POST"])
def addpersonality():
    personality = request.form["personality"]
    sql = "SELECT personalityname FROM personalities WHERE personalityname=:personality"
    result = db.session.execute(sql, {"personality":personality})
    checkpersonality = result.fetchone()
    if checkpersonality == None:
     sql = "INSERT INTO personalities (personalityname, visible) VALUES (:personality, 1)"
     db.session.execute(sql, {"personality":personality})
     db.session.commit()   
     return redirect("/personalities")
    else:
     return "A personality with this name already exists."

@app.route("/editpersonality", methods=["POST"])
def editpersonality():
    personality = request.form["old"]
    new = request.form["new"]
    sql = "SELECT personalityname FROM personalities WHERE personalityname=:new AND visible=1"
    result = db.session.execute(sql, {"new":new})
    checkpersonality = result.fetchone()
    if checkpersonality == None:
     sql = "SELECT id FROM personalities WHERE personalityname=:personality"
     result = db.session.execute(sql, {"personality":personality})
     id = result.fetchone()[0]
     sql = "UPDATE personalities SET personalityname=:new WHERE id=:id"
     db.session.execute(sql, {"new":new, "id":id})
     db.session.commit()
     return redirect("/personalities")
    else:
     return "A personality with this name already exists."

@app.route("/species")
def species():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
     sql = "SELECT speciesname FROM species WHERE visible=1"
     result = db.session.execute(sql)
     species = result.fetchall()
     return render_template("species.html", species=species)
    else:
     return "You don't have permission."

@app.route("/addspecies",methods=["POST"])
def addspecies():
    species = request.form["species"]
    sql = "SELECT speciesname FROM species WHERE speciesname=:species"
    result = db.session.execute(sql, {"species":species})
    checkspecies = result.fetchone()
    if checkspecies == None:
     sql = "INSERT INTO species (speciesname, visible) VALUES (:species, 1)"
     db.session.execute(sql, {"species":species})
     db.session.commit()   
     return redirect("/species")
    else:
     return "A species with this name already exists."

@app.route("/editspecies", methods=["POST"])
def editspecies():
    species = request.form["old"]
    new = request.form["new"]
    sql = "SELECT speciesname FROM species WHERE speciesname=:new AND visible=1"
    result = db.session.execute(sql, {"new":new})
    checkspecies = result.fetchone()
    if checkspecies == None:
     sql = "SELECT id FROM species WHERE speciesname=:species"
     result = db.session.execute(sql, {"species":species})
     id = result.fetchone()[0]
     sql = "UPDATE species SET speciesname=:new WHERE id=:id"
     db.session.execute(sql, {"new":new, "id":id})
     db.session.commit()
     return redirect("/species")
    else:
     return "A species with this name already exists."

@app.route("/outfits")
def outfits():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
     sql = "SELECT outfitname FROM outfits WHERE visible=1"
     result = db.session.execute(sql)
     outfits = result.fetchall()
     return render_template("outfits.html", outfits=outfits)
    else:
     return "You don't have permission."

@app.route("/addoutfit",methods=["POST"])
def addoutfit():
    outfit = request.form["outfit"]
    sql = "SELECT outfitname FROM outfits WHERE outfitname=:outfit"
    result = db.session.execute(sql, {"outfit":outfit})
    checkoutfit = result.fetchone()
    if checkoutfit == None:
     sql = "INSERT INTO outfits (outfitname, visible) VALUES (:outfit, 1)"
     db.session.execute(sql, {"outfit":outfit})
     db.session.commit()   
     return redirect("/outfits")
    else:
     return "An outfit with this name already exists."

@app.route("/editoutfit", methods=["POST"])
def editoutfit():
    outfit = request.form["old"]
    new = request.form["new"]
    sql = "SELECT outfitname FROM outfits WHERE outfitname=:new AND visible=1"
    result = db.session.execute(sql, {"new":new})
    checkoutfit = result.fetchone()
    if checkoutfit == None:
     sql = "SELECT id FROM outfits WHERE outfitname=:outfit"
     result = db.session.execute(sql, {"outfit":outfit})
     id = result.fetchone()[0]
     sql = "UPDATE outfits SET outfitname=:new WHERE id=:id"
     db.session.execute(sql, {"new":new, "id":id})
     db.session.commit()
     return redirect("/outfits")
    else:
     return "An outfit with this name already exists."+new +outfit


@app.route("/island")
def island():
    return render_template("island.html")
