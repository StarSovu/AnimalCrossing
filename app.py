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
    else:
     sql = "SELECT password FROM users WHERE username=:username"
     result = db.session.execute(sql, {"username":username})
     hash_value = result.fetchone()[0] 
     if check_password_hash(hash_value,password):
      session["username"] = username
      sql = "SELECT id FROM users WHERE username=:username"
      result = db.session.execute(sql, {"username":username})
      userid = result.fetchone()[0]
      session["userid"] = userid
      session["infotext"] = "q"
      del session["infotext"]
      sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
      result = db.session.execute(sql, {"userid":userid})
      role = result.fetchone()[0]
      if role == "admin":
       return redirect("/admin")
      else:
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
#ei mitään ehtoja username (paitsi pitää olla uniikki) ja password, esim. tyhjä käy. Pitää lisätä.
def register():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
     hash_value = generate_password_hash(password)
     sql = "INSERT INTO users (username, password, role, visible) VALUES (:username, :password, 'user', 1)"
     db.session.execute(sql, {"username":username, "password":hash_value})
     #db.session.execute(sql, {"username":username, "password":password})
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
    sql = "SELECT islandname, id FROM islands WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    islands = result.fetchall()
    return render_template("user.html", user=user, islands=islands, userid=userid)


@app.route("/createisland")
def createisland():
    userid = session["userid"]
    sql = "SELECT islandname, id FROM islands WHERE userid=:userid"
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


@app.route("/island/<int:id>")
def island(id):
    islandid = id
    sql = "SELECT islandname FROM islands WHERE id=:islandid AND visible=1"
    result = db.session.execute(sql, {"islandid":islandid})
    islandname = result.fetchone()[0]
    sql = "SELECT userid FROM islands WHERE id=:islandid AND visible=1"
    result = db.session.execute(sql, {"islandid":islandid})
    userid = result.fetchone()[0]
    sql = "SELECT username FROM users WHERE id=:userid"
    result = db.session.execute(sql, {"userid":userid})
    username = result.fetchone()[0]
    sql = "SELECT characterid, charactername, outfitname FROM characteronisland, characters, outfits WHERE islandid=:islandid AND characteronisland.visible=1 AND characters.id=characterid AND outfits.id=characteronisland.outfitid "
    result = db. session. execute(sql, {"islandid":islandid})
    characters = result.fetchall()
    return render_template("island.html", islandid=islandid, islandname=islandname, userid=userid, username=username, characters=characters)

@app.route("/renameisland",methods=["POST"])
def renameisland():
    islandid = request.form["id"]
    new = request.form["new"]
    userid = session["userid"]
    sql = "SELECT islandname FROM islands WHERE islandname=:new AND userid=:userid"
    result = db.session.execute(sql, {"new":new, "userid":userid})
    island = result.fetchone()
    if island == None:
     sql = "UPDATE islands SET islandname=:new WHERE id=:islandid"
     db.session.execute(sql, {"new":new, "islandid":islandid})
     db.session.commit()
     return redirect("/createisland")
    else:
     return "You already have an island with this name."
     #TODO: ohjaus jonnekin

@app.route("/island/<int:id>/addcharacter")
def islandaddcharacter(id):
    islandid = id
    userid = session["userid"] 
    sql = "SELECT userid FROM islands WHERE id=:islandid AND visible=1"
    result = db.session.execute(sql, {"islandid":islandid})
    checkuserid = result.fetchone()[0]
    if userid == checkuserid:
     sql = "SELECT islandname FROM islands WHERE id=:islandid"
     result = db.session.execute(sql, {"islandid":islandid})
     islandname = result.fetchone()[0]
     sql = "SELECT charactername FROM characters WHERE visible = 1"
     result = db.session.execute(sql)
     characters = result.fetchall()
     sql = "SELECT charactername FROM characteronisland, characters WHERE islandid=:islandid AND characteronisland.visible=1 AND characters.id=characterid"
     result = db. session. execute(sql, {"islandid":islandid})
     currentcharacters = result.fetchall()
     return render_template("addcharactertoisland.html", islandid=islandid, islandname=islandname, characters=characters, currentcharacters=currentcharacters)
    else:
     return "You don't have permission."

