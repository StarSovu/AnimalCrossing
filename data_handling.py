
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from db import db
from app import app
from datetime import date
from os import getenv
import calendar

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(400)
def server_error(e):
    return render_template('400.html'), 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def page_not_found(e):
    return render_template('405.html'), 405

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT username FROM users WHERE username=:username AND visible=1"
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
            sql = "SELECT role FROM users WHERE username=:username"
            result = db.session.execute(sql, {"username":username})
            role = result.fetchone()[0]
            session["role"] = role
            #print (role)
            session["infotext"] = "q"
            del session["infotext"]
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
    del session["role"]
    session["infotext"] = "q"
    del session["infotext"]
    return redirect("/")

@app.route("/register",methods=["POST"])
def register():
    un_min = 3
    un_max = 30
    pwd_min = 4
    pwd_max = 256
    username = request.form["username"]
    username_length = len(username)
    if username_length < un_min:
        session["infotext"] = "Minimum length of username is "+str(un_min)
        return redirect("/")
    else:
        if username_length > un_max:
            session["infotext"] = "Maximum length of username is "+str(un_max)
            return redirect("/")
        else:
            password = request.form["password"]
            password_length = len(password)
            if password_length < pwd_min:
                session["infotext"] = "Minimum length of password is "+str(pwd_min)
                return redirect("/")
            else:
                if password_length > pwd_max:
                    session["infotext"] = "Maximum length of password is "+str(pwd_max)
                    return redirect("/")
            check_password = request.form["rewritepassword"]
            sql = "SELECT password FROM users WHERE username=:username"
            result = db.session.execute(sql, {"username":username})
            user = result.fetchone()
            if user == None:
                if password == check_password:
                    hash_value = generate_password_hash(password)
                    sql = "INSERT INTO users (username, password, role, visible) VALUES (:username, :password, 'user', 1)"
                    db.session.execute(sql, {"username":username, "password":hash_value})
                    db.session.commit()
                    session["username"] = username
                    sql = "SELECT id FROM users WHERE username=:username"
                    result = db.session.execute(sql, {"username":username})
                    userid = result.fetchone()[0]
                    session["userid"] = userid
                    session["infotext"] = "q"
                    del session["infotext"]
                    return redirect("/")
                else:
                    session["infotext"] = "Password does not match"
                    return redirect("/")
            else:
                session["infotext"] = "Username taken"
                return redirect("/")

@app.route("/addisland",methods=["POST"])
def addisland():
    in_min = 1
    islandname = request.form["islandname"]
    if len(islandname) < in_min:
        return "You need to have a longer island name. Minimum length is "+str(in_min)
    else:
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

@app.route("/renameisland",methods=["POST"])
def renameisland():
    in_min = 1
    islandid = request.form["id"]
    new = request.form["new"]
    if len(new) < in_min:
        return "You need to have a longer island name. Minimum length is "+str(in_min)
    else:
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

@app.route("/user/<int:id>")
def page(id):
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
    sql = "SELECT COUNT(*) FROM characteronisland WHERE islandid=:islandid AND visible=1"
    result = db.session.execute(sql, {"islandid":islandid})
    count = result.fetchone()[0]
    if count == 10:
        return "There are already 10 characters on this island. Remove one character to add more."
    else:
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

@app.route("/characterlist")
def characterlist():
    sql = "SELECT charactername, id FROM characters WHERE visible=1"
    result = db.session.execute(sql)
    characters = result.fetchall()
    characters = sorted(characters)
    filter = "none"
    sql = "SELECT speciesname, id FROM species WHERE visible=1"
    result = db.session.execute(sql)
    specieslist = result.fetchall()
    specieslist = sorted(specieslist)
    sql = "SELECT personalityname, id FROM personalities WHERE visible=1"
    result = db.session.execute(sql)
    personalitylist = result.fetchall()
    personalitylist = sorted(personalitylist)
    return render_template("characterlist.html", characters=characters, filter=filter, specieslist=specieslist, personalitylist=personalitylist)

@app.route("/characterlist/species/<int:id>")
def characterlistspecies(id):
    speciesid = id
    sql = "SELECT speciesname FROM species WHERE id=:speciesid AND visible=1"
    result = db.session.execute(sql, {"speciesid":speciesid})
    species = result.fetchone()[0]
    sql = "SELECT charactername, id FROM characters WHERE visible=1 AND speciesid=:speciesid"
    result = db.session.execute(sql, {"speciesid":speciesid})
    characters = result.fetchall()
    filter = "species"
    sql = "SELECT speciesname, id FROM species WHERE visible=1"
    result = db.session.execute(sql)
    specieslist = result.fetchall()
    sql = "SELECT personalityname, id FROM personalities WHERE visible=1"
    result = db.session.execute(sql)
    personalitylist = result.fetchall()
    return render_template("characterlist.html", characters=characters, filter=filter, name=species, specieslist=specieslist, personalitylist=personalitylist)

@app.route("/characterlist/personality/<int:id>")
def characterlistpersonality(id):
    personalityid = id
    sql = "SELECT personalityname FROM personalities WHERE id=:personalityid AND visible=1"
    result = db.session.execute(sql, {"personalityid":personalityid})
    personality = result.fetchone()[0]
    sql = "SELECT charactername, id FROM characters WHERE visible=1 AND personalityid=:personalityid"
    result = db.session.execute(sql, {"personalityid":personalityid})
    characters = result.fetchall()
    filter = "personality"
    sql = "SELECT speciesname, id FROM species WHERE visible=1"
    result = db.session.execute(sql)
    specieslist = result.fetchall()
    sql = "SELECT personalityname, id FROM personalities WHERE visible=1"
    result = db.session.execute(sql)
    personalitylist = result.fetchall()
    return render_template("characterlist.html", characters=characters, filter=filter, name=personality, specieslist=specieslist, personalitylist=personalitylist)

@app.route("/characterlist/month/<int:id>")
def characterlistmonth(id):
    monthid = id
    month = calendar.month_name[monthid]
    sql = "SELECT charactername, id FROM characters WHERE visible=1 AND EXTRACT(MONTH FROM birth)=:monthid"
    result = db.session.execute(sql, {"monthid":monthid})
    characters = result.fetchall()
    filter = "month"
    sql = "SELECT speciesname, id FROM species WHERE visible=1"
    result = db.session.execute(sql)
    specieslist = result.fetchall()
    sql = "SELECT personalityname, id FROM personalities WHERE visible=1"
    result = db.session.execute(sql)
    personalitylist = result.fetchall()
    return render_template("characterlist.html", characters=characters, filter=filter, name=month, specieslist=specieslist, personalitylist=personalitylist)


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
    #birthday
    sql = "SELECT birth FROM characters WHERE id=:characterid"
    result = db.session.execute(sql, {"characterid":characterid})
    month = result.fetchone()[0].strftime("%B")
    sql = "SELECT EXTRACT(DAY FROM birth) FROM characters WHERE id=:characterid"
    result = db.session.execute(sql, {"characterid":characterid})
    day = int(result.fetchone()[0])
    #islands
    sql = "SELECT characteronisland.islandid, islands.islandname FROM islands, characteronisland WHERE characteronisland.characterid=:characterid AND characteronisland.islandid = islands.id AND characteronisland.visible = 1"
    result = db.session.execute(sql, {"characterid":characterid})
    islands = result.fetchall()
    return render_template("character.html", character=character, personality=personality, species=species, outfit = outfit, month = month, day = day, islands = islands)