@app.route("/addcharactertoisland", methods=["POST"])
def addcharactertoisland():
    islandid = request.form["id"]
    character = request.form["character"]
    sql = "SELECT id FROM characters WHERE charactername=:character"
    result = db.session.execute(sql, {"character":character})
    characterid = result.fetchone()[0]
    sql = "SELECT characterid FROM characteronisland WHERE characterid=:characterid AND islandid=:islandid"
    result = db.session.execute(sql, {"characterid":characterid, "islandid":islandid})
    check = result.fetchone()
    if check == None:
     sql = "SELECT outfitid FROM characters WHERE id=:characterid"
     result = db.session.execute(sql, {"characterid":characterid})
     outfitid = result.fetchone()[0]
     sql = "INSERT INTO characteronisland (islandid, characterid, outfitid, visible) VALUES (:islandid, :characterid, :outfitid, 1)"
     db.session.execute(sql, {"islandid":islandid, "characterid":characterid, "outfitid":outfitid})
     db.session.commit()
     return redirect("/createisland")
    else:
     sql = "SELECT visible FROM characteronisland WHERE characterid=:characterid AND islandid=:islandid"
     result = db.session.execute(sql, {"characterid":characterid, "islandid":islandid})
     visible = result.fetchone()[0]
     if visible == 0:
      sql = "UPDATE characteronisland SET visible=1 WHERE characterid=:characterid AND islandid=:islandid"
      db.session.execute(sql, {"characterid":characterid, "islandid":islandid})
      db.session.commit()
      return redirect("/createisland")
     else:
      return "This character is already on this island."

@app.route("/island/<int:id>/changecharacteroutfit")
def islandchangecharacteroutfit(id):
    islandid = id
    userid = session["userid"] 
    sql = "SELECT userid FROM islands WHERE id=:islandid AND visible=1"
    result = db.session.execute(sql, {"islandid":islandid})
    checkuserid = result.fetchone()[0]
    if userid == checkuserid:
     sql = "SELECT islandname FROM islands WHERE id=:islandid AND visible=1"
     result = db.session.execute(sql, {"islandid":islandid})
     islandname = result.fetchone()[0]
     sql = "SELECT charactername, outfitname FROM characteronisland, characters, outfits WHERE islandid=:islandid AND characteronisland.visible=1 AND characters.id=characterid AND outfits.id=characteronisland.outfitid "
     result = db.session.execute(sql, {"islandid":islandid})
     characters = result.fetchall()
     sql = "SELECT outfitname FROM outfits WHERE visible=1"
     result = db.session.execute(sql)
     outfits = result.fetchall()
     return render_template("changecharacteroutfitonisland.html", islandid=islandid, islandname=islandname, characters=characters, outfits=outfits)
    else:
     return "You don't have permission."

@app.route("/changecharacteroutfitonisland", methods=["POST"])
def changecharacteroutfitonisland():
    islandid = request.form["id"]
    character = request.form["character"]
    outfit = request.form["outfit"]
    sql = "SELECT id FROM characters WHERE charactername=:character"
    result = db.session.execute(sql, {"character":character})
    characterid = result.fetchone()[0]
    sql = "SELECT id FROM outfits WHERE outfitname=:outfit"
    result = db.session.execute(sql, {"outfit":outfit})
    outfitid = result.fetchone()[0]
    sql = "UPDATE characteronisland SET outfitid=:outfitid WHERE characterid=:characterid AND islandid=:islandid"
    db.session.execute(sql, {"outfitid":outfitid, "characterid":characterid, "islandid":islandid})
    db.session.commit()
    return redirect("/createisland")

@app.route("/island/<int:id>/removecharacter")
def islandremovecharacter(id):
    islandid = id
    userid = session["userid"] 
    sql = "SELECT userid FROM islands WHERE id=:islandid AND visible=1"
    result = db.session.execute(sql, {"islandid":islandid})
    checkuserid = result.fetchone()[0]
    if userid == checkuserid:
     sql = "SELECT islandname FROM islands WHERE id=:islandid AND visible=1"
     result = db.session.execute(sql, {"islandid":islandid})
     islandname = result.fetchone()[0]
     sql = "SELECT charactername FROM characteronisland, characters WHERE islandid=:islandid AND characteronisland.visible=1 AND characters.id=characterid"
     result = db.session.execute(sql, {"islandid":islandid})
     characters = result.fetchall()
     return render_template("removecharacterfromisland.html", islandid=islandid, islandname=islandname, characters=characters)
    else:
     return "You don't have permission."

@app.route("/removecharacterfromisland", methods=["POST"])
def removecharacterfromisland():
    islandid = request.form["id"]
    character = request.form["character"]
    sql = "SELECT id FROM characters WHERE charactername=:character"
    result = db.session.execute(sql, {"character":character})
    characterid = result.fetchone()[0]
    sql = "UPDATE characteronisland SET visible=0 WHERE characterid=:characterid AND islandid=:islandid"
    db.session.execute(sql, {"characterid":characterid, "islandid":islandid})
    db.session.commit()
    return redirect("/createisland")

@app.route("/admin")
def admin():
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
     sql = "SELECT charactername, id FROM characters WHERE visible=1"
     result = db.session.execute(sql)
     characters = result.fetchall()
     return render_template("admin.html", personalities=personalities, species=species, outfits=outfits, characters=characters)
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
     return "An outfit with this name already exists."

@app.route("/characterlist")
def characterlist():
    sql = "SELECT charactername, id FROM characters WHERE visible=1"
    result = db.session.execute(sql)
    characters = result.fetchall()
    return render_template("characterlist.html", characters=characters)

@app.route("/character/<int:id>")
def character(id):
    characterid = id
    sql = "SELECT charactername FROM characters WHERE id=:characterid"
    result = db.session.execute(sql, {"characterid":characterid})
    character = result.fetchone()[0]
    #personality
    sql = "SELECT personalityid FROM characters WHERE id=:characterid"
    result = db.session.execute(sql, {"characterid":characterid})
    personalityid = result.fetchone()[0]
    sql = "SELECT personalityname FROM personalities WHERE id=:personalityid"
    result = db.session.execute(sql, {"personalityid":personalityid})
    personality = result.fetchone()[0]
    #species
    sql = "SELECT speciesid FROM characters WHERE id=:characterid"
    result = db.session.execute(sql, {"characterid":characterid})
    speciesid = result.fetchone()[0]
    sql = "SELECT speciesname FROM species WHERE id=:speciesid"
    result = db.session.execute(sql, {"speciesid":speciesid})
    species = result.fetchone()[0]
    #defaultoutfit
    sql = "SELECT outfitid FROM characters WHERE id=:characterid"
    result = db.session.execute(sql, {"characterid":characterid})
    outfitid = result.fetchone()[0]
    sql = "SELECT outfitname FROM outfits WHERE id=:outfitid"
    result = db.session.execute(sql, {"outfitid":outfitid})
    outfit = result.fetchone()[0]
    return render_template("character.html", character=character, personality=personality, species=species, outfit = outfit)

@app.route("/editcharacter/<int:id>")
def editcharacter(id):
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
     characterid = id
     sql = "SELECT charactername FROM characters WHERE id=:characterid"
     result = db.session.execute(sql, {"characterid":characterid})
     character = result.fetchone()[0]
     #personality
     sql = "SELECT personalityid FROM characters WHERE id=:characterid"
     result = db.session.execute(sql, {"characterid":characterid})
     personalityid = result.fetchone()[0]
     sql = "SELECT personalityname FROM personalities WHERE id=:personalityid"
     result = db.session.execute(sql, {"personalityid":personalityid})
     personality = result.fetchone()[0]
     sql = "SELECT personalityname FROM personalities WHERE visible=1"
     result = db.session.execute(sql)
     personalitylist = result.fetchall()
     #species
     sql = "SELECT speciesid FROM characters WHERE id=:characterid"
     result = db.session.execute(sql, {"characterid":characterid})
     speciesid = result.fetchone()[0]
     sql = "SELECT speciesname FROM species WHERE id=:speciesid"
     result = db.session.execute(sql, {"speciesid":speciesid})
     species = result.fetchone()[0]
     sql = "SELECT speciesname FROM species WHERE visible=1"
     result = db.session.execute(sql)
     specieslist = result.fetchall()
     #defaultoutfit
     sql = "SELECT outfitid FROM characters WHERE id=:characterid"
     result = db.session.execute(sql, {"characterid":characterid})
     outfitid = result.fetchone()[0]
     sql = "SELECT outfitname FROM outfits WHERE id=:outfitid"
     result = db.session.execute(sql, {"outfitid":outfitid})
     outfit = result.fetchone()[0]
     sql = "SELECT outfitname FROM outfits WHERE visible=1"
     result = db.session.execute(sql)
     outfitlist = result.fetchall()
     return render_template("editcharacter.html", characterid=characterid, character=character, personality=personality, personalitylist=personalitylist, species=species, specieslist=specieslist, outfit = outfit, outfitlist = outfitlist)
    else:
     return "You don't have permission."

@app.route("/editcharactername", methods=["POST"])
def editcharactername():
    id = request.form["id"]
    new = request.form["new"]
    sql = "SELECT charactername FROM characters WHERE charactername=:new AND visible=1"
    result = db.session.execute(sql, {"new":new})
    checkname = result.fetchone()
    if checkname == None:
     sql = "UPDATE characters SET charactername=:new WHERE id=:id"
     db.session.execute(sql, {"new":new, "id":id})
     db.session.commit()
     return redirect("/admin")
    else:
     return "A character with this name already exists."

@app.route("/changecharacterspecies", methods=["POST"])
def changecharacterspecies():
    id = request.form["id"]
    new = request.form["new"]
    sql = "SELECT id FROM species WHERE speciesname=:new"
    result = db.session.execute(sql, {"new":new})
    speciesid = result.fetchone()[0]
    sql = "UPDATE characters SET speciesid=:speciesid WHERE id=:id"
    db.session.execute(sql, {"speciesid":speciesid, "id":id})
    db.session.commit()
    return redirect("/admin")

@app.route("/changecharacterpersonality", methods=["POST"])
def changecharacterpersonality():
    id = request.form["id"]
    new = request.form["new"]
    sql = "SELECT id FROM personalities WHERE personalityname=:new"
    result = db.session.execute(sql, {"new":new})
    personalityid = result.fetchone()[0]
    sql = "UPDATE characters SET personalityid=:personalityid WHERE id=:id"
    db.session.execute(sql, {"personalityid":personalityid, "id":id})
    db.session.commit()
    return redirect("/admin")

@app.route("/changecharacteroutfit", methods=["POST"])
def changecharacteroutfit():
    id = request.form["id"]
    new = request.form["new"]
    sql = "SELECT id FROM outfits WHERE outfitname=:new"
    result = db.session.execute(sql, {"new":new})
    outfitid = result.fetchone()[0]
    sql = "UPDATE characters SET outfitid=:outfitid WHERE id=:id"
    db.session.execute(sql, {"outfitid":outfitid, "id":id})
    db.session.commit()
    return redirect("/admin")

@app.route("/addcharacter")
def addcharacter():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
     #personality
     sql = "SELECT personalityname FROM personalities WHERE visible=1"
     result = db.session.execute(sql)
     personalities = result.fetchall()
     #species
     sql = "SELECT speciesname FROM species WHERE visible=1"
     result = db.session.execute(sql)
     species = result.fetchall()
     #defaultoutfit
     sql = "SELECT outfitname FROM outfits WHERE visible=1"
     result = db.session.execute(sql)
     outfits = result.fetchall()
     return render_template("addcharacter.html", personalities=personalities, species=species, outfits = outfits)
    else:
     return "You don't have permission."

@app.route("/createcharacter", methods=["POST"])
def createcharacter():
    name = request.form["name"]
    personality = request.form["personality"]
    species = request.form["species"]
    outfit = request.form["outfit"]
    birthday = 101
    sql = "SELECT charactername FROM characters WHERE charactername=:name"
    result = db.session.execute(sql, {"name":name})
    checkcharacter = result.fetchone()
    if checkcharacter == None:
     #personality
     sql = "SELECT id FROM personalities WHERE personalityname=:personality"
     result = db.session.execute(sql, {"personality":personality})
     personalityid = result.fetchone()[0]
     #species
     sql = "SELECT id FROM species WHERE speciesname=:species"
     result = db.session.execute(sql, {"species":species})
     speciesid = result.fetchone()[0]
     #defaultoutfit
     sql = "SELECT id FROM outfits WHERE outfitname=:outfit"
     result = db.session.execute(sql, {"outfit":outfit})
     outfitid = result.fetchone()[0]
     sql = "INSERT INTO characters (charactername, personalityid, speciesid, outfitid, birthmmdd, visible) VALUES (:name, :personalityid, :speciesid, :outfitid, :birthday, 1)"
     db.session.execute(sql, {"name":name, "personalityid":personalityid, "speciesid":speciesid, "outfitid":outfitid, "birthday":birthday})
     db.session.commit()   
     return redirect("/admin")
    else:
     return "A character with this name already exists."
